# -*- coding: utf-8 -*-
import time
from motor_controller import MotorController
from CMD_Folder import sine

if __name__ == "__main__":
    motor = MotorController(can_port="can2", motor_id=3, torque_constant=2)

    print("Setting current position as zero...")
    motor.set_zero()

    # cmd_value = sine.SineCommand(30, 0.1)
    
    print("Entering interactive motor control loop. Press Ctrl+C to exit.\n")

    try:
        while True:
            # 1. Print status
            print("motor3 status")
            motor.get_motor_status2()
            motor.set_zero()

            # 2. Ask user to select mode
            print("\nSelect control mode:")
            print("1 - Absolute Position Control")
            print("2 - Velocity Control")
            print("3 - Torque Control")
            print("4 - Stop Motor")
            print("5 - Shutdown Motor")
            choice = input("Enter choice (1-5, Enter to keep previous): ").strip()

            if choice == "1":
                current_mode = "position"
                velocity_rpm = float(input("Enter velocity (RPM): "))
                t0 = time.monotonic()
                while True:              
                    t = time.monotonic() - t0
                    # cmd = cmd_value.get(t)
                    cmd_value = float(input("Enter target position (deg): "))
                    motor.position_control(cmd_value, velocity_rpm)
                    time.sleep(0.001)
                    if t>10:
                        break        
            elif choice == "2":
                current_mode = "velocity"
                cmd_value = float(input("Enter velocity (RPM): "))
                motor3.velocity_control(cmd_value)
            elif choice == "3":
                current_mode = "torque"
                cmd_value = float(input("Enter torque (A): "))
                motor.torque_control(cmd_value)
            elif choice == "4":
                motor.stop()
                print("Motor stopped.")
            elif choice == "5":
                motor.shutdown()
                print("Motor shutdown. Exiting program.")
                break
            elif choice == "":
                # Re-apply previous command
                if current_mode == "position":
                    motor.position_control(cmd_value, velocity_rpm)
                elif current_mode == "velocity":
                    motor.velocity_control(cmd_value)
                elif current_mode == "torque":
                    motor.torque_control(cmd_value)

            # Short delay for loop
            time.sleep(0.001)

    except KeyboardInterrupt:
        print("\nExiting interactive control...")
        motor.stop()
        motor.shutdown()

