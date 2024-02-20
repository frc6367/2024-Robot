import magicbot 
import rev
import wpilib
import phoenix5


class Intake: 
    front_motor: phoenix5.WPI_VictorSPX
    back_motor: phoenix5.WPI_VictorSPX
    

    #
    # Action methods
    grab_open_speed = magicbot.tunable(0.2)
    speed = magicbot.will_reset_to(0)

    def grab(self): 
        self.speed = self.grab_open_speed
    
    #
    # Execute
    #
    def execute(self):
        pass


    

