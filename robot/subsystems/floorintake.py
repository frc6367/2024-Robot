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

    green_motor: phoenix5.WPI_TalonSRX
    black_motor: phoenix5.WPI_TalonSRX
    # sensor: unknown

    black_grab_speed = magicbot.tunable(0.4)
    green_grab_speed = magicbot.tunable(0.8)

    action = magicbot.will_reset_to(Action.NONE)

    def setup(self):
        self.timer = wpilib.Timer()
        self.continue_grab = False
        self.continuing_grab = False

        self.last_action = Action.NONE

    #
    # Action methods
    #

    def grab(self, continue_grab: bool = False):
        self.action = Action.GRAB
        self.continue_grab = continue_grab

    def reverse(self):
        self.action = Action.REVERSE

    #
    # Execute
    #

    def execute(self):

        bspeed = 0
        gspeed = 0

        if self.action == Action.NONE:
            if self.continue_grab and self.last_action != self.action:
                self.timer.restart()
                self.continue_grab = False
                self.continuing_grab = True

            if self.continuing_grab:
                if self.timer.get() < 2:
                    self.action = Action.GRAB
                else:
                    self.continuing_grab = False
        else:
            self.continuing_grab = False

        if self.action == Action.GRAB:
            if self.indexer.floorIntake():
                bspeed = self.black_grab_speed
                gspeed = self.green_grab_speed

        elif self.action == Action.REVERSE:
            bspeed = -self.black_grab_speed
            gspeed = -self.green_grab_speed
            self.indexer.reverse()
            self.continue_grab = False

        self.black_motor.set(bspeed)
        self.green_motor.set(gspeed)
        self.last_action = self.action
