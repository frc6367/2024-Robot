import wpilib
import wpilib.drive
import phoenix5
import rev 


class MyRobot(wpilib.TimedRobot):
   

    # The channel on the driver station that the joystick is connected to
    kJoystickChannel0 = 0
    kJoystickChannel1 = 1

    # front_motorChannel = 5
    # back_motorChannel = 6


    right_motorChannel = 10
    left_motorChannel = 11
    blue_motorChannel = 0



    def robotInit(self):
        #self.motor = rev.CANSparkMax(20,rev.CANSparkLowLevel.MotorType.kBrushless)

        # self.front = phoenix5.WPI_VictorSPX(self.front_motorChannel)
        # self.back = phoenix5.WPI_VictorSPX(self.back_motorChannel)

        self.right = rev.CANSparkMax(self.right_motorChannel, rev.CANSparkMax.MotorType.kBrushless)
        self.left = rev.CANSparkMax(self.left_motorChannel, rev.CANSparkMax.MotorType.kBrushless)

        self.stick0 = wpilib.Joystick(self.kJoystickChannel0)
        self.stick1 = wpilib.Joystick(self.kJoystickChannel1)

    def teleopPeriodic(self):

        ##code for climber motor test 
        if self.stick0.getTrigger():
            self.right.set(self.stick0.getRawAxis(3))
        else: 
            self.right.set(0)

        if self.stick1.getTrigger():
            self.left.set(self.stick1.getRawAxis(3))
        else: 
            self.left.set(0)


        ##code for intake motor test 
        # if self.stick0.getTrigger():
        #     self.front.set(self.stick0.getRawAxis(3))
        # else:
        #     self.front.set(0)
        
        # if self.stick1.getTrigger():
        #     self.back.set(self.stick1.getRawAxis(3))
        # else:
        #     self.back.set(0)
            



