import wpilib

from magicbot import AutonomousStateMachine, timed_state, state
from subsystems.drivetrain import DriveTrain
from subsystems.floorintake import FloorIntake
from subsystems.shooter import Shooter
from subsystems.indexer import Indexer


class Scoring(AutonomousStateMachine):
    floorintake: FloorIntake
    drivetrain: DriveTrain
    shooter: Shooter
    indexer: Indexer

    @timed_state(first=True, duration=3, next_state="shoot")
    def move_forward(self):
        self.drivetrain.move(0.2, 0)

    @timed_state(duration=1.1, next_state="pick_up")
    def shoot(self):
        self.shoot()
    
    @timed_state(duration=1.1, next_state="position")
    def pick_up(self):
        pass

    @state
    def position(self):
        pass


    



        # if self.level == "MID":
        #     self.arm.gotoMiddle()
        # else:
        #     self.arm.gotoMiddle2()
        # if self.arm.getPosition() == self.level:
        #     self.next_state(self.move_forward)

    # @timed_state(duration=1.1, next_state="release_grabber")
    # def move_forward(self):
    #     if self.level == "MID2":
    #         self.next_state_now(self.move_forward_less)
    #         return

    #     self.drivetrain.move(0.2, 0)

    # @timed_state(duration=1, next_state="release_grabber")
    # def move_forward_less(self):
    #     self.drivetrain.move(0.2, 0)
