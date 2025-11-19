# -*- coding: utf-8 -*-
import time
import math
from motor_controller import MotorController
from CMD_Folder.sine import SineCommand
from CMD_Folder.poly345 import Poly345Command
from Ankle_Folder import ankle

def jointLinearInterpolation(initPos, targetPos, rate):

    rate = np.fmin(np.fmax(rate, 0.0), 1.0)
    p = initPos*(1-rate) + targetPos*rate
    return p
   
if __name__ == "__main__":

    motor1 = MotorController(can_port="can2", motor_id=1, torque_constant=1.5)
    motor2 = MotorController(can_port="can2", motor_id=2, torque_constant=1.5)
    motor3 = MotorController(can_port="can2", motor_id=3, torque_constant=2)
    motor4 = MotorController(can_port="can2", motor_id=4, torque_constant=2)
    ankle_left = ankle.Ankle()
    dtr = math.pi/180
    duration_time = 5

    # Initialize Command
    ankle_p_cmd = Poly345Command(20, -20, 5)
    ankle_r_cmd = Poly345Command(5, -5, 5)
    knee_cmd = Poly345Command(-10, 90, 5)
    hip_p_cmd = Poly345Command(-30, 30, 5)
    
    print("Entering interactive motor control loop. Press Ctrl+C to exit.\n")

    try:
        while True:
            # Short delay for loop
            time.sleep(0.002)
            # 1. Print status
            print("motor1 status")
            motor1.get_motor_status2()
            print("motor2 status")
            motor2.get_motor_status2()
            print("motor3 status")
            motor3.get_motor_status2()
            print("motor4 status")
            motor4.get_motor_status2()

            # 2. Ask user to select mode
            print("\nSelect control mode:")
            print("1 - Absolute Position Control")
            print("2 - Impedance Control")
            print("3 - Set Motor Zero")
            print("4 - Move to Joint Zero")
            print("5 - Stop Motor")
            print("6 - Shutdown Motor")
            choice = input("Enter choice (1-6): ").strip()

            if choice == "1":
                print("Absolute position mode")
                velocity_rpm = float(input("Enter velocity (RPM): "))
                t0 = time.monotonic()
                while True:           
                    t = time.monotonic() - t0

                    # For debugging: print command values
                    #ankle_p_cmd.print(t)
                    #ankle_r_cmd.print(t)
                    #knee_cmd.print(t)
                    #hip_p_cmd.print(t)  

                    motor1_cmd,motor2_cmd = ankle_left.IK(ankle_p_cmd.get(t)*dtr,ankle_r_cmd.get(t)*dtr)
                    motor3_cmd = knee_cmd.get(t)
                    motor4_cmd = hip_p_cmd.get(t)               
                    motor1.position_control(motor1_cmd/dtr, velocity_rpm)
                    motor2.position_control(-motor2_cmd/dtr, velocity_rpm) # Negative sign for motor2
                    motor3.position_control(motor3_cmd, velocity_rpm)
                    motor4.position_control(motor4_cmd, velocity_rpm)
                    time.sleep(0.002)

                    if t>duration_time:
                        break   
            elif choice == "2":
                print("Impedence mode")         
            elif choice == "3":
                motor1.set_zero()
                motor2.set_zero()
                motor3.set_zero()
                motor4.set_zero()
                print("Motor set to zero point.")
            elif choice == "4":
                motor1_cmd, motor2_cmd = ankle_left.IK(0, 0)
                motor1.position_control(motor1_cmd/dtr, 30)
                motor2.position_control(-motor2_cmd/dtr, 30)
                motor3.position_control(0, 30)
                motor4.position_control(0, 30)
                print("Move joint to zero point.")                     
            elif choice == "5":
                motor1.stop()
                motor2.stop()
                motor3.stop()
                motor4.stop()
                print("Motor stopped.")
            elif choice == "6":
                motor1.shutdown()
                motor2.shutdown()
                motor3.shutdown()
                motor4.shutdown()
                print("Motor shutdown. Exiting program.")
                break

    except KeyboardInterrupt:
        print("\nExiting interactive control...")
        motor1.stop()
        motor1.shutdown()
        motor2.stop()
        motor2.shutdown()
        motor3.stop()
        motor3.shutdown()
        motor4.stop()
        motor4.shutdown()
