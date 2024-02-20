import magicbot 
import rev
import wpilib


class Climber: 
    motor: rev.CANSparkMax
    led: LEDController

    #
    # Action methods
    #
    def climb(self): 
        pass