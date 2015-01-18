import wpilib
from wpilib.smartdashboard import SmartDashboard

class MyRobot(wpilib.SampleRobot):
    
    def robotInit(self):
        self.Accelerometer = wpilib.BuiltInAccelerometer(range=2)        
    def operatorControl(self):
        #self.myRobot.setSafetyEnabled(True)

        while self.isOperatorControl() and self.isEnabled():            
            wpilib.SmartDashboard.putNumber('Accelerometer X', self.Accelerometer.getX())
            wpilib.SmartDashboard.putNumber('Accelerometer Y', self.Accelerometer.getY())
            wpilib.SmartDashboard.putNumber('Accelerometer Z', self.Accelerometer.getZ())
            
                    
            wpilib.Timer.delay(0.005)
            
if __name__ == '__main__':
    wpilib.run(MyRobot)
