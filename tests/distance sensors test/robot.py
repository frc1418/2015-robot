import wpilib
from wpilib.smartdashboard import SmartDashboard
from wpilib.joystick import Joystick

class MyRobot(wpilib.SampleRobot):
    
    def robotInit(self):
        self.joystick1 = wpilib.Joystick(0)
        self.joystick2 = wpilib.Joystick(1)
        self.joystick3 = wpilib.Joystick(2)
        
        
        self.smalldistance = wpilib.AnalogInput(0)
        self.largedistance = wpilib.AnalogInput(1)
        self.smalldistance2 = wpilib.AnalogInput(3)
                
        
    def operatorControl(self):
        #self.myRobot.setSafetyEnabled(True)

        while self.isOperatorControl() and self.isEnabled():
            '''
            wpilib.SmartDashboard.putNumber('smallSensor Voltage', self.smalldistance.getVoltage())
            wpilib.SmartDashboard.putNumber('smallSensor Voltage', self.smalldistance2.getVoltage())
            wpilib.SmartDashboard.putNumber('largeSensor Voltage', self.largedistance.getVoltage())
            '''
            wpilib.SmartDashboard.putNumber('smallSensor Voltage', self.joystick1.getX())
            wpilib.SmartDashboard.putNumber('smallSensor Voltage', self.joystick2.getX())
            wpilib.SmartDashboard.putNumber('largeSensor Voltage', self.joystick3.getX())
            
            self.fixedSmallValue = ((max(0,self.smalldistance.getVoltage()))/9.042)**0.8605
            self.fixedSmallValue2 = ((max(0,self.smalldistance2.getVoltage()))/9.042)**0.8605
            self.fixedLargeValue = ((max(0,self.smalldistance.getVoltage()))/22.73)**0.03081          
            
            
            wpilib.SmartDashboard.putNumber('smallSensor Value in cm', self.fixedSmallValue)
            wpilib.SmartDashboard.putNumber('second smallSensor Value in cm', self.fixedSmallValue2)
            wpilib.SmartDashboard.putNumber('largeSensor Value in cm', self.fixedLargeValue)
            
            
        
            wpilib.Timer.delay(0.005)
    '''        
    def convertVoltageToDistance (self, voltage, SmallerSensor):
        if(SmallerSensor):
            return ((self.voltage)/9.042)**0.8605
        else:
            return ((self.voltage)/22.73)**0.03081
        
    '''
if __name__ == '__main__':
    wpilib.run(MyRobot)
