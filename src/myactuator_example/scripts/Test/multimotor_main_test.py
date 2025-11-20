import myactuator_rmd_py as rmd
import time
import threading

# Initialize CAN driver and actuator interfaces for two motors
driver = rmd.CanDriver("can2")
motor1 = rmd.ActuatorInterface(driver, 1)  # Motor 1 (ID = 1)
motor3 = rmd.ActuatorInterface(driver, 3)  # Motor 3 (ID = 3)

# Global variables to store the current velocity for both motors (in RPM)
current_velocity_rpm_motor1 = 0.0
current_velocity_rpm_motor3 = 0.0

# Shared exit flag
exit_flag = False
exit_flag_lock = threading.Lock()

# Function to handle velocity updates based on user input for both motors
def update_velocity():
    global current_velocity_rpm_motor1, current_velocity_rpm_motor3, exit_flag
    while True:
        try:
            # Take user input for velocity setpoints (RPM) for both motors
            user_input = input("Enter velocity setpoint for Motor 1 (RPM), Motor 3 (RPM), or 'exit' to quit: ")

            # If user wants to exit, set the exit flag
            if user_input.lower() == 'exit':
                with exit_flag_lock:
                    exit_flag = True
                print("Exiting program.")
                break

            # Validate input and set velocity for both motors
            velocities = user_input.split()  # Split input into two values for both motors
            if len(velocities) == 2:
                new_velocity_motor1 = float(velocities[0])
                new_velocity_motor3 = float(velocities[1])

                print(f"Setting velocity for Motor 1 to {new_velocity_motor1} RPM.")
                print(f"Setting velocity for Motor 3 to {new_velocity_motor3} RPM.")

                current_velocity_rpm_motor1 = new_velocity_motor1  # Set velocity for Motor 1
                current_velocity_rpm_motor3 = new_velocity_motor3  # Set velocity for Motor 3
            else:
                print("Please enter two values: one for Motor 1 and one for Motor 3.")

        except ValueError:
            print("Invalid input. Please enter valid numbers for both motors or 'exit' to quit.")

# Function to continuously control both motors
def control_motors():
    global current_velocity_rpm_motor1, current_velocity_rpm_motor3, exit_flag
    while True:
        with exit_flag_lock:
            if exit_flag:
                break
        try:
            # Convert RPM to DPS (degrees per second) for both motors
            current_velocity_dps_motor1 = current_velocity_rpm_motor1 * 6  # Conversion factor for Motor 1
            current_velocity_dps_motor3 = current_velocity_rpm_motor3 * 6  # Conversion factor for Motor 3

            # Send the current velocity setpoint to both motors (in DPS)
            motor1.sendVelocitySetpoint(current_velocity_dps_motor1)  # Send to Motor 1
            motor3.sendVelocitySetpoint(current_velocity_dps_motor3)  # Send to Motor 3

            time.sleep(0.1)  # Update the setpoints every 0.1 seconds (10 Hz)
        except Exception as e:
            print(f"Error controlling motors: {e}")
            break

    # Ensure motors are stopped when exiting
    motor1.stopMotor()
    motor3.stopMotor()
    print("Motors stopped.")

# Main function to set up threads and start the program
def main():
    global exit_flag
    # Start the input thread to update velocity
    input_thread = threading.Thread(target=update_velocity)
    input_thread.daemon = True  # This ensures the thread will exit when the main program exits
    input_thread.start()

    # Start the motor control loop
    control_motors()

if __name__ == "__main__":
    main()

