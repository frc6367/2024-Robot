# TODO: insert robot code here
"""
    This is a demo program showing how to use Mecanum control with the
    MecanumDrive class.
"""

import phoenix5
import wpilib
import wpilib.drive


class MyRobot(wpilib.TimedRobot):
    # Channels on the roboRIO that the motor controllers are plugged in to
    kFrontLeftChannel = 2
    kRearLeftChannel = 3
    kFrontRightChannel = 6
    kRearRightChannel = 5

    # The channel on the driver station that the joystick is connected to
    kJoystickChannel0 = 0
    kJoystickChannel1 = 1

    def robotInit(self):
        self.frontLeft = phoenix5.WPI_VictorSPX(self.kFrontLeftChannel)
        self.rearLeft = phoenix5.WPI_VictorSPX(self.kRearLeftChannel)
        self.frontRight = phoenix5.WPI_VictorSPX(self.kFrontRightChannel)
        self.rearRight = phoenix5.WPI_VictorSPX(self.kRearRightChannel)

        self.left = wpilib.MotorControllerGroup(self.frontLeft, self.rearLeft)
        self.right = wpilib.MotorControllerGroup(self.frontRight, self.rearRight)

        # invert the right side motors
        # you may need to change or remove this to match your robot
        self.frontRight.setInverted(True)
        self.rearRight.setInverted(True)

        self.robotDrive = wpilib.drive.DifferentialDrive(
            self.left, self.right
        )

        self.stick0 = wpilib.Joystick(self.kJoystickChannel0)

    def teleopPeriodic(self):
        # Use the joystick X axis for lateral movement, Y axis for forward
        # movement, and Z axis for rotation.
        self.robotDrive.arcadeDrive(
            -self.stick0.getY(),
            -self.stick0.getTwist()
        )

