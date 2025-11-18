# -*- coding: gbk -*-
import myactuator_rmd_py as rmd
import time
driver = rmd.CanDriver("can2")
actuator = rmd.ActuatorInterface(driver, 320)

# Power off motor
actuator.shutdownMotor()
print("Motor powered off")
