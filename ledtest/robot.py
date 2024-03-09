# TODO: insert robot code here
from robotpy_ext.common_drivers.distance_sensors import SharpIR2Y0A21
import wpilib


class MyRobot(wpilib.TimedRobot):
    def robotInit(self) -> None:
        self.sensor = SharpIR2Y0A21(2)

    def robotPeriodic(self) -> None:
        wpilib.SmartDashboard.putNumber("distance", self.sensor.getDistance())
