import magicbot
import rev
import wpilib


class Climber:
    """ """

    motor: rev.CANSparkMax
    sensor: wpilib.DigitalInput

    climb_speed = magicbot.tunable(0.2)
    retracting_speed = magicbot.tunable(-0.2)

    speed = magicbot.will_reset_to(0.0)

    def __init__(self) -> None:
        self.last_direction = False

    #
    # Action methods
    #
    def climb(self):
        self.speed = self.climb_speed

    def retracting(self):
        self.speed = self.retracting_speed

    def direct(self, speed: float):
        self.speed = speed

    ## feedback

    @magicbot.feedback
    def is_retracted(self):
        return self.sensor.get() == False

    #
    # Execute
    #
    def execute(self):
        speed = self.speed
        if abs(speed) < 0.1:
            speed = 0
        else:
            direction = True if speed < 0 else False

            if self.is_retracted():
                if self.last_direction == direction:
                    speed = 0
            else:
                self.last_direction = direction

        self.motor.set(speed)
