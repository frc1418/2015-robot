import wpilib

class MyRobot(wpilib.SampleRobot):
    
    def robotInit(self):
        self.largeDistance = wpilib.AnalogInput(0)
        self.smallDistance = wpilib.AnalogInput(1)
        self.accelerometer = wpilib.BuiltInAccelerometer(range=2)

        
    def disabled(self):
        self.operatorControl()
        
    def operatorControl(self):
        #self.myRobot.setSafetyEnabled(True)
        
        while not self.isEnabled():    
            wpilib.SmartDashboard.putNumber('Accelerometer X', self.accelerometer.getX())
            wpilib.SmartDashboard.putNumber('Accelerometer Y', self.accelerometer.getY())
            wpilib.SmartDashboard.putNumber('Accelerometer Z', self.accelerometer.getZ())
            
            wpilib.SmartDashboard.putNumber('largeSensor Voltage', self.largeDistance.getVoltage())           
            wpilib.SmartDashboard.putNumber('smalllSensor Voltage', self.smallDistance.getVoltage())
            #large distance 22.73x^-0.7533
            #small distance 7.330x^-0.7685
            self.fixedLargeValue = ((max(0.00001,self.largeDistance.getVoltage()))/22.73)**(1/-0.7533)/2.54
            self.fixedSmallValue = ((max(0.00001,self.smallDistance.getVoltage()))/7.330)**(1/-0.7685)/2.54

            wpilib.SmartDashboard.putNumber('largeSensor Value in in', self.fixedLargeValue)
            wpilib.SmartDashboard.putNumber('smallSensor Value in in', self.fixedSmallValue)
            
            
            
            
            
            
        
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
