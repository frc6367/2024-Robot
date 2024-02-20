 

import wpilib
import wpilib.drive
import phoenix5


class MyRobot(wpilib.TimedRobot):
   

    # The channel on the driver station that the joystick is connected to
    kJoystickChannel0 = 0
    kJoystickChannel1 = 1

    front_motorChannel = 5
    back_motorChannel = 6

    def robotInit(self):
        #self.motor = rev.CANSparkMax(20,rev.CANSparkLowLevel.MotorType.kBrushless)
        self.front = phoenix5.WPI_VictorSPX(self.front_motorChannel)
        self.back = phoenix5.WPI_VictorSPX(self.back_motorChannel)
        self.stick0 = wpilib.Joystick(self.kJoystickChannel0)
        self.stick1 = wpilib.Joystick(self.kJoystickChannel1)

    def teleopPeriodic(self):
        if self.stick0.getTrigger():
            self.front.set(self.stick0.getRawAxis(3))
        else:
            self.front.set(0)
        
        if self.stick1.getTrigger():
            self.back.set(self.stick1.getRawAxis(3))
        else:
            self.back.set(0)

