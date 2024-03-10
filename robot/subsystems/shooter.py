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
    SHOOTAMP = 3
    SOURCE = 4


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

    shoot_speed = magicbot.tunable(1)
    shoot_amp_speed = magicbot.tunable(0.3)
    source_speed = magicbot.tunable(-0.5)

    speed = magicbot.will_reset_to(0)
    action = magicbot.will_reset_to(Action.NONE)

    timer = wpilib.Timer()
    delay = magicbot.tunable(0.8)
    force_shoot = magicbot.tunable(2)

    def __init__(self):
        self.is_shooting = False
        self.timer.reset()
        self.timer.start()

    # Action methods
    def sourceIntake(self):
        self.action = Action.SOURCE

    ##indexer runs first, then motors run at full speed to shot the node
    def shoot(self):
        self.action = Action.SHOOT

    def shootAmp(self):
        self.action = Action.SHOOTAMP

    def execute(self):
        zspeed = 0

        tm = self.timer.get()
        if self.is_shooting == True and self.delay > tm and self.delay + self.force_shoot < tm:
            self.action = Action.SHOOT


        if self.action == Action.SOURCE:
            self.is_shooting = False

            if self.indexer.sourceIntake():
                zspeed = self.source_speed

        elif self.action == Action.SHOOT:
            zspeed = self.shoot_speed
            if not self.is_shooting:
                self.is_shooting = True
                self.timer.reset()
                self.timer.start()
                tm = 0
            if tm > self.delay:
                self.indexer.shooting()
            else:
                self.indexer.shootBack()

        elif self.action == Action.SHOOTAMP:
            zspeed = self.shoot_amp_speed
            if not self.is_shooting:
                self.is_shooting = True
                self.timer.reset()
                self.timer.start()
                tm = 0
            if tm > self.delay:
                self.indexer.shooting()

        else:

            self.is_shooting = False

        self.left_motor.set(zspeed)
        self.right_motor.set(-zspeed)

        wpilib.SmartDashboard.putNumber("zspeed", zspeed)
