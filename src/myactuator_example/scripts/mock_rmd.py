class MockStatus:
    def __init__(self):
        self.temperature = 25
        self.voltage = 24
        self.error_code = 0
        self.shaft_speed = 0
        self.current = 0
        self.shaft_angle = 0


class ActuatorInterface:
    def __init__(self, driver, motor_id):
        self.motor_id = motor_id
        self.status = MockStatus()

    # ---- Mock control commands (just print instead of sending CAN) ----
    def sendPositionAbsoluteSetpoint(self, pos_deg, vel_dps):
        print(f"[MOCK] M{self.motor_id} Position cmd = {pos_deg}, vel = {vel_dps}")

    def sendVelocitySetpoint(self, vel_dps):
        print(f"[MOCK] M{self.motor_id} Velocity cmd = {vel_dps}")

    def sendCurrentSetpoint(self, amps):
        print(f"[MOCK] M{self.motor_id} Torque cmd = {amps}")

    # ---- Mock utilities ----
    def setCurrentPositionAsEncoderZero(self):
        print(f"[MOCK] M{self.motor_id} Zero set")

    def stopMotor(self):
        print(f"[MOCK] M{self.motor_id} Stop")

    def shutdownMotor(self):
        print(f"[MOCK] M{self.motor_id} Shutdown")

    def reset(self):
        print(f"[MOCK] M{self.motor_id} Reset")

    def getMultiTurnAngle(self):
        return self.status.shaft_angle

    # ---- Mock status ----
    def getMotorStatus1(self):
        return self.status

    def getMotorStatus2(self):
        return self.status

    def getMotorStatus3(self):
        return self.status


class CanDriver:
    def __init__(self, can_port):
        print(f"[MOCK] CAN Driver initialized on {can_port}")
