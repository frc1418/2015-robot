
from networktables import NetworkTable
import logging
logger = logging.getLogger("Aligning")

from common.sensor import Sensor

class Alignment:
    
    sensors = Sensor
    
    def __init__(self, sensors, forkLift, drive):
        '''
            :param sensors: Sensors object
            :type sensors: :class:`.Sensor`
        '''
        
        self.sensors = sensors
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
        l_voltage = self.sensors.leftDistance
        r_voltage = self.sensors.rightDistance
        
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
        
        leftLimit = self.sensors.toteLimitL
        rightLimit = self.sensors.toteLimitR
        
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
    
    
    
    def doit(self):
        if not self.aligning:
            self.aligned = False
        
        self.aligning = False
        