#!/usr/bin/env python3

import wpilib
from wpilib.cantalon import CANTalon

class MyRobot(wpilib.SampleRobot):
    
    def robotInit(self):
        self.servo= wpilib.Servo(6)

        ##INITIALIZE JOYSTICKS##
        self.joystick1 = wpilib.Joystick(0)
        self.joystick2 = wpilib.Joystick(1)
        
        ##INITIALIZE MOTORS##
        self.lf_motor = wpilib.CANTalon(6)
        self.lr_motor = wpilib.CANTalon(2)
        self.rf_motor = wpilib.CANTalon(8)
        self.rr_motor = wpilib.CANTalon(4)
        
        ##ROBOT DRIVE##
        self.robot_drive = wpilib.RobotDrive(self.lf_motor, self.lr_motor, self.rf_motor, self.rr_motor)
        self.robot_drive.setInvertedMotor(wpilib.RobotDrive.MotorType.kFrontRight, True)
        self.robot_drive.setInvertedMotor(wpilib.RobotDrive.MotorType.kRearRight, True)

    def disabled(self):
        wpilib.Timer.delay(.01)
    
    def operatorControl(self):
        while self.isOperatorControl() and self.isEnabled():
            if self.joystick1.getRawButton(3):
                self.servo.set(1)
            if self.joystick1.getRawButton(2):
                self.servo.set(0)
                
            self.x = self.joystick1.getX()
            self.y = self.joystick1.getY()
            
            #Forward and Backward for testing
            if self.joystick2.getRawButton(2):
                self.y = 0.5;
            if self.joystick2.getRawButton(3):
                self.y = -0.5;
            
            self.rotation = (self.joystick2.getX() / 2)
            
            self.robot_drive.mecanumDrive_Cartesian(self.x, self.y, self.rotation, 0)
            wpilib.Timer.delay(0.025)
            
if __name__ == '__main__':
    wpilib.run(MyRobot)
