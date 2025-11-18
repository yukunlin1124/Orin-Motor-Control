import myactuator_rmd_py as rmd
import time
import threading

# Initialize CAN driver and actuator interface
driver = rmd.CanDriver("can2")
actuator = rmd.ActuatorInterface(driver, 3)

# Global variable to store the current velocity (in RPM)
current_velocity_rpm = 0.0

# Shared exit flag
exit_flag = False
exit_flag_lock = threading.Lock()

# Function to handle velocity updates based on user input
def update_velocity():
    global current_velocity_rpm, exit_flag
    while True:
        try:
            # Take user input for velocity setpoint in RPM
            user_input = input("Enter velocity setpoint (RPM) or 'exit' to quit: ")

            # If user wants to exit, set the exit flag
            if user_input.lower() == 'exit':
                with exit_flag_lock:
                    exit_flag = True
                print("Exiting program.")
                break

            # Validate input and set velocity (in RPM)
            new_velocity_rpm = float(user_input)
            print(f"Setting velocity to {new_velocity_rpm} RPM.")
            current_velocity_rpm = new_velocity_rpm  # Keep it in RPM
        except ValueError:
            print("Invalid input. Please enter a valid number or 'exit' to quit.")

# Function to continuously control the motor
def control_motor():
    global current_velocity_rpm, exit_flag
    while True:
        with exit_flag_lock:
            if exit_flag:
                break
        try:
            # Convert RPM to DPS (degrees per second)
            current_velocity_dps = current_velocity_rpm * 6  # Conversion factor

            # Send the current velocity setpoint to the actuator (in DPS)
            actuator.sendVelocitySetpoint(current_velocity_dps)  # Send in DPS
            time.sleep(0.1)  # Update the setpoint every 0.1 seconds (10 Hz)
        except Exception as e:
            print(f"Error controlling motor: {e}")
            break

    # Ensure motor is stopped when exiting
    actuator.stopMotor()
    print("Motor stopped.")

# Main function to set up threads and start the program
def main():
    global exit_flag
    # Start the input thread to update velocity
    input_thread = threading.Thread(target=update_velocity)
    input_thread.daemon = True  # This ensures the thread will exit when the main program exits
    input_thread.start()

    # Start the motor control loop
    control_motor()

if __name__ == "__main__":
    main()

