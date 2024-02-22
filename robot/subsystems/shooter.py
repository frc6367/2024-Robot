import magicbot 
import rev
import wpilib
import phoenix5

# from misc.led_controller import LEDController

class Shooter: 
    left_motor: phoenix5.WPI_VictorSPX
    right_motor: phoenix5.WPI_VictorSPX
    indexer_motor: rev.CANSparkMax
    # led: LEDController
    # sensor: unknown 
    
    shoot_speed = magicbot.tunable(0.2)
    
    pulling_in_speed = magicbot.tunable(-0.2)
    indexer_down_pos_speed = magicbot.tunable(-0.2)
    indexer_up_pos_speed = magicbot.tunable(0.4)

    speed = magicbot.will_reset_to(0)

    
    def setup(self):
        self.left_motor.setInverted(True)

    #
    # Action methods
        

    ##indexer runs first, then motors r4un at full speed to shot the
    def shoot(self):
        self.right_motor = self.shoot_speed
        self.left_motor = self.shoot_speed

    #### indexer 
    ##when the node comes from the ground 
        ##need a sensor to tell where the node is
        ## if node is close, indexer moves node up 
    def postioning_up(self):
        self.indexer_motor = self.indexer_up_pos_speed

    ##when the node comes from the source and needs to be moved lower  
        ##speed = neg to run motors backwards 
    def postioning_down(self):
        self.right_motor = self.pulling_in_speed
        self.left_motor = self.pulling_in_speed
        self.indexer_motor =  self.indexer_down_pos_speed

    def execute(self):
        pass