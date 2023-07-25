import sys
# from email.header import UTF8
sys.path.append(R'YOUR_PATH\Python_64\DLL64') #add the path of DLL64 library here
sys.path.append(R'YOUR_PATH\Python_64') #add the path to Python64 here


import time
import numpy as np
from ctypes import *
from array import array
from scipy import integrate
from Elveflow64 import *

# create a new folder to contain calibration file, and add the path here.
Instr_ID = c_int32()
Calib = (c_double*1000)()
Calib_path = R'YOUR_PATH\Calibration\Calib'

class Pressure_Regulator():
    
    # see SDK User Guide to determine regulator/sensor types and NI MAX to determine the instrument name
    # calibration array should have 1000 elements

    def __init__(self, Instr_name = 'YOUR_INSTR_NAME', arg_1 = 5, arg_2 = 0, arg_3 = 0, arg_4 = 0, arg_5 = 1, arg_6 = 4, arg_7 = 0, arg_8 = 0, arg_9 = 7, arg_10 = 2.5):
        # Initialize OB1 and analog flow sensor, edit arguments based on device specifications found in SDK User Guide.
        self.error = OB1_Initialization(Instr_name.encode('ascii'), arg_1, arg_2, arg_3, arg_4, byref(Instr_ID))
        print('error: %d' % self.error)
        print('OB1 ID: %d' % Instr_ID.value)
        self.error = OB1_Add_Sens(Instr_ID, arg_5, arg_6, arg_7, arg_8, arg_9, arg_10)
        print('analog flow sensor error: %d' % self.error)

    def pause(self, custom_message = 'operation completed,'):
        # Asks if the user wants to continue, and takes y/n input.
        self.answer = input('%s continue? ([y]/n): ' % custom_message)

        if self.answer != 'y':
            sys.exit()
              
    def default_calibration(self):
        # Perform default calibration, this command is incomplete.
        self.error = Elveflow_Calibration_Default(byref(Calib),1000)
        print('default calibration error: %d' % self.error)

    def load_calibration(self):
        # Load a previous calibration located at the specified file path, this command is incomplete.
        error = Elveflow_Calibration_Load(Calib_path.encode('ascii'), byref(Calib), 1000)
        print('load calibration error: %d' % self.error)

    def new_calibration(self):
        # Use this command over the previous two because it actually calibrates device rather than reading calibration file.
        # Start a new calibration and save calibration file to specified path.
        OB1_Calib(Instr_ID.value, Calib, 1000)
        self.error = Elveflow_Calibration_Save(Calib_path.encode('ascii'), byref(Calib), 1000)
        print('calib saved in %s' % Calib_path.encode('ascii'))
        print('new calibration error: %d' % self.error)

    def load_sample(self, set_channel = 1, set_pressure = 60, target_volume = 100):
        # Pressure is in mbar, volume is in μL.
        # Set a target volume based on microfluidic setup, ensure that target volume does not exceed length of tubing and overflows waste container.
        self.channel = c_int32(set_channel) # convert to c_int32
        self.pressure = c_double(set_pressure) # convert to c_double
        self.data_sens = c_double()
        self.error = OB1_Set_Press(Instr_ID.value, self.channel, self.pressure, byref(Calib), 1000)

        # Loop to integrate flow rate to find volume
        self.repeat = True
        self.times = [0]
        self.flo_rates = [0]
        self.time0 = time.time()

        while self.repeat:
            self.error = OB1_Get_Sens_Data(Instr_ID.value, self.channel, 1, byref(self.data_sens)) # Acquire_data = 1 -> read all the analog values
            self.flo_rates.append(float(self.data_sens.value))
            self.times.append(float((time.time() - self.time0) / 60))

            self.volume_passed = integrate.simpson(self.flo_rates, self.times)

            if self.volume_passed >= target_volume:
                self.error = OB1_Set_Press(Instr_ID.value, self.channel, c_double(0), byref(Calib), 1000)
                print('sample has been loaded, total volume passed: %d μL' % self.volume_passed)
                self.repeat = False

            if self.error != 0:
                print('error: %d' % self.error)
                self.repeat = False

    def flush(self, set_channel = 1, first_pressure = 100, second_pressure = 0, sleep_time = 90):
        # Wash out microfluidic device with solution in a given channel
        self.channel = c_int32(set_channel) # convert to c_int32
        self.pressure = (c_double(first_pressure), c_double(second_pressure)) # convert to c_double
        self.error = OB1_Set_Press(Instr_ID.value, self.channel, self.pressure[0], byref(Calib), 1000)
        time.sleep(sleep_time)
        self.error = OB1_Set_Press(Instr_ID.value, self.channel, self.pressure[1], byref(Calib), 1000)

        print('error: %d' % self.error)

    def terminate(self):
        # Only pass this command if OB1 is disconnected from microfluidic setup, and air/vaccum lines are shut off.
        self.error = OB1_Destructor(Instr_ID.value)
        print('OB1 termination error: %d' % self.error) 

'''
Troubleshooting:

OB1_Set_Press(ascii('01FB0FC6'), 1, 0, byref(Calib), 1000)

get_pressure = c_double()
OB1_Get_Press(ascii('01FB0FC6'), 1, 1, byref(Calib), byref(get_pressure), 1000)
print(get_pressure.value)

'''
