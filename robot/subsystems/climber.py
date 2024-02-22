import magicbot 
import rev
import wpilib
# from misc.led_controller import LEDController


class Climber: 
    right_arm_motor: rev.CANSparkMax
    left_arm_motor: rev.CANSparkMax
    # led: LEDController


    climb_speed = magicbot.tunable(0.2)
    
    retracting_speed = magicbot.tunable(-0.2)

    speed = magicbot.will_reset_to(0)

    #
    # Action methods
    #
    def right_climb(self): 
        self.right_arm_motor = self.climb_speed

    def left_climb(self): 
        self.left_arm_motor = self.climb_speed
        
    def right_retracting(self):
        self.right_arm_motor= self.retracting_speed

    def left_retracting(self):
        self.left_arm_motor = self.retracting_speed
        


    
