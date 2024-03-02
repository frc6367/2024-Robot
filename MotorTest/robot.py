import wpilib
import wpilib.drive
import phoenix5
import rev

from robotpy_ext.common_drivers.distance_sensors import SharpIR2Y0A21


class MyRobot(wpilib.TimedRobot):

    # The channel on the driver station that the joystick is connected to
    kJoystickChannel0 = 0
    kJoystickChannel1 = 1

    def robotInit(self):
        self.green_motor = phoenix5.WPI_TalonSRX(7)
        self.black_motor = phoenix5.WPI_TalonSRX(8)

        self.shooter_left_motor = phoenix5.WPI_VictorSPX(5)
        self.shooter_right_motor = phoenix5.WPI_VictorSPX(6)

        self.stick0 = wpilib.Joystick(self.kJoystickChannel0)
        self.stick1 = wpilib.Joystick(self.kJoystickChannel1)

        self.indexer_motor = rev.CANSparkMax(9, rev.CANSparkMax.MotorType.kBrushless)
        self.lower_sensor = SharpIR2Y0A21(0)
        self.middle_sensor = SharpIR2Y0A21(1)

        self.climber_right_motor = rev.CANSparkMax(
            10, rev.CANSparkMax.MotorType.kBrushless
        )
        self.climber_left_motor = rev.CANSparkMax(
            11, rev.CANSparkMax.MotorType.kBrushless
        )

    def robotPeriodic(self) -> None:
        wpilib.SmartDashboard.putNumber("lower", self.lower_sensor.getDistance())
        wpilib.SmartDashboard.putNumber("middle", self.middle_sensor.getDistance())

    def teleopPeriodic(self):

        if False:
            v = self.stick0.getRawAxis(3)

            # code for intake motor test
            if self.stick0.getRawButton(11):
                self.green_motor.set(v)
            else:
                self.green_motor.set(0)

            if self.stick0.getRawButton(12):
                self.black_motor.set(-v)
            else:
                self.black_motor.set(0)

            if self.stick0.getTrigger():
                self.indexer_motor.set(-v)
            else:
                self.indexer_motor.set(0)

            # Shooter
            if self.stick1.getTrigger():
                v = self.stick1.getRawAxis(3)
                self.shooter_left_motor.set(v)
                self.shooter_right_motor.set(-v)
            else:
                self.shooter_left_motor.set(0)
                self.shooter_right_motor.set(0)

        if True:
            self.climber_left_motor.set(self.stick0.getY())
            self.climber_right_motor.set(self.stick1.getY())
