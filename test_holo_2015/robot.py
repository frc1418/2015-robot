import wpilib

class MyRobot(wpilib.SampleRobot):
    def robotInit(self):
        super().__init__()
        print("Team 1418 2015 Test Code")
        self.joystick1 = wpilib.Joystick(0)
        self.joystick2 = wpilib.Joystick(1)
        
        self.lf_motor = wpilib.Talon(0);
        self.lr_motor = wpilib.Talon(1);
        self.rr_motor = wpilib.Talon(2);
        self.rf_motor = wpilib.Talon(3);
        
        self.robot_drive = wpilib.RobotDrive(self.lf_motor, self.lr_motor, self.rr_motor, self.rf_motor)
        self.robot_drive.setSafetyEnabled(False)  
        
    def operatorControl(self):
        print("Entering Teleop")
        while self.isOperatorControl() and self.isEnabled():
            self.robot_drive.holonomicDrive(self.joystick1.getY(), self.joystick1.getX(), self.joystick2.getX())
            wpilib.Timer.delay(.01)
        
    def disabled(self):
        '''Called when the robot is in disabled mode'''
        
        
        wpilib.Timer.delay(.01)

if __name__ == '__main__':
    
    wpilib.run(MyRobot)