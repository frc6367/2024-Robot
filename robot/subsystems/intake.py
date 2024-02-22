import magicbot 
import rev
import wpilib
import phoenix5


class Intake: 
    front_motor: phoenix5.WPI_VictorSPX
    back_motor: phoenix5.WPI_VictorSPX
    # sensor: unknown 

    #
    # Action methods
    back_grab_speed = magicbot.tunable(0.4)
    front_grab_speed = magicbot.tunable(0.2)
    speed = magicbot.will_reset_to(0)

    ## front motor runs faster than the back motor 
    ## the motor should stop moving when sensor senses node  
    def grab(self): 
        self.front_motor = self.front_grab_speed
        self.back_motor = self.back_grab_speed
    
    #
    # Execute
    #
    def execute(self):
        pass


    

