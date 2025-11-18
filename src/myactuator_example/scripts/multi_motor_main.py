# -*- coding: utf-8 -*-
import time
import math
from motor_controller import MotorController
from CMD_Folder import sine
from Ankle_Folder import ankle

if __name__ == "__main__":
    motor3 = MotorController(can_port="can2", motor_id=3, torque_constant=2)
    motor4 = MotorController(can_port="can2", motor_id=4, torque_constant=2)
    Ankle1 = ankle.Ankle()
    dtr = math.pi/180

    print("Current position set as encoder zero point")
    motor3.set_zero()
    motor4.set_zero()

    # Initialize default mode
    current_mode = "position"
    cmd = sine.SineCommand(30, 0.1)
    
    print("Entering interactive motor control loop. Press Ctrl+C to exit.\n")

    try:
        while True:
            # 1. Print status
            print("motor3 status")
            motor3.get_motor_status2()
            print("motor4 status")
            motor4.get_motor_status2()

            # 2. Ask user to select mode
            print("\nSelect control mode:")
            print("1 - Absolute Position Control")
            print("2 - Velocity Control")
            print("3 - Torque Control")
            print("4 - Stop Motor")
            print("5 - Set_zero")
            print("6 - Shutdown Motor")
            choice = input("Enter choice (1-5, Enter to keep previous): ").strip()

            if choice == "1":
                current_mode = "position"
                velocity_rpm = float(input("Enter velocity (RPM): "))
                t0 = time.monotonic()
                while True:              
                    t = time.monotonic() - t0
                    AKP_ref = cmd.get(t)*dtr
                    AKR_ref = cmd.get(t)*dtr
                    motor3_ref,motor4_ref = Ankle1.IK(AKP_ref,AKR_ref)/dtr
                    print("Time: ",t)                
                    motor3.position_control(motor3_ref, velocity_rpm)
                    motor4.position_control(motor4_ref, velocity_rpm)
                    time.sleep(0.001)
                    if t>10:
                        break        
            elif choice == "2":
                current_mode = "velocity"
                cmd_value = float(input("Enter velocity (RPM): "))
                motor3.velocity_control(cmd_value)
                motor4.velocity_control(cmd_value)
            elif choice == "3":
                current_mode = "torque"
                cmd_value = float(input("Enter torque (A): "))
                motor3.torque_control(cmd_value)
                motor4.torque_control(cmd_value)
            elif choice == "4":
                motor3.stop()
                motor4.stop()
                print("Motor stopped.")
            elif choice == "5":
                motor3.set_zero()
                motor4.set_zero()
                print("Motor set to zero point.")
            elif choice == "6":
                motor3.shutdown()
                motor4.shutdown()
                print("Motor shutdown. Exiting program.")
                break
            elif choice == "":
                # Re-apply previous command
                if current_mode == "position":
                    motor3.position_control(cmd_value, velocity_rpm)
                elif current_mode == "velocity":
                    motor3.velocity_control(cmd_value)
                elif current_mode == "torque":
                    motor3.torque_control(cmd_value)

            # Short delay for loop
            time.sleep(0.001)

    except KeyboardInterrupt:
        print("\nExiting interactive control...")
        motor3.stop()
        motor3.shutdown()

