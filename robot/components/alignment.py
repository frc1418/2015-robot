import wpilib
from networktables.networktable import NetworkTable
import logging
logger = logging.getLogger("Aligning")

class Alignment (object):
    
    def __init__(self, leftInfrared, rightInfrared, leftToteLimit, rightToteLimit,
                 forkLift, drive):
        
        self.leftSensor = leftInfrared
        self.rightSensor = rightInfrared
        
        self.leftToteLimit = leftToteLimit
        self.rightToteLimit = rightToteLimit
        
        self.forkLift = forkLift
        self.drive = drive
        
        sd = NetworkTable.getTable('SmartDashboard')
        self.c = sd.getAutoUpdateValue('Align Constant', .7)
        self.c = sd.getAutoUpdateValue('Speed Constant', .5)
        self.t = sd.getAutoUpdateValue('Dist Threshold', .5)
        
        self.next_pos = None
        self.aligning = False
        
    def get_rotation_speed(self):
        r_voltage = self.rightSensor.getDistance()
        l_voltage = self.leftSensor.getDistance()
        
        if abs(r_voltage-l_voltage)<3:
            rotateSpeed=0
        elif r_voltage>l_voltage: 
            diff = r_voltage-l_voltage
            rotateSpeed = min(self.t.value, diff*self.c.value)*-1
        elif l_voltage>r_voltage:
            diff = l_voltage-r_voltage
            rotateSpeed = min(self.t.value, diff*self.c.value)
        #logger.info("Aligning")   
        return rotateSpeed
    
    def align(self):
        
        self.aligning = True
        
        if self.aligned:
            return
        
        leftLimit = self.leftToteLimit.get()
        rightLimit = self.rightToteLimit.get()
        
        rotation = self.get_rotation_speed()
        self.drive.move(-.2, 0, rotation)
            
        if abs(rotation) < 0.01:
            self.drive.move(-.3, 0, 0)
            
        if not leftLimit and rightLimit:
            self.drive.move(-.3, -.2, 0)
        elif leftLimit and not rightLimit:
            self.drive.move(-.3, .2, 0)
        elif not leftLimit and not rightLimit:
            self.tote_forklift.raise_forklift()
            self.aligned = True
        
    def doit(self):
        
        if not self.aligning:
            self.aligned = False
        