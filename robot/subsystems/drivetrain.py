import wpilib.drive
import phoenix5
import magicbot
from robotpy_ext.common_drivers.distance_sensors import SharpIR2Y0A21
import wpilib


class DriveTrain:
    sensor: SharpIR2Y0A21
    drive_l1: phoenix5.WPI_TalonSRX
    drive_l2: phoenix5.WPI_TalonSRX
    drive_r1: phoenix5.WPI_TalonSRX
    drive_r2: phoenix5.WPI_TalonSRX

    encoder_l: wpilib.Encoder
    encorder_r: wpilib.Encoder

    speed = magicbot.will_reset_to(0)
    rotation = magicbot.will_reset_to(0)
    limit = magicbot.will_reset_to(1.0)

    l = magicbot.will_reset_to(0.0)
    r = magicbot.will_reset_to(0.0)
    tank = magicbot.will_reset_to(False)

    lv = magicbot.will_reset_to(0.0)
    rv = magicbot.will_reset_to(0.0)
    volts = magicbot.will_reset_to(False)

    def setup(self):
        self.drive_l2.follow(self.drive_l1)
        self.drive_r2.follow(self.drive_r1)

        self.drive = wpilib.drive.DifferentialDrive(self.drive_l1, self.drive_r1)

    def limit_speed(self):
        self.limit = 0.25

    def move(self, speed: float, rotation: float):
        self.speed = speed
        self.rotation = rotation

    def tank_drive(self, l: float, r: float):
        self.tank = True
        self.l = l
        self.r = r

    def volt_drive(self, lv: float, rv: float):
        self.volts = True
        self.lv = lv
        self.rv = rv

    def rotate(self, rotation: float):
        self.rotation = rotation

    # @magicbot.feedback
    # def distance(self):
    #     return self.sensor.getDistance()

    # @magicbot.feedback
    # def isObjectSensed(self):
    #     return self.distance() <= 70

    # heading_error = self.tx
    # steering_adjust = self.kp * self.tx
    # self.drivetrain.move(self.speed,steering_adjust)

    ##adjust the forawrd and back speed of the robot based on thew error

    # @magicbot.feedback
    def right_pos(self):
        pass

    def backAlign(self):
        self.doBackAlign = True
        pass

    def execute(self):
        if self.tank:
            self.drive.tankDrive(self.l, self.r)
        elif self.volts:
            self.drive.feed()
            self.drive_l1.setVoltage(self.lv)
            self.drive_r1.setVoltage(self.rv)
        else:
            self.drive.arcadeDrive(
                self.speed * self.limit, self.rotation * self.limit, False
            )

        # if self.doBackAlign == True:
        #     self.move(-0.3,0)
