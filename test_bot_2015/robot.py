import wpilib

class MyRobot(wpilib.SampleRobot):
    def robotInit(self):
        super().__init__()
        print("Team 1418 2015 Test Code")
        self.joystick1 = wpilib.Joystick(0)
        self.joystick2 = wpilib.Joystick(1)
        
        self.lmotor = wpilib.Talon(5)
        self.rmotor = wpilib.Talon(10)
        
        self.robot_drive = wpilib.RobotDrive(self.lmotor,self.rmotor )
        self.robot_drive.setSafetyEnabled(False)  
        
    def operatorControl(self):
        print("Entering Teleop")
        while self.isOperatorControl() and self.isEnabled():
            self.robot_drive.tankDrive(self.joystick1, self.joystick2)
            wpilib.Timer.delay(.01)
        
    def disabled(self):
        '''Called when the robot is in disabled mode'''
        
        
        wpilib.Timer.delay(.01)

if __name__ == '__main__':
    
    wpilib.run(MyRobot)