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
        self.c = sd.getAutoUpdateValue('Align Constant', .1)
        self.s = sd.getAutoUpdateValue('Speed Constant', .5)
        self.t = sd.getAutoUpdateValue('Dist Threshold', 3)
        
        self.next_pos = None
        self.aligning = False
        self.aligned = False
        
    def get_rotation_speed(self):
        r_voltage = self.rightSensor.getDistance()
        l_voltage = self.leftSensor.getDistance()
        
        if abs(r_voltage-l_voltage)<self.t.value:
            rotateSpeed=0
        elif r_voltage>l_voltage: 
            diff = r_voltage-l_voltage
            rotateSpeed = min(self.s.value, diff*self.c.value)*-1
        elif l_voltage>r_voltage:
            diff = l_voltage-r_voltage
            rotateSpeed = min(self.s.value, diff*self.c.value)
        #logger.info("Aligning")   
        return rotateSpeed
    
    def align(self):
        '''Will align the totes based on values from infrared sensors'''
        self.aligning = True
        
        if self.aligned:
            return
        
        leftLimit = self.leftToteLimit.get()
        rightLimit = self.rightToteLimit.get()
        
        rotation = self.get_rotation_speed()
        self.drive.move(-.1, 0, 0)
            
        if abs(rotation) < 0.01:
            self.drive.move(-.3, 0, 0)
            
        if not leftLimit and rightLimit:
            self.drive.move(-.3, 0., -.1)
        elif leftLimit and not rightLimit:
            self.drive.move(-.3, 0, .1)
        elif not leftLimit and not rightLimit:
            self.forkLift.raise_forklift()
            self.aligned = True
    def is_in_range(self):
        self.rightDist = self.rightSensor.getDistance()
        self.leftDist = self.leftSensor.getDistance()
        if self.rightSensor.getDistance()>4 and self.rightSensor.getDistance()<145 and self.leftSensor.getDistance()>4 and self.leftSensor.getDistance()<145:
            return True
        return False
    def is_against_tote(self):
        if not self.rightToteLimit and not self.leftToteLimit:
            return True
        return False
    def doit(self):
        
        if not self.aligning:
            self.aligned = False
        
        self.aligning = False
        