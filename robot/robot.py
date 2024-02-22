import wpilib
import wpilib.drive
# from misc.ejoystick import EnhancedJoystick

import magicbot
import phoenix5

# import navx
import rev
from wpimath.filter import SlewRateLimiter

# from misc.led_controller import LEDController

from subsystems.climber import Climber
from subsystems.drivetrain import DriveTrain
from subsystems.intake import Intake
from subsystems.shooter import Shooter
# from misc.sparksim import CANSparkMax


# def map_range(x, a, b, c, d):
#     y = (x - a) / (b - a) * (d - c) + c
#     return y


# def twitch_range(y):
#     return map_range(y, -1.0, 1.0, 0.5, 0.25)


class MyRobot(wpilib.TimedRobot):
    intake: Intake
    drivetrain: DriveTrain
    climber: Climber 
    shooter: Shooter


    # ##Joysticks    
    # # The channel on the driver station that the joystick is connected to
    kJoystickChannel0 = 0
    kJoystickChannel1 = 1
    stick0 = wpilib.Joystick(kJoystickChannel0)
    stick1 = wpilib.Joystick(kJoystickChannel1)


    def createObjects(self):
        # Joysticks
        # self.speed_limiter = SlewRateLimiter(3)
        # self.twist_limiter = SlewRateLimiter(0.5)
        # self.stick0 = wpilib.Joystick(self.kJoystickChannel0)
        # self.stick1 = wpilib.Joystick(self.kJoystickChannel1)


        ##Drivetrain 
        self.drive_l1 = phoenix5.WPI_VictorSPX(4)
        self.drive_l2 = phoenix5.WPI_VictorSPX(3)
        self.drive_r1 = phoenix5.WPI_VictorSPX(1)
        self.drive_r2 = phoenix5.WPI_VictorSPX(2)

        self.drive_r1.setInverted(True)
        self.drive_r2.setInverted(True)

        ## intake
        self.front_motor = phoenix5.WPI_VictorSPX(7)
        self.back_motor = phoenix5.WPI_VictorSPX(8)

        ## shooter 
        self.left_motor = phoenix5.WPI_VictorSPX(5)
        self.right_motor = phoenix5.WPI_VictorSPX(6)

        ## index --> within shooter class
        self.indexer_motor = rev.CANSparkMax(9, rev.CANSparkMax.MotorType.kBrushless)

        ## climber
        self.right_arm_motor = rev.CANSparkMax(10, rev.CANSparkMax.MotorType.kBrushless)
        self.left_arm_motor = rev.CANSparkMax(11, rev.CANSparkMax.MotorType.kBrushless)


        
    def teleopPeriodic(self):
        # # Use the joystick X axis for lateral movement, Y axis for forward
        # # movement, and Z axis for rotation.
        # self.drivetrain.move(
        #     -self.stick0.getY(),
        #     -self.stick0.getTwist()n
        # )
     
        ## grabs the node 
        if self.stick0.getRawButton(5):
            self.intake.grab()
        ## moves indexer up when node taken from ground 
        if self.stick0.getRawButton(6):
            self.shooter.postioning_up()

        ##moves the indexer down when node taken from source 
        if self.stick0.getRawButton(7):
            self.shooter.postioning_down()

        ## shoots the node 
        if self.stick0.getRawButton(8):
            self.shooter.shoot()

        #extends the right arm of the climber
        if self.stick0.getRawButton(9):
            self.climber.right_climb()
            
        #retracts the right arm of the climber
        if self.stick0.getRawButton(10):
            self.climber.right_retracting()


        






         







