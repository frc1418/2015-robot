#!/usr/bin/env python3

import wpilib
from wpilib.cantalon import CANTalon

class MyRobot(wpilib.SampleRobot):
    
    def robotInit(self):
        self.servo= wpilib.Servo(6)

        ##INITIALIZE JOYSTICKS##
        self.joystick1 = wpilib.Joystick(0)
        self.joystick2 = wpilib.Joystick(0)

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
            self.rotation = (self.joystick2.getX() / 2)
            
            #self.robot_drive.mecanumDrive_Cartesian((self.x), (self.y), (self.rotation), 0,)
            wpilib.Timer.delay(0.025)
            
if __name__ == '__main__':
    wpilib.run(MyRobot)
