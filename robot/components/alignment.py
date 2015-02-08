import wpilib
from components import drive

class Alignment (object):
    def __init__(self, leftInfrared, rightInfrared):
        self.rightSensor = rightInfrared
        self.leftSensor = leftInfrared
    
    
    def get_speed(self):
        if abs(self.rightSensor.getVoltage()-self.leftSensor.getVoltage())<2:
            rotateSpeed=0
        elif self.rightSensor.getVoltage()>self.leftSensor.getVoltage   (): 
            diff = self.rightSensor.getVoltage()-self.leftSensor.getVoltage()
            rotateSpeed = min(.5, diff*.1)*-1
        elif self.rightSensor.getVoltage()<self.leftSensor.getVoltage():
            diff = self.leftSensor.getVoltage()-self.rightSensor.getVoltage()
            rotateSpeed = min(.5, diff*.1)
        return rotateSpeed
    def doit(self):
        pass
            