import wpilib
from common.distance_sensors import SharpIR2Y0A02, SharpIRGP2Y0A41SK0F, CombinedSensor
from networktables import NetworkTable

class Sensor:
    
    def __init__(self, tote_motor, can_motor):
        
        self.sd = NetworkTable.getTable('SmartDashboard')
        
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
        
        self.in_range = False
        self.in_range_start = None
        
        # Premature optimization, but it looks nicer
        self._tote_exclude_range = set()
        
        for i in [1060, 1992, 4610, 5457, 7995]:
            for j in range(i-85, i+85):
                self._tote_exclude_range.add(j)
        
        self.update()
        
    def update(self):
        
        self.now = wpilib.Timer.getFPGATimestamp()
        
        self.toteLimitL = self.toteLimitLSensor.get()
        self.toteLimitR = self.toteLimitRSensor.get()
        
        self.longDistanceL = self.longDistanceLSensor.getDistance()
        self.longDistanceR = self.longDistanceRSensor.getDistance()
        self.shortDistanceL = self.shortDistanceLSensor.getDistance() 
        self.shortDistanceR = self.shortDistanceRSensor.getDistance() 
                
        self.leftDistance = self.leftSensor.getDistance()
        self.rightDistance = self.rightSensor.getDistance()
        
        self.tote_enc = self.tote_motor.getEncPosition()
        self.can_enc = self.can_motor.getEncPosition()
        
        # Calculate if its in range
        in_range = (self.leftDistance < 120 and self.rightDistance < 120)
        
        # if it's in the way, then set it to the last thing
        self.interfered = self.tote_enc in self._tote_exclude_range
        if self.interfered:
            in_range = self.in_range
        
        if self.in_range_start is None:
            if in_range:
                self.in_range_start = self.now
        else:
            self.in_range = in_range and self.now > self.in_range_start + 0.1
                
            if not in_range:
                self.in_range_start = None
        
    
    def is_against_tote(self):
        if not self.toteLimitL and not self.toteLimitR:
            return True
        return False
    
    def is_in_range(self):
        return self.in_range
    
    def update_sd(self):
        self.sd.putNumber('shortSensorValueL', self.shortDistanceL)
        self.sd.putNumber('shortSensorValueR', self.shortDistanceR)
        self.sd.putNumber('longSensorValueL', self.longDistanceL)
        self.sd.putNumber('longSensorValueR', self.longDistanceR)
        #self.sd.putNumber('shortSensorVoltageL', self.sensor.shortDistanceL)
        #self.sd.putNumber('shortSensorVoltageR', self.sensor.shortDistanceR)
        #self.sd.putNumber('longSensorVoltageL', self.sensor.longDistanceL)
        #self.sd.putNumber('longSensorVoltageR', self.sensor.longDistanceR)
        
        self.sd.putBoolean('toteInRange', self.in_range)
        self.sd.putBoolean('toteInterfere', self.interfered)
        
        self.sd.putNumber('combinedL', self.leftDistance)
        self.sd.putNumber('combinedR', self.rightDistance)
        
        self.sd.putBoolean('toteLimitL', self.toteLimitL)
        self.sd.putBoolean('toteLimitR', self.toteLimitR)
        
    