import rev
import magicbot

from robotpy_ext.common_drivers.distance_sensors import SharpIR2Y0A41


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

    upper_sensor: SharpIR2Y0A41
    lower_sensor: SharpIR2Y0A41

    floorintake_speed = magicbot.tunable(0.2)
    sourceintake_speed = magicbot.tunable(0.2)
    shooting_speed = magicbot.tunable(0.2)

    speed = magicbot.will_reset_to(0)

    #
    # Feedback method
    #

    @magicbot.feedback
    def is_note_present(self):
        if (
            self.upper_sensor.getDistance() < 10
            and self.lower_sensor.getDistance() < 10
        ):
            return True

        return False

    #
    # Actions methods
    #

    def floorIntake(self):
        if not self.is_note_present():
            self.speed = self.floorintake_speed

    def sourceIntake(self):
        if not self.is_note_present():
            self.speed = self.sourceintake_speed

    def shooting(self):
        self.speed = self.shooting_speed

    #
    # Execute methods
    #

    def execute(self):
        self.motor.set(self.speed)
