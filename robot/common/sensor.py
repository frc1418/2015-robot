import wpilib
from common.distance_sensors import SharpIR2Y0A02, SharpIRGP2Y0A41SK0F, CombinedSensor
class Sensor:
    def __init__(self, tote_motor, can_motor):
        self.toteLimitLSensor = wpilib.DigitalInput(0) ##Left limit switch
        self.toteLimitRSensor = wpilib.DigitalInput(1) ##Right limit switch
        
        self.longDistanceLSensor = SharpIR2Y0A02(1)  # # Robot's left
        self.longDistanceRSensor = SharpIR2Y0A02(3)  # # Robot's right
        self.shortDistanceLSensor = SharpIRGP2Y0A41SK0F(2)  # # Robot's left
        self.shortDistanceRSensor = SharpIRGP2Y0A41SK0F(7)  # # Robot's right
                
        self.leftSensor = CombinedSensor(self.longDistanceLSensor, 20, self.shortDistanceLSensor, 6)
        self.rightSensor = CombinedSensor(self.longDistanceRSensor, 20, self.shortDistanceRSensor, 6)
        
        self.tote_motor = tote_motor
        self.can_motor = can_motor
        
    def update(self):
        self.toteLimitL = self.toteLimitLSensor.get()
        self.toteLimitR = self.toteLimitRSensor.get()
        
        self.longDistanceL = self.longDistanceLSensor.getDistance()
        self.longDistanceR = self.longDistanceRSensor.getDistance()
        self.shortDistanceL = self.shortDistanceLSensor.getDistance() 
        self.shortDistanceR = self.shortDistanceRSensor.getDistance() 
                
        self.leftSensors = self.leftSensor.getDistance()
        self.leftSensors = self.rightSensor.getDistance()
        
        self.tote_enc = self.tote_motor.getEncPosition()
        self.can_enc = self.can_motor.getEncPosition()
        