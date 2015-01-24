import wpilib
from wpilib import cantalon

class MyRobot(wpilib.SampleRobot):
    
    def robotInit(self):
        self.largeDistance = wpilib.AnalogInput(0)
        self.largeDistance2 = wpilib.AnalogInput(1)
        self.smallDistance = wpilib.AnalogInput(2)
        self.smallDistance2 = wpilib.AnalogInput(3)
        self.accelerometer = wpilib.BuiltInAccelerometer(range=2)
        #self.pot = wpilib.AnalogInput(2)
        self.timercounter = 0
        self.XOfRobot=0
        self.YOfRobot=0
        
        self.talon = wpilib.CANTalon(0)
        
        self.encoder= wpilib.Encoder(0,1)

        
    def disabled(self):
        self.operatorControl()
        
    def operatorControl(self):
        #self.myRobot.setSafetyEnabled(True)
        
        while not self.isEnabled():    
            wpilib.SmartDashboard.putNumber('Accelerometer X', self.accelerometer.getX())
            wpilib.SmartDashboard.putNumber('Accelerometer Y', self.accelerometer.getY())
            #wpilib.SmartDashboard.putNumber('Accelerometer Z', self.accelerometer.getZ())
            
            #large distance 22.73x^-0.7533
            #small distance 7.330x^-0.7685
            fixedLargeValue = ((max(0.00001,self.largeDistance.getVoltage()))/22.73)**(1/-0.7533)/2.54
            fixedLargeValue2 = ((max(0.00001,self.largeDistance2.getVoltage()))/22.73)**(1/-0.7533)/2.54
            fixedSmallValue = ((max(0.00001,self.smallDistance.getVoltage()))/7.330)**(1/-0.7685)/2.54
            fixedSmallValue2 = ((max(0.00001,self.smallDistance2.getVoltage()))/7.330)**(1/-0.7685)/2.54

            wpilib.SmartDashboard.putNumber('largeSensorValue', fixedLargeValue)
            wpilib.SmartDashboard.putNumber('largeSensorValue2', fixedLargeValue2)
            
            wpilib.SmartDashboard.putNumber('smallSensorValue', fixedSmallValue)
            wpilib.SmartDashboard.putNumber('smallSensorValue2', fixedSmallValue2)
            
            #wpilib.SmartDashboard.putNumber('Potentiometer', self.pot.getVoltage())
            
            wpilib.SmartDashboard.putNumber('Enc', self.encoder.getDistance())
            
            self.timercounter=self.timercounter+0.005
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
