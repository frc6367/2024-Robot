import wpilib

from magicbot import AutonomousStateMachine, timed_state, state
from subsystems.drivetrain import DriveTrain
from subsystems.floorintake import FloorIntake
from subsystems.shooter import Shooter
from subsystems.indexer import Indexer


class Right(AutonomousStateMachine):
    floorintake: FloorIntake
    drivetrain: DriveTrain
    shooter: Shooter
    indexer: Indexer

    # @timed_state(first=True, duration=3,)
    # def turn(self):
    #     self.drivetrain.move(0, 0.2 * -1)

    @timed_state(first=True, duration=3, next_state="shoot")
    def align(self):
        self.drivetrain.move(-0.2, 0)
        self.drivetrain.move(0, 0.2 * -1)
        self.drivetrain.move(0.2, 0)

    @timed_state(duration=1.1, next_state="pick_up")
    def shoot(self):
        self.shooter.shootAmp()

    @timed_state(duration=2.1)
    def pick_up(self):
        self.drivetrain.move(-0.1, 0)
        self.drivetrain.move(-0, 0.2 * 1)
        self.drivetrain.move(0.1, 0)
        self.floorintake.grab()
