import wpilib
import math

class MyRobot(wpilib.SampleRobot):
    def robotInit(self):
        super().__init__()
        print("Team 1418 2015 Test Code")
        self.joystick1 = wpilib.Joystick(0)
        
        self.lf_motor = wpilib.Talon(0)
        self.lr_motor = wpilib.Talon(1)
        self.rr_motor = wpilib.Talon(2)
        self.rf_motor = wpilib.Talon(3)
        
        self.logTimer = wpilib.Timer()
        self.logTimer.start()
        
        self.robot_drive = wpilib.RobotDrive(self.lr_motor, self.rr_motor, self.lf_motor, self.rf_motor)
        self.robot_drive.setSafetyEnabled(False)
        self.robot_drive.setInvertedMotor(0, True)
        self.robot_drive.setInvertedMotor(2, True)
    def operatorControl(self):
        print("Entering Teleop")
        while self.isOperatorControl() and self.isEnabled():
            if self.joystick1.getPOV()is not 180 or 90:
                strafe = 0
            else:
                strafe = math.sin(self.joystick1.getPOV())
            self.robot_drive.mecanumDrive_Cartesian(self.joystick1.getY(), math.sin(self.joystick1.getPOV()), self.joystick1.getTwist()*-1, 0)
            if self.joystick1.getRawButton(4):
                self.robot_drive.mecanumDrive_Cartesian(0, -1, 0, 0)
            if self.joystick1.getRawButton(5):
                self.robot_drive.mecanumDrive_Cartesian(0, 1, 0, 0)
            if self.logTimer.hasPeriodPassed(1.0):
                pass
                #self.logger.info(self.DriverStation.getStickPOV(0,0))
            wpilib.Timer.delay(.01)
                
        
    def disabled(self):
        '''Called when the robot is in disabled mode'''
        
        
        wpilib.Timer.delay(.01)

if __name__ == '__main__':
    
    wpilib.run(MyRobot)