import magicbot 
import rev
import wpilib
import ctre
from misc.led_controller import LEDController

class Shooter: 
    left_motor: ctre.WPI_TalonSRX
    right_motor: ctre.WPI_TalonSRX
    indexer_motor: rev.CANSparkMax
    led: LEDController
    
    grab_close_speed = magicbot.tunable(0.2)
    
    pulling_in_speed = magicbot.tunable(-0.2)
    indexer_down_pos_speed = magicbot.tunable(-0.2)
    indexer_up_pos_speed = magicbot.tunable(0.4)

    speed = magicbot.will_reset_to(0)

    #
    # Action methods
    #
    def shoot(self): 
        self.speed = self.grab_close_speed

    ##when the node comes from the source and needs to be moved lower 
    ## slow speed 
    ## indexer 
    def postioning_up(self):
        self.speed = self.indexer_up_pos_speed

    def postioning_down(self):
        self.speed =  self.indexer_down_pos_speed

    def execute(self):

        pass