import wpilib

from magicbot import AutonomousStateMachine, timed_state, state
from subsystems.drivetrain import DriveTrain
from subsystems.floorintake import FloorIntake
from subsystems.shooter import Shooter
from subsystems.indexer import Indexer
from navx import AHRS


class AngleBase(AutonomousStateMachine):

    DISABLED = True

    floorintake: FloorIntake
    drivetrain: DriveTrain
    shooter: Shooter
    indexer: Indexer

    direction = 1

    ## sensor needs to be added for robot to be the right distance away from the speaker
    ## back up first 2ft 4 in(make sure right distance with sensor), and then shoot

    @timed_state(first=True, duration=5, next_state="initial_back")
    def wait(self):
        pass

    @timed_state(duration=0.2, next_state="initial_back2")
    def initial_back(self):
        self.drivetrain.move(-0.2, 0.0)

    @timed_state(duration=0.8, next_state="shoot")
    def initial_back2(self):
        self.drivetrain.move(-0.3, -0.35 * self.direction)

    @timed_state(duration=2, next_state="goback")
    def shoot(self):
        self.shooter.shoot()

    @timed_state(duration=4)
    def goback(self):
        self.drivetrain.move(-0.3, -0.3 * self.direction)


class LeftSideAuto(AngleBase):
    MODE_NAME = "amp side-left"
    direction = -1
    DISABLED = False
    DEFAULT = True


class RightSideAuto(AngleBase):
    MODE_NAME = "source side-right"
    direction = 1
    DISABLED = False
    DEFAULT = False
