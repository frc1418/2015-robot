try:
    import wpilib
except ImportError:
    from pyfrc import wpilib



class MyRobot(wpilib.SimpleRobot):

    def __init__(self):
        
        super().__init__()
        
        self.largeDistance=wpilib.AnalogChannel(1)
        self.largeDistance2=wpilib.AnalogChannel(2)
        self.smallDistance=wpilib.AnalogChannel(3)
        self.smallDistance2=wpilib.AnalogChannel(4)
        
        #self.initSmartDashboard()
    def Disabled(self):
        
        while not self.IsEnabled() and not self.IsOperatorControl():
        
            self.fixedLargeValue = ((max(0.00001,self.largeDistance.GetVoltage()))/22.73)**(1/-0.7533)/2.54
            self.fixedSmallValue = ((max(0.00001,self.smallDistance.GetVoltage()))/7.330)**(1/-0.7685)/2.54
            self.fixedLargeValue2 = ((max(0.00001,self.largeDistance2.GetVoltage()))/22.73)**(1/-0.7533)/2.54
            self.fixedSmallValue2 = ((max(0.00001,self.smallDistance2.GetVoltage()))/7.330)**(1/-0.7685)/2.54

            
            wpilib.SmartDashboard.PutNumber('largeSensorValue', self.fixedLargeValue)
            wpilib.SmartDashboard.PutNumber('smallSensorValue', self.fixedSmallValue)
            wpilib.SmartDashboard.PutNumber('largeSensorValue2', self.fixedLargeValue2)
            wpilib.SmartDashboard.PutNumber('smallSensorValue2', self.fixedSmallValue2)
            
            
            wpilib.Wait(0.025)
        
        
def run():
    robot = MyRobot()
    robot.StartCompetition()
    
    return robot

if __name__ == '__main__':
    
    if not hasattr(wpilib, 'require_version'):
        print("ERROR: You must have pyfrc 2014.7.3 or above installed!") # pragma: no cover
    else:    
        wpilib.require_version('2014.7.3')
    
    
    wpilib.run()
