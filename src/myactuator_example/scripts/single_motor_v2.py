# -*- coding: utf-8 -*-
import time
from motor_controller import MotorController
from CMD_Folder import sine
import numpy as np
import math

def jointLinearInterpolation(initPos, targetPos, rate):

    rate = np.fmin(np.fmax(rate, 0.0), 1.0)
    p = initPos*(1-rate) + targetPos*rate
    return p

if __name__ == "__main__":

    dt = 0.002
    q_init = 0.0
    motor_cmd = 0.0
    sine_count = 0
    rate_count = 0
    duration_time = 5  # seconds
    sine_mid_q = 10

    motor = MotorController(can_port="can2", motor_id=3, torque_constant=2)
    motor.set_zero()
    motion_time = 0.0

    # Print status
    print(motion_time)
    print("motor status")
    motor.get_motor_status2()

    # User prompt
    print("WARNING: Please ensure there are no obstacles around the robot while running this example.")
    input("Press Enter to continue...")

    try:
        while True:
            time.sleep(0.002)
            motion_time += 1

            if( motion_time >= 0):

                # first, get record initial position
                if( motion_time >= 0 and motion_time < 10):
                    motor_cmd = q_init

                # second, move to the origin point of a sine movement
                if( motion_time >= 10 and motion_time < 400):
                    rate_count += 1
                    rate = rate_count/200.0 # needs count to 200
                    motor_cmd = jointLinearInterpolation(q_init, sine_mid_q, rate)
                
                # last, do sine wave
                freq_hz = 1
                amplitude = 30
                t = dt*sine_count
                if( motion_time >= 400 and motion_time < duration_time/dt):
                    sine_count += 1
                    sin_cmd = amplitude * math.sin(t*freq_hz) + sine_mid_q
                    motor_cmd = sin_cmd

                if( motion_time >= duration_time/dt):
                    motor.stop()
                    motor.shutdown()   

                """
                cmd.motorCmd[d['FR_0']].q = qDes[0]
                cmd.motorCmd[d['FR_0']].dq = 0
                cmd.motorCmd[d['FR_0']].Kp = Kp[0]
                cmd.motorCmd[d['FR_0']].Kd = Kd[0]
                cmd.motorCmd[d['FR_0']].tau = -0.65
                """

            if(motion_time > 10):
                motor.shutdown()

            motor.position_control(motor_cmd, 120) 
            
            # debug print
            #print(f"motion_time: {motion_time} s")  

    except KeyboardInterrupt:
        print("\nExiting interactive control...")
        motor.stop()
        motor.shutdown()

