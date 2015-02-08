import wpilib
from networktables.networktable import NetworkTable
class Alignment (object):
    def __init__(self, leftInfrared, rightInfrared):
        self.rightSensor = rightInfrared
        self.leftSensor = leftInfrared
        sd = NetworkTable.getTable('SmartDashboard')
        self.c = sd.getAutoUpdateValue('Align Constant', .1)
        self.t = sd.getAutoUpdateValue('Voltage Threshold', .5)
    def get_speed(self):
        r_voltage = self.rightSensor.getVoltage()
        l_voltage = self.leftSensor.getVoltage()
        c = wpilib.SmartDashboard.getDouble('Align Constant')
        if abs(r_voltage-l_voltage)<2:
            rotateSpeed=0
        elif r_voltage>l_voltage: 
            diff = r_voltage-l_voltage
            rotateSpeed = min(self.t, diff*self.c)*-1
        elif l_voltage>r_voltage:
            diff = l_voltage-r_voltage
            rotateSpeed = min(self.t, diff*c)
        return rotateSpeed
