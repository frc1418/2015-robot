
import math

from networktables import NetworkTable

from common.sensor import Sensor

class Alignment:
    
    sensors = Sensor
    
    def __init__(self, sensors, forkLift, drive, autolift):
        '''
            :param sensors: Sensors object
            :type sensors: :class:`.Sensor`
        '''
        
        self.sensors = sensors
        self.forkLift = forkLift
        self.drive = drive
        self.autolift = autolift
        sd = NetworkTable.getTable('SmartDashboard')
        
        self.rotate_constant = sd.getAutoUpdateValue('Align|Rotation Constant', 0.015)   
        self.fwd_constant = sd.getAutoUpdateValue('Align|FwdConstant', 175.0)
        
        self.drive_speed = sd.getAutoUpdateValue('Align|Speed', -.3)
        #self.threshold = sd.getAutoUpdateValue('Align|DistThreshold', 3)
        self.strafe_speed = sd.getAutoUpdateValue('Align|StrafeSpeed', .2)
        
        self.binPos = sd.getAutoUpdateValue('binPosition', 0)
        
        # in centimeters
        self.sensor_spacing = 18
        
        self.next_pos = None
        self.aligning = False
        self.aligned = False
        
        self.can_aligning = True
        self.can_aligned = False
        
        
    def get_tote_angle(self):
        '''returns the angle of the bin in relationship to the front of the robot'''
        diff = self.sensors.leftDistance - self.sensors.rightDistance
        distance = min(self.sensors.leftDistance, self.sensors.rightDistance) + abs(diff/2.0)
        distance = abs(distance)
        
        if abs(diff) < 1:
            angle = 0
        else:
            angle = math.degrees(math.atan2(diff, self.sensor_spacing))
        
        return distance, angle
        
    def get_speed(self):
        ''''returns fwd speed, rotation speed'''
        
        distance, angle = self.get_tote_angle()
        
        # bound it
        distance = min(max(distance, 0.0), 70)
        
        fwd_speed = 0.1 + distance/ self.fwd_constant.value
        
        # bound it
        angle = min(max(angle, -30.0), 30.0)
            
        # calculate a rotation based on the angle
        if abs(angle) < 5:
            rotation_speed = 0
        else:
            rotation_speed = angle * self.rotate_constant.value
        
        return -fwd_speed, rotation_speed
    
    def align(self):
        '''Will align the totes based on values from infrared sensors'''
        self.aligning = True
        
        if self.aligned:
            self.drive.move(-.1, 0, 0)
            return
        
        leftLimit = self.sensors.toteLimitL
        rightLimit = self.sensors.toteLimitR
        
        fwd_speed, rotation_speed = self.get_speed()
        
        # What we really want: if the distance sensor says we're really close,
        # then we need to strafe. Otherwise, go forward.
        
        if not leftLimit and rightLimit: ##Right side not touching tote
            self.drive.move(fwd_speed, -self.strafe_speed.value, rotation_speed)
        
        elif leftLimit and not rightLimit: ##Left side is not touching tote
            self.drive.move(fwd_speed, self.strafe_speed.value, rotation_speed)
        
        elif not leftLimit and not rightLimit:
            self.autolift.autolift()
            self.drive.move(-.1, 0, 0)
            self.aligned = True
        else:
            self.drive.move(fwd_speed, 0, rotation_speed)
    
    def can_align(self):
        self.can_aligning = True
        
        if self.can_aligned:
            self.drive.move(.5, 0, 0) # .5 because the part must go into the can fast enough to engage. Otherwise the can will just be pushed
        if self.binPos.value in range(-.1, .1):
            self.can_aligned = True
        else:
            self.drive.move(0, self.binPos.value/10, 0)
            
    def doit(self):
        if not self.aligning:
            self.aligned = False
        self.aligning = False
        
        if not self.can_aligning:
            self.can_aligned = False
        self.can_aligning = False
        