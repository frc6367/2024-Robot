import wpilib.drive
import phoenix5
import magicbot
import navx
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

    tx = ntproperty("/limelight/tx", 0.0)
    tclass = ntproperty("/limelight/tclass", "")
    kpturn = magicbot.tunable(-0.1)
    maxAdjustment = magicbot.tunable(0.3)

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

        return outputSpeed, doingIt

    def execute(self):

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


class DrivePID:

    offset = magicbot.tunable(0.0)
    wantTo = magicbot.will_reset_to(False)

    output = 0

    def setup(self):
        self.doingIt = False

    def getSetpoint(self) -> float: ...

    def getSensor(self) -> float: ...

    def doIt(self, kP, maxOutput):
        if self.wantTo == False:
            self.doingIt = False
            return None

        else:
            sensorValue = self.getSensor()

            if self.doingIt == False:
                self.doingIt = True
                self.startPos = sensorValue

            error = self.getSetpoint() - sensorValue

            self.lastError = error
            outputSpeed = kP * error

            if outputSpeed > maxOutput:
                outputSpeed = maxOutput
            elif outputSpeed < -maxOutput:
                outputSpeed = -maxOutput

            return outputSpeed


class NavxPID(DrivePID):

    drivetrain: DriveTrain
    navx: navx.AHRS

    maxOutput = magicbot.tunable(0.3)
    kP = magicbot.tunable(0.25)

    def enable(self, v):
        self.wantTo = True
        self.offset = v

    @magicbot.feedback
    def isAligned(self):
        return self.doingIt and abs(self.lastError) < 3

    @magicbot.feedback
    def yaw(self):
        return self.navx.getYaw()

    def getSetpoint(self) -> float:
        return self.offset

    def getSensor(self):
        return self.navx.getYaw()

    def execute(self):
        output = self.doIt(self.kP, self.maxOutput)
        if output is not None:
            self.drivetrain.rotation = -output


class EncoderPID(DrivePID):
    drivetrain: DriveTrain
    encoder_r: wpilib.Encoder

    maxOutput = magicbot.tunable(0.5)
    kP = magicbot.tunable(3.0)

    def enable(self):
        self.wantTo = True
        self.offset = -0.4

    @magicbot.feedback
    def isAligned(self):
        return self.doingIt and abs(self.lastError) < 0.05

    def getSetpoint(self) -> float:
        return self.startPos + self.offset

    def getSensor(self):
        return self.encoder_r.getDistance()

    def execute(self):
        output = self.doIt(self.kP, self.maxOutput)
        if output is not None:
            self.drivetrain.speed = output
