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

    @timed_state(first=True, duration=2, next_state="initial_back")
    def wait(self):
        pass

    @timed_state(duration=1.5, next_state="shoot")
    def initial_back(self):
        self.drivetrain.move(-0.25, 0.15 * self.direction)

    # @timed_state(duration=0.8, next_state="shoot")
    # def initial_back2(self):
    #     self.drivetrain.move(-03, -0.35 * self.direction)

    @timed_state(duration=2, next_state="goback1")
    def shoot(self):
        self.shooter.shoot()

    @timed_state(duration=1.75, next_state="goback2")
    def goback1(self):
        self.drivetrain.move(-0.3, -0.4 * self.direction)

    @timed_state(duration=3)
    def goback2(self):
        self.drivetrain.move(-0.3, 0)


class LeftSideAuto(AngleBase):
    MODE_NAME = "left"
    direction = -1
    DISABLED = False
    DEFAULT = True


class RightSideAuto(AngleBase):
    MODE_NAME = "right"
    direction = 1
    DISABLED = False
    DEFAULT = False
