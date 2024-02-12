"""
    This is a demo program showing how to use Mecanum control with the
    MecanumDrive class.
"""

import phoenix5
import wpilib
import wpilib.drive

from ntcore.util import ntproperty 

class MyRobot(wpilib.TimedRobot):
    # Channels on the roboRIO that the motor controllers are plugged in to
    kFrontLeftChannel = 2
    kRearLeftChannel = 3
    kFrontRightChannel = 6
    kRearRightChannel = 5

    # The channel on the driver station that the joystick is connected to
    kJoystickChannel0 = 0
    kJoystickChannel1 = 1

    kp = ntproperty("/kp",-0.1)
    tx = ntproperty("/limelight/tx", 0.0)

    def robotInit(self):
        self.frontLeft = phoenix5.WPI_VictorSPX(self.kFrontLeftChannel)
        self.rearLeft = phoenix5.WPI_VictorSPX(self.kRearLeftChannel)
        self.frontRight = phoenix5.WPI_VictorSPX(self.kFrontRightChannel)
        self.rearRight = phoenix5.WPI_VictorSPX(self.kRearRightChannel)

        # invert the right side motors
        # you may need to change or remove this to match your robot
        self.frontRight.setInverted(True)
        self.rearRight.setInverted(True)

        self.robotDrive = wpilib.drive.MecanumDrive(
            self.frontLeft, self.rearLeft, self.frontRight, self.rearRight
        )

        self.stick0 = wpilib.Joystick(self.kJoystickChannel0)
        self.stick1 = wpilib.Joystick(self.kJoystickChannel1)

    def teleopPeriodic(self):

        if self.stick0.getRawButton(9):
            heading_error = self.tx
            steering_adjust = self.kp * self.tx
            self.robotDrive.driveCartesian(
            -self.stick0.getY(),
            steering_adjust,
            self.stick1.getZ(),
        )
        else:
            # Use the joystick X axis for lateral movement, Y axis for forward
            # movement, and Z axis for rotation.
            self.robotDrive.driveCartesian(
                -self.stick0.getY(),
                -self.stick0.getX(),
                self.stick1.getZ(),
            )

