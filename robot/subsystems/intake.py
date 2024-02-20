import magicbot 
import rev
import wpilib

class Intake: 
    front_motor: rev.CANSparkMax
    back_motor: rev.CANSparkMax

    #
    # Action methods

    speed = magicbot.will_reset_to(0)
    def grab(self): 
        pass

    

