 

import rev
import wpilib
import wpilib.drive


class MyRobot(wpilib.TimedRobot):
   

    # The channel on the driver station that the joystick is connected to
    kJoystickChannel0 = 0
    kJoystickChannel1 = 1

    def robotInit(self):
        self.motor = rev.CANSparkMax(20,rev.CANSparkLowLevel.MotorType.kBrushless)

        self.stick0 = wpilib.Joystick(self.kJoystickChannel0)

    def teleopPeriodic(self):
        if self.stick0.getTrigger():
            self.motor.set(self.stick0.getZ())
        else:
            self.motor.set(0)

