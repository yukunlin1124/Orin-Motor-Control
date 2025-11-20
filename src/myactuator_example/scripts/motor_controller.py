# -*- coding: utf-8 -*-
import time
import myactuator_rmd_py as rmd


class MotorController:
    def __init__(self, 
                 can_port="can0",
                 motor_id=1,
                 torque_constant=1):             # Nm per Amp (example)
        """
        Motor controller wrapper for MyActuator motors.

        Parameters
        ----------
        can_port : str
            CAN interface name (e.g., "can0").
        motor_id : int
            Motor CAN ID.
        torque_constant : float
            Motor torque constant (Nm/A).
        """

        # -------- store attributes --------
        self.can_port = can_port
        self.motor_id = motor_id
        self.torque_constant = torque_constant
	
        # -------- hardware setup --------
        self.driver = rmd.CanDriver(can_port)
        self.actuator = rmd.ActuatorInterface(self.driver, motor_id)

    # ============================================================
    # UNIT CONVERSIONS
    # ============================================================
    @staticmethod
    def rpm_to_deg_per_sec(rpm):
        """Convert RPM → deg/s"""
        return rpm * 6.0

    @staticmethod
    def deg_per_sec_to_rpm(dps):
        """Convert deg/s → RPM"""
        return dps / 6.0

    # ============================================================
    # POSITION CONTROL (ABSOLUTE)
    # ============================================================
    def position_control(self, target_deg, velocity_rpm):
        """
        Move motor to an absolute angle (deg)
        """
        vel_dps = self.rpm_to_deg_per_sec(velocity_rpm)
        self.actuator.sendPositionAbsoluteSetpoint(target_deg, vel_dps)

    # ============================================================
    # VELOCITY CONTROL
    # ============================================================
    def velocity_control(self, rpm):
        """
        Continuous rotation at a specified RPM.
        """
        vel_dps = self.rpm_to_deg_per_sec(rpm)
        self.actuator.sendVelocitySetpoint(vel_dps)

    # ============================================================
    # TORQUE CONTROL
    # ============================================================
    def torque_control(self, current_amp):
        """
        Apply motor torque by commanding current (A).
        """
        self.actuator.sendCurrentSetpoint(current_amp)

    def torque_to_current(self, desired_torque):
        """
        Convert torque (Nm) → required current (A) using torque_constant.
        """
        return desired_torque / self.torque_constant

    def send_torque(self, torque_nm):
        """
        Command torque directly in Nm (converted automatically to current).
        """
        current = self.torque_to_current(torque_nm)
        self.torque_control(current)

    # ============================================================
    # UTILITY
    # ============================================================
    def stop(self):
        """Stop motor movement."""
        self.actuator.stopMotor()

    def shutdown(self):
        """Disable motor power."""
        self.actuator.shutdownMotor()

    def set_zero(self):
        """Set current multi-turn position as zero."""
        self.actuator.setCurrentPositionAsEncoderZero()
        self.actuator.shutdownMotor()
        self.actuator.reset()
        time.sleep(1)
        self.driver = rmd.CanDriver(self.can_port)
        self.actuator = rmd.ActuatorInterface(self.driver, self.motor_id)
    # ============================================================
    # MOTOR STATUS
    # ============================================================
    def get_motor_status1(self):
        status1 = self.actuator.getMotorStatus1()
        print(f"""
        Motor Status 1:
        Temperature: {status1.temperature}°C
        Brake Status: {'Released' if status1.is_brake_released else 'Locked'}
        Voltage: {status1.voltage}V
        Error Code: {status1.error_code}
        """)
    def get_motor_status2(self):
        status2 = self.actuator.getMotorStatus2()
        print(f"""
        Motor Status 2:
        Temperature: {status2.temperature}°C
        Current: {status2.current}A
        Shaft Speed: {status2.shaft_speed} RPM
        Shaft Angle: {status2.shaft_angle}°
        """)
    def get_motor_status3(self):
        status3 = self.actuator.getMotorStatus3()    
        print(f"""
        Motor Status 3:
        Temperature: {status3.temperature}°C
        Phase A Current: {status3.current_phase_a}A
        Phase B Current: {status3.current_phase_b}A
        Phase C Current: {status3.current_phase_c}A
        """)
    # ============================================================
    # READ FEEDBACK VALUES
    # ============================================================
    def read_feedback(self):
        """Return motor feedback in a dict."""
        s2 = self.actuator.getMotorStatus2()

        position = self.actuator.getMultiTurnAngle()

        return {
            "temperature": s2.temperature,
            "current": s2.current,
            "velocity": s2.shaft_speed,      # RPM
            "position": float(position),
        }    
