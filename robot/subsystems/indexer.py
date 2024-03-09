import rev
import magicbot

from robotpy_ext.common_drivers.distance_sensors import SharpIR2Y0A21


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

    motor: rev.CANSparkMax

    upper_sensor: SharpIR2Y0A21
    lower_sensor: SharpIR2Y0A21

    floorintake_speed = magicbot.tunable(0.35)
    sourceintake_speed = magicbot.tunable(-0.2)
    shooting_speed = magicbot.tunable(1.0)
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

    def reverse(self):
        self.speed = self.reverse_speed

    #
    # Execute methods
    #

    def execute(self):
        self.motor.set(self.speed)
