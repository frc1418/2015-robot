import wpilib
import math

from components import forklift

class MyRobot(wpilib.SampleRobot):
    def robotInit(self):
        super().__init__()
        print("Team 1418 2015 Test Code")
        
        ##INITIALIZE JOYSTICKS##
        self.joystick1 = wpilib.Joystick(0)
        self.joystick2 = wpilib.Joystick(1)

        
        ##INITIALIZE MOTORS##
        self.lf_motor = wpilib.Talon(0)
        self.lr_motor = wpilib.Talon(1)
        self.rr_motor = wpilib.Talon(2)
        self.rf_motor = wpilib.Talon(3)
        self.lift_motor = wpilib.CANTalon(10)
        
       
        ##ROBOT DRIVE##
        self.robot_drive = wpilib.RobotDrive(self.lr_motor, self.rr_motor, self.lf_motor, self.rf_motor)
        self.robot_drive.setSafetyEnabled(False)
        self.robot_drive.setInvertedMotor(0, True)
        self.robot_drive.setInvertedMotor(2, True)
        
        self.forklift = forklift.Forklift(self.lift_motor)
        
        
        self.components = {
            'forklift': self.forklift,
        }
    def operatorControl(self):
        print("Entering Teleop")
        while self.isOperatorControl() and self.isEnabled():
            if self.joystick1.getPOV()is not 180 or 90:
                self.strafe = 0
            else:
                self.strafe = math.sin(self.joystick1.getPOV())
            self.robot_drive.mecanumDrive_Cartesian((self.joystick1.getY()), (self.joystick1.getX()), (self.joystick2.getX() * -1) / 2, 0)
            
            if self.joystick1.getRawButton(2):
                self.forklift.setLift(.5)
            elif self.joystick1.getRawButton(3):
                self.forklift.setLift(-.5)
            elif self.joystick2.getRawButton(2):
                self.forklift.setLift(1)
            elif self.joystick2.getRawButton(3):
                self.forklift.setLift(-1)
            else: 
                self.forklift.setLift(0)
            self.update()
            wpilib.Timer.delay(.01)
                
        
    def update (self):
        for component in self.components.values():
            component.doit()
    def disabled(self):
        '''Called when the robot is in disabled mode'''
        
        
        wpilib.Timer.delay(.01)

if __name__ == '__main__':
    
    wpilib.run(MyRobot)
