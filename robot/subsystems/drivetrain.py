import wpilib.drive
import phoenix5
import magicbot
from robotpy_ext.common_drivers.distance_sensors import SharpIR2Y0A21
import wpilib
from wpilib import Timer
from ntcore.util import ntproperty


class DriveTrain:
    sensor: SharpIR2Y0A21
    drive_l1: phoenix5.WPI_TalonSRX
    drive_l2: phoenix5.WPI_TalonSRX
    drive_r1: phoenix5.WPI_TalonSRX
    drive_r2: phoenix5.WPI_TalonSRX

    encoder_l: wpilib.Encoder
    encoder_r: wpilib.Encoder

    speed = magicbot.will_reset_to(0)
    rotation = magicbot.will_reset_to(0)
    extra_rotation = magicbot.will_reset_to(0)
    limit = magicbot.will_reset_to(1.0)

    l = magicbot.will_reset_to(0.0)
    r = magicbot.will_reset_to(0.0)
    tank = magicbot.will_reset_to(False)

    lv = magicbot.will_reset_to(0.0)
    rv = magicbot.will_reset_to(0.0)
    volts = magicbot.will_reset_to(False)

    offset = magicbot.tunable(-0.4)
    maxOutput = magicbot.tunable(0.5)

    wantTo = magicbot.will_reset_to(False)
    kP = magicbot.tunable(3.0)
    iLimit = 1

    tx = ntproperty("/limelight/tx", 0.0)
    tclass = ntproperty("/limelight/tclass", "")
    kpturn = magicbot.tunable(-0.1)
    maxAdjustment = magicbot.tunable(0.3)

    setpoint = 0
    errorSum = 0
    lastTimestamp = 0
    lastError = 0

    def setup(self):
        self.drive_l2.follow(self.drive_l1)
        self.drive_r2.follow(self.drive_r1)

        self.drive = wpilib.drive.DifferentialDrive(self.drive_l1, self.drive_r1)

        self.doingIt = False

    def limit_speed(self):
        self.limit = 0.25

    def move(self, speed: float, rotation: float):
        self.speed = speed
        self.rotation = rotation

    # def tank_drive(self, l: float, r: float):
    #     self.tank = True
    #     self.l = l
    #     self.r = r

    # def volt_drive(self, lv: float, rv: float):
    #     self.volts = True
    #     self.lv = lv
    #     self.rv = rv

    def rotate(self, rotation: float):
        self.rotation = rotation

    def backAlign(self):
        self.wantTo = True

    @magicbot.feedback
    def isAligned(self):
        return self.doingIt and abs(self.lastError) < 0.05

    def noteAlign(self):
        if self.tclass == "note":
            steering_adjust = self.kpturn * self.tx
            self.extra_rotation = steering_adjust

            if self.extra_rotation > self.maxAdjustment:
                self.extra_rotation = self.maxAdjustment
            elif self.extra_rotation < -self.maxAdjustment:
                self.extra_rotation = -self.maxAdjustment
            return True
        else:
            return False

    # 0.4
    ## only the right encoder works

    # wpilib.SmartDashboard.putNumber("lower", self.lower_sensor.getDistance())

    def execute(self):
        if self.wantTo == False:
            self.doingIt = False
        else:
            sensorPosition = self.encoder_r.getDistance()
            if self.doingIt == False:
                self.doingIt = True
                self.startPos = sensorPosition

            setpoint = self.startPos + self.offset
            error = setpoint - sensorPosition

            self.lastError = error
            outputSpeed = self.kP * error

            if outputSpeed > self.maxOutput:
                outputSpeed = self.maxOutput
            elif outputSpeed < -self.maxOutput:
                outputSpeed = -self.maxOutput

            self.move(outputSpeed, 0)

        # if self.tank:
        #     self.drive.tankDrive(self.l, self.r)
        # elif self.volts:
        #     self.drive.feed()
        #     self.drive_l1.setVoltage(self.lv)
        #     self.drive_r1.setVoltage(self.rv)
        # else:
        self.drive.arcadeDrive(
            self.speed * self.limit,
            (self.rotation + self.extra_rotation) * self.limit,
            False,
        )
