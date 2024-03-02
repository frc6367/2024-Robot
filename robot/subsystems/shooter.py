import enum
import magicbot
import rev
import wpilib
import phoenix5

from .indexer import Indexer

# from misc.led_controller import LEDController


class Action(enum.Enum):
    NONE = 1
    SHOOT = 2
    SOURCE = 3


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
    reverse_speed = magicbot.tunable(-0.5)

    action = magicbot.will_reset_to(Action.NONE)

    # Action methods
    def sourceIntake(self):
        self.action = Action.SOURCE
        pass

    ##indexer runs first, then motors run at full speed to shot the node
    def shoot(self):
        self.action = Action.SHOOT

    # def shoot(self):
    #     self.right_motor = self.shoot_speed
    #     self.left_motor = self.shoot_speed

    def execute(self):
        if self.action == Action.SOURCE:
            zspeed = -self.shoot_speed
            self.indexer.sourceIntake()

        elif self.action == Action.SHOOT:
            self.indexer.shooting()
            zspeed = self.shoot_speed
        else:
            zspeed = 0

        self.left_motor.set(zspeed)
        self.right_motor.set(zspeed)
