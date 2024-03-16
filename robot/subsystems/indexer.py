import rev
import magicbot

from robotpy_ext.common_drivers.distance_sensors import SharpIR2Y0A21
from misc.led_controller import LEDController


class Indexer:
    """
    actions
        floorIntake:
            motor rotates slowly
            slows down the note--> tries to put it in correct spot
        sourceIntake:
            motor rotates slowly
            slows down the note --> tries to put it in correct spot
        shooting:
            motor rotates fast
            speed up note
            holds note till its ready to shoot--> delay


    """

    led_controller: LEDController

    motor: rev.CANSparkMax

    upper_sensor: SharpIR2Y0A21
    lower_sensor: SharpIR2Y0A21

    floorintake_speed = magicbot.tunable(0.35)
    sourceintake_speed = magicbot.tunable(-0.2)
    shooting_speed = magicbot.tunable(1.0)
    shootBack_speed = magicbot.tunable(-0.1)
    reverse_speed = magicbot.tunable(-0.2)

    speed = magicbot.will_reset_to(0)

    #
    # Feedback method
    #

    @magicbot.feedback
    def is_note_present(self):
        if (
            self.upper_sensor.getDistance() < 20
            and self.lower_sensor.getDistance() < 20
        ):
            return True

        return False

    def is_lower_note_present(self):
        return self.lower_sensor.getDistance() < 20

    #
    # Actions methods
    #

    def floorIntake(self) -> bool:
        if not self.is_note_present():
            self.speed = self.floorintake_speed
            return True
        return False

    def sourceIntake(self) -> bool:
        if not self.is_note_present():
            self.speed = self.sourceintake_speed
            return True
        return False

    def shooting(self):
        self.speed = self.shooting_speed

    def shootBack(self):
        self.speed = self.shootBack_speed

    def reverse(self):
        self.speed = self.reverse_speed

    #
    # Execute methods
    #

    def execute(self):
        if self.is_note_present():
            self.led_controller.indicateHasNote()

        self.motor.set(self.speed)
