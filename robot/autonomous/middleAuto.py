import wpilib

from magicbot import AutonomousStateMachine, timed_state, state
from subsystems.drivetrain import DriveTrain
from subsystems.floorintake import FloorIntake
from subsystems.shooter import Shooter
from subsystems.indexer import Indexer
from navx import AHRS


class Middle(AutonomousStateMachine):

    MODE_NAME = "Middle"
    DEFAULT = False

    floorintake: FloorIntake
    drivetrain: DriveTrain
    shooter: Shooter
    indexer: Indexer

    ## sensor needs to be added for robot to be the right distance away from the speaker
    ## back up first 2ft 4 in(make sure right distance with sensor), and then shoot

    @timed_state(first=True, duration=1.75, next_state="shoot")
    def initial_back(self):
        self.drivetrain.move(-0.2, 0)

    @timed_state(duration=2, next_state="goback")
    def shoot(self):
        self.shooter.shoot()

    @timed_state(duration=2.1, next_state="goForward")
    def goback(self):
        self.drivetrain.move(-0.3, 0)
        self.floorintake.grab()

        if self.indexer.is_note_present() == True:
            self.next_state_now("goForward")

    @timed_state(duration=6, next_state="go_back_again")
    def goForward(self):
        self.drivetrain.move(0.3, 0)

    @timed_state(duration=0.7, next_state="shoot2")
    def go_back_again(self):
        self.drivetrain.move(-0.2, 0)

    @timed_state(duration=2)
    def shoot2(self):
        self.shooter.shoot()
