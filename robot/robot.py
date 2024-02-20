import wpilib
import magicbot
import phoenix5

# import navx
import rev

from misc.led_controller import LEDController

from subsystems.climber import Climber
from subsystems.drivetrain import DriveTrain
from subsystems.intake import Intake
from subsystems.shooter import Shooter
from misc.sparksim import CANSparkMax


class MyRobot(wpilib.TimedRobot):
    intake: Intake
    drivetrain: DriveTrain
    climber: Climber 
    shooter: Shooter

    ##Joysticks    
    # The channel on the driver station that the joystick is connected to
    kJoystickChannel0 = 0
    kJoystickChannel1 = 1

    def createObjects(self):

        ##Drivetrain 
        self.frontLeft = phoenix5.WPI_VictorSPX(4)
        self.rearLeft = phoenix5.WPI_VictorSPX(3)
        self.frontRight = phoenix5.WPI_VictorSPX(1)
        self.rearRight = phoenix5.WPI_VictorSPX(2)
        
        self.frontRight.setInverted(True)
        self.rearRight.setInverted(True)

        ## intake
        self.front_motor = phoenix5.WPI_VictorSPX(7)
        self.back_motor = phoenix5.WPI_VictorSPX(8)

        ## shooter 
        self.left_motor = phoenix5.WPI_VictorSPX(5)
        self.right_motor = phoenix5.WPI_VictorSPX(6)

        ## index 
        self.indexer_motor = CANSparkMax(9, CANSparkMax.MotorType.kBrushless)

        ## climber
        self.right_arm_motor = CANSparkMax(10, CANSparkMax.MotorType.kBrushless)
        self.left_arm_motor = CANSparkMax(11, CANSparkMax.MotorType.kBrushless)

        self.stick0 = wpilib.Joystick(self.kJoystickChannel0)
        self.stick1 = wpilib.Joystick(self.kJoystickChannel1)
        
    def teleopPeriodic(self):
        # Use the joystick X axis for lateral movement, Y axis for forward
        # movement, and Z axis for rotation.
        self.robotDrive.arcadeDrive(
            -self.stick0.getY(),
            -self.stick0.getTwist()
        )
        ## grabs the node into the robot 
        if self.stick0.getRawButton(6):
            self.intake.grab()

        ## shoots the node 
        if self.stick0.getRawButton(7):
            self.shooter.shoot()

        ##postions the node when the robot collects the node from the source 
        if self.stick0.getRawButton(8):
            self.shooter()












        # if self.stick0.getTrigger():
        #     self.front_motor.set(self.stick0.getRawAxis(3))
        # else:
        #     self.front_motor.set(0)
        
        # if self.stick1.getTrigger():
        #     self.back_motor.set(self.stick1.getRawAxis(3))
        # else:
        #     self.back_motor.set(0)


        






         







