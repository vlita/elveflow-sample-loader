import OB1
import MUX

# Example requires 4 seperate vials containing samples: 2 test samples, a wash sample, and an empty vial for a dry step. 

p = OB1.Pressure_Regulator()
s = MUX.Sample_Distributor()

p.pause(custom_message = 'OB1/MUX initialization completed, you may now turn on air/vaccum lines,')

s.home()

p.pause(custom_message = 'MUX homing complete, ready to calibrate OB1,')

p.new_calibration()

p.pause(custom_message = 'calibration completed, you may now connect OB1 to microfluidic setup,')

s.switch_valve(valve_number = 1)

p.load_sample(set_pressure = 40, target_volume = 60)

p.pause()

s.switch_valve(valve_number = 3)

p.flush(first_pressure = 100, sleep_time = 90)

p.pause(custom_message = 'wash step completed,')

s.switch_valve(valve_number = 4)

p.flush(first_pressure = 150, sleep_time = 120)

p.pause(custom_message = 'first dry step completed,')

s.switch_valve(valve_number = 1)

p.load_sample(set_pressure = 40, target_volume = 60)

p.pause()

s.switch_valve(valve_number = 3)

p.flush(first_pressure = 100, sleep_time = 90)

p.pause(custom_message = 'wash step completed,')

s.switch_valve(valve_number = 4)

p.flush(first_pressure = 150, sleep_time = 120)

p.pause(custom_message = 'second dry step completed, dont forget to turn off air/vaccum lines before termination,')

p.terminate()

s.terminate()