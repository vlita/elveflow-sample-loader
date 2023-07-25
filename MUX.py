import sys
sys.path.append(R'YOUR_PATH\Python_64\DLL64') #add the path of DLL64 library here
sys.path.append(R'YOUR_PATH\Python_64') #add the path to Python64 here

import time
from ctypes import *
from array import array
from Elveflow64 import *

Instr_ID = c_int32()
Answer = (c_char*40)()

class Sample_Distributor():

    def __init__(self, Instr_name = 'YOUR_INSTR_NAME'):
        # Initialize MUX Distributor, edit arguments based on device specifications found in SDK User Guide.
        self.error = MUX_DRI_Initialization(Instr_name.encode('ascii'), byref(Instr_ID))
        print('initialization error: %d' % self.error)

    def home(self):
        # Command to home valve (only for MUX Distribution and Recirculation).
        # Do not set a new valve position until homing is completed
        self.error = MUX_DRI_Send_Command(Instr_ID.value, 0, Answer, 40)
        time.sleep(5) 
        print('Answer: %s' % Answer.value)
        print('set home error: %d' % self.error)

    def switch_valve(self, valve_number):
        # Set valve to a certain position
        self.valve_pos = c_int32(int(valve_number))
        self.error = MUX_DRI_Set_Valve(Instr_ID.value, self.valve_pos, 0) # shortest distance: 0, clockwise: 1 or counterclockwise: 2.

        if self.error != 0:
            print('valve switch error: %d' % self.error)

    def read_valve(self):
        #Read valve position.
        self.cur_valve = c_int32(-1)
        self.error = MUX_DRI_Get_Valve(Instr_ID.value, byref(self.cur_valve)) #get the active valve. it returns 0 if valve is busy.
        print('current valve position: %d' % self.cur_valve.value)
        
        if self.error != 0:
            print('valve read error: %d' % self.error)

    def terminate(self):
        # Only pass this command if MUX is disconnected from microfluidic setup, and no fluid is running through the valves.
        self.error = MUX_DRI_Destructor(Instr_ID.value)
        print('MUX termination error: %d' % self.error)

