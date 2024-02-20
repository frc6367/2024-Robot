import magicbot 
import rev
import wpilib
from misc.led_controller import LEDController


class Climber: 
    right_arm_motor: rev.CANSparkMax
    left_arm_motor: rev.CANSparkMax
    led: LEDController


    climb_speed = magicbot.tunable(0.2)
    
    retracting_speed = magicbot.tunable(-0.2)

    speed = magicbot.will_reset_to(0)


    #
    # Action methods
    #
    def climb(self): 
        self.speed = self.climb_speed
        
    def retracting(self):
        self.speed = self.retracting_speed

    
