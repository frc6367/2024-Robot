import wpilib
import wpilib.drive
import constants
from ntcore.util import ntproperty

import math

# from misc.ejoystick import EnhancedJoystick

import magicbot
import phoenix5

import navx
import rev
from robotpy_ext.common_drivers.distance_sensors import SharpIR2Y0A21
from wpimath.filter import SlewRateLimiter

from misc.ejoystick import EnhancedJoystick

from misc.led_controller import LEDController

from subsystems.climber import Climber
from subsystems.drivetrain import DriveTrain, EncoderPID, NavxPID
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
    return map_range(y, -1.0, 1.0, 0.9, 0.25)


def squared(v):
    return math.copysign(v * v, v)


CLIMB_WITH_JOYSTICK = False


class MyRobot(magicbot.MagicRobot):
    encoder_pid: EncoderPID
    navx_pid: NavxPID
    floorintake: FloorIntake
    drivetrain: DriveTrain
    right_climber: Climber
    left_climber: Climber
    shooter: Shooter
    indexer: Indexer
    led_controller: LEDController

    # ##Joysticks
    # # The channel on the driver station that the joystick is connected to
    kJoystickChannel0 = 0
    kJoystickChannel1 = 1

    ll_led = ntproperty("/limelight/ledMode", 0.0)

    @magicbot.feedback
    def encoder_l_d(self):
        return self.encoder_l.getDistance()

    @magicbot.feedback
    def encoder_r_d(self):
        return self.encoder_r.getDistance()

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

        self.drivetrain_sensor = SharpIR2Y0A21(2)

        self.navx = navx.AHRS.create_spi()

        ### make sure to check the numbers for the encoders are correct
        self.encoder_l = wpilib.Encoder(0, 1)
        self.encoder_r = wpilib.Encoder(2, 3)
        self.encoder_l.setDistancePerPulse(constants.kDistancePerPulse)
        self.encoder_r.setDistancePerPulse(constants.kDistancePerPulse)
        self.encoder_r.setReverseDirection(True)

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
        self.left_climber_motor.setInverted(True)
        self.right_climber_motor.setInverted(False)

        self.left_climber_motor.setIdleMode(rev.CANSparkMax.IdleMode.kBrake)
        self.right_climber_motor.setIdleMode(rev.CANSparkMax.IdleMode.kBrake)

        self.right_climber_sensor = wpilib.DigitalInput(4)
        self.left_climber_sensor = wpilib.DigitalInput(5)

    def teleopPeriodic(self):
        # # Use the joystick X axis for lateral movement, Y axis for forward
        twitch = twitch_range(self.stick.getRawAxis(3))

        if False:
            speed = -self.stick.getEnhY()
            rotation = -self.stick.getEnhTwist() * abs(twitch)
        else:
            speed = -squared(self.stick.getY())
            rotation = -squared(self.stick.getZ()) * abs(twitch)

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
        if self.stick.getRawButton(9):
            self.shooter.shootAmp()

        if self.stick.getRawButton(8):
            self.encoder_pid.enable()
            if self.encoder_pid.isAligned():
                self.shooter.shoot()

        if self.climb_stick.getRawButton(1):
            if self.drivetrain.noteAlign():
                self.floorintake.grab(True)

        if CLIMB_WITH_JOYSTICK:
            # Joystick based climber
            cy = self.climb_stick.getY()
            if self.climb_stick.getRawButton(11):
                self.left_climber.direct(cy)
            if self.climb_stick.getRawButton(12):
                self.right_climber.direct(-cy)
        else:
            ## left side
            if self.climb_stick.getRawButton(5):
                speed = self.climb_stick.getRawAxis(1)
                self.left_climber.direct(speed)

            ## right side
            if self.climb_stick.getRawButton(6):
                speed2 = self.climb_stick.getRawAxis(3)
                self.right_climber.direct(speed2)

    def robotPeriodic(self):
        super().robotPeriodic()
        if self.indexer.is_note_present():
            self.ll_led = 3
        else:
            self.ll_led = 1
