import wpilib
import wpilib.drive

# from misc.ejoystick import EnhancedJoystick

import magicbot
import phoenix5

# import navx
import rev
from robotpy_ext.common_drivers.distance_sensors import SharpIR2Y0A21
from wpimath.filter import SlewRateLimiter

from misc.ejoystick import EnhancedJoystick

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


def map_range(x, a, b, c, d):
    y = (x - a) / (b - a) * (d - c) + c
    return y


def twitch_range(y):
    return map_range(y, -1.0, 1.0, 0.5, 0.25)


class MyRobot(magicbot.MagicRobot):
    floorintake: FloorIntake
    drivetrain: DriveTrain
    right_climber: Climber
    left_climber: Climber
    shooter: Shooter
    indexer: Indexer

    # ##Joysticks
    # # The channel on the driver station that the joystick is connected to
    kJoystickChannel0 = 0
    kJoystickChannel1 = 1

    def createObjects(self):
        # Joysticks
        self.stick = EnhancedJoystick(0)
        self.speed_limiter = SlewRateLimiter(3)
        self.twist_limiter = SlewRateLimiter(0.5)

        self.climb_stick = wpilib.Joystick(1)

        ##Drivetrain
        self.drive_l1 = phoenix5.WPI_TalonSRX(4)
        self.drive_l2 = phoenix5.WPI_TalonSRX(3)
        self.drive_r1 = phoenix5.WPI_TalonSRX(1)
        self.drive_r2 = phoenix5.WPI_TalonSRX(2)

        self.drive_r1.setInverted(True)
        self.drive_r2.setInverted(True)

        ## floor intake
        self.green_motor = phoenix5.WPI_TalonSRX(7)
        self.black_motor = phoenix5.WPI_TalonSRX(8)
        self.black_motor.setInverted(True)

        ## shooter
        self.shooter_left_motor = phoenix5.WPI_VictorSPX(5)
        self.shooter_right_motor = phoenix5.WPI_VictorSPX(6)

        ## indexer
        self.indexer_motor = rev.CANSparkMax(9, rev.CANSparkMax.MotorType.kBrushless)
        self.indexer_motor.setInverted(True)
        self.indexer_upper_sensor = SharpIR2Y0A21(0)
        self.indexer_lower_sensor = SharpIR2Y0A21(1)

        ## climber
        self.right_climber_motor = rev.CANSparkMax(
            10, rev.CANSparkMax.MotorType.kBrushless
        )
        self.left_climber_motor = rev.CANSparkMax(
            11, rev.CANSparkMax.MotorType.kBrushless
        )
        self.left_climber_motor.setInverted(False)
        self.right_climber_motor.setInverted(True)

        self.right_climber_sensor = wpilib.DigitalInput(4)
        self.left_climber_sensor = wpilib.DigitalInput(5)

    def teleopPeriodic(self):
        # # Use the joystick X axis for lateral movement, Y axis for forward
        twitch = twitch_range(self.stick.getRawAxis(3))

        speed1 = -self.stick.getEnhY()
        speed = self.speed_limiter.calculate(speed1)
        rotation = -self.stick.getEnhTwist() * abs(twitch)
        rotation = self.twist_limiter.calculate(rotation)

        self.drivetrain.move(speed, rotation)

        ## Output the node
        if self.stick.getRawButton(4):
            self.floorintake.reverse()

        ## grabs the node
        if self.stick.getRawButton(2):
            self.floorintake.grab()

        ## grabs node from source
        if self.stick.getRawButton(3):
            self.shooter.sourceIntake()

        ## shoots the node
        if self.stick.getTrigger():
            self.shooter.shoot()

        ## shoots the amp
        if self.stick.getRawButton(11):
            self.shooter.shootAmp()

        # Joystick based climber
        if True:
            cy = self.climb_stick.getY()
            if self.climb_stick.getRawButton(11):
                self.left_climber.direct(cy)
            if self.climb_stick.getRawButton(12):
                self.right_climber.direct(-cy)

        # extends the right arm of the climber
        # if self.stick.getRawButton(9):
        #     self.climber.right_climb()

        # # retracts the right arm of the climber
        # if self.stick.getRawButton(10):
        #     self.climber.right_retracting()
