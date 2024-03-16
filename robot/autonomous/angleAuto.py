import wpilib

from magicbot import AutonomousStateMachine, timed_state, state
from subsystems.drivetrain import DriveTrain, EncoderPID, NavxPID
from subsystems.floorintake import FloorIntake
from subsystems.shooter import Shooter
from subsystems.indexer import Indexer
from navx import AHRS


class AngleBase(AutonomousStateMachine):

    DISABLED = True

    encoder_pid: EncoderPID
    navx_pid: NavxPID

    floorintake: FloorIntake
    drivetrain: DriveTrain
    shooter: Shooter
    indexer: Indexer

    # don't change these, do in the auto instead
    initial_shot_angle = 0
    goback_backward_angle = 0
    second_shot_angle = 0

    ## sensor needs to be added for robot to be the right distance away from the speaker
    ## back up first 2ft 4 in(make sure right distance with sensor), and then shoot

    @timed_state(first=True, duration=0.5, next_state="initial_back")
    def wait(self):
        pass

    @timed_state(duration=2, next_state="shoot")
    def initial_back(self):
        # self.drivetrain.move(-0.25, 0.15 * self.direction)
        self.encoder_pid.enable()
        self.navx_pid.enable(self.initial_shot_angle)
        # if self.encoder_pid.isAligned():
        # self.next_state(self.shoot)

    # @timed_state(duration=0.8, next_state="shoot")
    # def initial_back2(self):
    #     self.drivetrain.move(-03, -0.35 * self.direction)

    @timed_state(duration=2, next_state="rotate")
    def shoot(self):
        self.encoder_pid.enable()
        self.navx_pid.enable(self.initial_shot_angle)
        self.shooter.shoot()

    @timed_state(duration=1, next_state="goback")
    def rotate(self):
        self.navx_pid.enable(self.goback_backward_angle)

    @timed_state(duration=3, next_state="goForward")
    def goback(self):
        # self.drivetrain.move(-0.3, -0.4 * self.direction)/
        self.navx_pid.enable(self.goback_backward_angle)
        self.drivetrain.move(-0.3, 0)
        # self.drivetrain.noteAlign()
        self.floorintake.grab()
        if self.indexer.is_note_present() == True:
            self.next_state_now("goForward")

    @timed_state(duration=4, next_state="go_back_again")
    def goForward(self):
        self.navx_pid.enable(self.second_shot_angle)
        self.drivetrain.move(0.3, 0)
        self.floorintake.grab()

    @timed_state(duration=2, next_state="shoot2")
    def go_back_again(self):
        # self.drivetrain.move(-0.2, 0)
        self.navx_pid.enable(self.second_shot_angle)
        self.encoder_pid.enable()
        if self.encoder_pid.isAligned():
            self.next_state(self.shoot2)

    @timed_state(duration=2)
    def shoot2(self):
        self.encoder_pid.enable()
        self.shooter.shoot()


class LeftSideAuto(AngleBase):
    MODE_NAME = "left"
    direction = -1

    DISABLED = False
    DEFAULT = True

    initial_shot_angle = 10
    goback_backward_angle = -60
    second_shot_angle = -30


class RightSideAuto(AngleBase):
    MODE_NAME = "right"
    direction = 1

    DISABLED = False
    DEFAULT = False

    initial_shot_angle = 5
    goback_backward_angle = 60
    second_shot_angle = 40
