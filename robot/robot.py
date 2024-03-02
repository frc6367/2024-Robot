import wpilib
import wpilib.drive

# from misc.ejoystick import EnhancedJoystick

import magicbot
import phoenix5

# import navx
import rev
from robotpy_ext.common_drivers.distance_sensors import SharpIR2Y0A21
from wpimath.filter import SlewRateLimiter

# from misc.led_controller import LEDController

from subsystems.climber import Climber
from subsystems.drivetrain import DriveTrain
from subsystems.floorintake import FloorIntake
from subsystems.shooter import Shooter
from subsystems.indexer import Indexer

# from misc.sparksim import CANSparkMax


# def map_range(x, a, b, c, d):
#     y = (x - a) / (b - a) * (d - c) + c
#     return y


# def twitch_range(y):
#     return map_range(y, -1.0, 1.0, 0.5, 0.25)


class MyRobot(magicbot.MagicRobot):
    floorintake: FloorIntake
    drivetrain: DriveTrain
    climber: Climber
    shooter: Shooter
    indexer: Indexer

    # ##Joysticks
    # # The channel on the driver station that the joystick is connected to
    kJoystickChannel0 = 0
    kJoystickChannel1 = 1

    def createObjects(self):
        # Joysticks
        # self.speed_limiter = SlewRateLimiter(3)
        # self.twist_limiter = SlewRateLimiter(0.5)
        self.stick0 = wpilib.Joystick(self.kJoystickChannel0)
        self.stick1 = wpilib.Joystick(self.kJoystickChannel1)

        ##Drivetrain
        self.drive_l1 = phoenix5.WPI_TalonSRX(4)
        self.drive_l2 = phoenix5.WPI_TalonSRX(3)
        self.drive_r1 = phoenix5.WPI_TalonSRX(1)
        self.drive_r2 = phoenix5.WPI_TalonSRX(2)

        self.drive_r1.setInverted(True)
        self.drive_r2.setInverted(True)

        ## floor intake
        # self.floorintake_front_motor = phoenix5.WPI_TalonSRX(7)
        # self.floorintake_back_motor = phoenix5.WPI_TalonSRX(8)

        self.green_motor = phoenix5.WPI_TalonSRX(7)
        self.black_motor = phoenix5.WPI_TalonSRX(8)

        ## shooter
        self.shooter_left_motor = phoenix5.WPI_VictorSPX(5)
        self.shooter_right_motor = phoenix5.WPI_VictorSPX(6)

        ## indexer
        self.indexer_motor = rev.CANSparkMax(9, rev.CANSparkMax.MotorType.kBrushless)
        self.indexer_upper_sensor = SharpIR2Y0A21(0)
        self.indexer_lower_sensor = SharpIR2Y0A21(1)

        ## climber
        self.climber_right_motor = rev.CANSparkMax(
            10, rev.CANSparkMax.MotorType.kBrushless
        )
        self.climber_left_motor = rev.CANSparkMax(
            11, rev.CANSparkMax.MotorType.kBrushless
        )

    def teleopPeriodic(self):
        # # Use the joystick X axis for lateral movement, Y axis for forward
        # # movement, and Z axis for rotation.
        # self.drivetrain.move(
        #     -self.stick0.getY(),
        #     -self.stick0.getTwist()n
        # )
        self.drivetrain.move(-self.stick0.getY(), -self.stick0.getTwist())

        ## grabs the node
        if self.stick0.getRawButton(5):
            self.floorintake.grab()

        ## grabs node from source
        if self.stick0.getRawButton(6):
            self.shooter.sourceIntake()

        ## shoots the node
        if self.stick0.getRawButton(7):
            self.shooter.shoot()
        # extends the right arm of the climber
        if self.stick0.getRawButton(9):
            self.climber.right_climb()

        # retracts the right arm of the climber
        if self.stick0.getRawButton(10):
            self.climber.right_retracting()
