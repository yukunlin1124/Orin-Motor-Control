import myactuator_rmd_py as rmd
import time

# Initialize CAN driver and actuator interface
driver = rmd.CanDriver("can2")  # Using can2
actuator = rmd.ActuatorInterface(driver, 3)  # CAN ID set to 3

# Get version number
print("Version number:", actuator.getVersionDate())
