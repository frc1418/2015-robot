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
        self.rotate_speed = sd.getAutoUpdateValue('Align|Rotation Speed', .1)
        self.drive_speed = sd.getAutoUpdateValue('Align|Speed', -.3)
        self.threshold = sd.getAutoUpdateValue('Align|DistThreshold', 3)
        self.strafe_speed = sd.getAutoUpdateValue('Align|StrafeSpeed', .1)
        
        self.next_pos = None
        self.aligning = False
        self.aligned = False
        
    def get_rotation_speed(self):
        r_voltage = self.rightSensor.getDistance()
        l_voltage = self.leftSensor.getDistance()
        
        if abs(r_voltage-l_voltage)<self.threshold.value:
            rotateSpeed=0
        elif r_voltage>l_voltage: 
            diff = r_voltage-l_voltage
            rotateSpeed = min(self.drive_speed.value, diff*self.rotate_speed.value)*-1
        elif l_voltage>r_voltage:
            diff = l_voltage-r_voltage
            rotateSpeed = min(self.drive_speed.value, diff*self.rotate_speed.value)
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
            
        if not leftLimit and rightLimit: ##Right side not touching tote
            self.drive.move(self.drive_speed.value, -self.strafe_speed.value, rotation)
        elif leftLimit and not rightLimit: ##Left side is not touching tote
            self.drive.move(self.drive_speed.value, self.strafe_speed.value, rotation)
        elif not leftLimit and not rightLimit:
            self.forkLift.raise_forklift()
            self.aligned = True
        else:
            self.drive.move(self.drive_speed.value, 0, 0)
    
    def is_in_range(self):
        rightDist = self.rightSensor.getDistance()
        leftDist = self.leftSensor.getDistance()
        if rightDist>4 and rightDist<120 and leftDist>4 and leftDist<120:
            return True
        return False
    
    def is_against_tote(self):
        if not self.rightToteLimit.get() and not self.leftToteLimit.get():
            return True
        return False
    
    def doit(self):
        if not self.aligning:
            self.aligned = False
        
        self.aligning = False
        