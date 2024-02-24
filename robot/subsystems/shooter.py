import magicbot
import rev
import wpilib
import phoenix5

from .indexer import Indexer

# from misc.led_controller import LEDController


class Shooter:
    """
    actions
        shoot:
            spin the motor
            delay

        intake:
            spin the motor (other way)

    """

    indexer: Indexer

    left_motor: phoenix5.WPI_VictorSPX
    right_motor: phoenix5.WPI_VictorSPX

    # led: LEDController
    # sensor: unknown

    shoot_speed = magicbot.tunable(0.5)

    speed = magicbot.will_reset_to(0)

    # Action methods
    def sourceIntake(self):
        pass

    ##indexer runs first, then motors r4un at full speed to shot the
    def shoot(self):
        self.right_motor = self.shoot_speed
        self.left_motor = self.shoot_speed

    def execute(self):
        pass
