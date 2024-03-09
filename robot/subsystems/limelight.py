import magicbot
import wpilib
from subsystems.shooter import Shooter
from subsystems.indexer import Indexer
from subsystems.drivetrain import DriveTrain
from ntcore.util import ntproperty 
import enum


class Action(enum.Enum):
    NONE = 1
    ALIGN = 2
    SHOOT = 3
    AMP = 4 


class AmpShoot:
    shooter: Shooter
    indexer: Indexer
    drivetrain: DriveTrain
    kp = ntproperty("/kp",-0.1)
    tx = ntproperty("/limelight/tx", 0.0)

    speed = magicbot.will_reset_to(0)
    action = magicbot.will_reset_to(Action.NONE)

    timer = wpilib.Timer()
    delay = magicbot.tunable(0.5)

    def __init__(self):
        self.switch = False 
        self.timer.reset()
        self.timer.start()


    #
    # Action methods
    #


    def align(self):
        self.action = Action.ALIGN

    def shoot(self):
        self.action = Action.SHOOT
 
    def amp(self):
        self.action = Action.AMP


     #
    # Execute
    #

      
    def execute(self):
        if self.action == Action.ALIGN:
            self.switch = False
            heading_error = self.tx
            steering_adjust = self.kp * self.tx
            self.drivetrain.move(self.speed,steering_adjust)
        # elif self.action == Action.SHOOT:
        #     if not self.switch:
        #         self.switch = True
        #         self.timer.reset()
        #         self.timer.start()

        #     if self.timer.get() > self.delay:
        #         self.shooter.shoot()
        # else: 
        #     self.is_shooting = False






