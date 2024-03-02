import enum

import magicbot
import rev
import wpilib
import phoenix5


from .indexer import Indexer


class Action(enum.Enum):
    NONE = 1
    GRAB = 2
    REVERSE = 3


class FloorIntake:
    """
    actions
        intake:
            spin the motor
    """

    indexer: Indexer

    green_motor:phoenix5.WPI_TalonSRX
    black_motor:phoenix5.WPI_TalonSRX
    # sensor: unknown

    black_grab_speed = magicbot.tunable(0.4)
    green_grab_speed = magicbot.tunable(0.2)

    action = magicbot.will_reset_to(Action.NONE)

    #
    # Action methods
    #

    def grab(self):
        self.action = Action.GRAB

    def reverse(self):
        self.action = Action.REVERSE

    #
    # Execute
    #

    def execute(self):

        ## front motor runs faster than the back motor
        ## the motor should stop moving when sensor senses node

        if self.action == Action.GRAB:
            bspeed = self.black_grab_speed
            gspeed = self.green_grab_speed
            self.indexer.floorIntake()

        elif self.action == Action.REVERSE:
            bspeed = -self.black_grab_speed
            gspeed = -self.green_grab_speed
        else:
            bspeed = 0
            gspeed = 0

        self.black_motor.set(bspeed)
        self.green_motor.set(gspeed)
