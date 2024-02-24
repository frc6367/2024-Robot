import magicbot
import rev


class Climber:
    """ """

    right_motor: rev.CANSparkMax
    left_motor: rev.CANSparkMax

    climb_speed = magicbot.tunable(0.2)
    retracting_speed = magicbot.tunable(-0.2)

    left_speed = magicbot.will_reset_to(0)
    right_speed = magicbot.will_reset_to(0)

    #
    # Action methods
    #
    def right_climb(self):
        self.right_speed = self.climb_speed

    def left_climb(self):
        self.left_speed = self.climb_speed

    def right_retracting(self):
        self.right_speed = self.retracting_speed

    def left_retracting(self):
        self.left_speed = self.retracting_speed

    #
    # Execute
    #
    def execute(self):
        self.right_motor.set(self.right_speed)
        self.left_motor.set(self.left_speed)
