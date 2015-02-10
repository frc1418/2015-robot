import wpilib
from networktables.networktable import NetworkTable
import logging
logger = logging.getLogger("Aligning")

class Alignment (object):
    def __init__(self, leftInfrared, rightInfrared):
        self.rightSensor = rightInfrared
        self.leftSensor = leftInfrared
        sd = NetworkTable.getTable('SmartDashboard')
        self.c = sd.getAutoUpdateValue('Align Constant', .7)
        self.c = sd.getAutoUpdateValue('Speed Constant', .5)
        self.t = sd.getAutoUpdateValue('Dist Threshold', .5)
    def get_speed(self):
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
    def align(self, leftLim, rightLim, next_pos):
        self.limit1 = self.leftLim.get()
        self.limit2 = self.rightLim.get()
        self.next_pos = next_pos
        self.drive.move(0, 0, self.align.get_speed())
        if self.align.get_speed() == 0:
            self.aligned = True
            
        if self.aligned:
            self.drive.move(-.3, 0, 0)
            
        if not self.limit1 and self.limit2:
            self.drive.move(-.3, -.2, 0)
        elif not self.limit2 and self.limit1:
            self.drive.move(-.3, .2, 0)
        elif not self.limit1 and not self.limit2:
            self.tote_forklift._set_position(self.next_pos)
            self.aligned = False  
            self.aligning = False
        
    def doit(self):
        pass