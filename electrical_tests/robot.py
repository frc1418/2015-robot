#!/usr/bin/env python3

import wpilib
from wpilib.cantalon import CANTalon

class MyRobot(wpilib.SampleRobot):
    
    def robotInit(self):
        self.timercounter = 0

        '''
        self.talon = wpilib.CANTalon(5)
        self.talon.changeControlMode(CANTalon.ControlMode.Position)
        self.talon.setFeedbackDevice(CANTalon.FeedbackDevice.QuadEncoder)
        self.talon.setSensorPosition(0)
        self.talon.setP(.001)
         
        self.bin_talon = wpilib.CANTalon(15)
        self.bin_talon.changeControlMode(CANTalon.ControlMode.Position)
        self.bin_talon.setFeedbackDevice(CANTalon.FeedbackDevice.QuadEncoder)
        self.bin_talon.reverseSensor(True)
        self.bin_talon.setSensorPosition(0)
        '''
        
        # #INITIALIZE JOYSTICKS##
        self.joystick1 = wpilib.Joystick(0)
        self.joystick2 = wpilib.Joystick(1)

        
        # #INITIALIZE MOTORS##
        self.lf_motor = wpilib.Talon(0)
        self.lr_motor = wpilib.Talon(1)
        self.rf_motor = wpilib.Talon(2)
        self.rr_motor = wpilib.Talon(3)
        self.toteMotor = wpilib.CANTalon(5)
        self.canMotor = wpilib.CANTalon(15)
        self.reverse = 1
        
        
        # #SMART DASHBOARD
        
        # #ROBOT DRIVE##
        self.robot_drive = wpilib.RobotDrive(self.lf_motor, self.lr_motor, self.rf_motor, self.rr_motor)
        self.robot_drive.setInvertedMotor(wpilib.RobotDrive.MotorType.kFrontRight, True)
        self.robot_drive.setInvertedMotor(wpilib.RobotDrive.MotorType.kRearRight, True)

    def disabled(self):
        # self.talon.setSensorPosition(0)
        wpilib.Timer.delay(.01)
    
    def operatorControl(self):
        # self.myRobot.setSafetyEnabled(True)
        
        while self.isOperatorControl() and self.isEnabled():    
            
            '''
            wpilib.SmartDashboard.putNumber('Enc', self.toteMotor.getEncPosition())
            
            if wpilib.SmartDashboard.getNumber('P') is not self.talon.getP():
                self.talon.setP(wpilib.SmartDashboard.getNumber('P'))
            
            position = (wpilib.SmartDashboard.getNumber('Dist')*1440)/5.75
            canPosition = (wpilib.SmartDashboard.getNumber('Dist')*1440)/9.625
            self.talon.set(wpilib.SmartDashboard.getNumber('Pos')*-1)
            #self.XOfRobot=self.XOfRobot+(self.accelerometer.getX()*.5*(self.timercounter**2))
            #self.YOfRobot=self.YOfRobot+(self.acwcelerometer.getY()*.5*(self.timercounter**2))
            '''
            if self.joystick1.getRawButton(2):
                self.toteMotor.set(1)
            elif self.joystick1.getRawButton(3):
                self.toteMotor.set(-1)
            else:
                self.toteMotor.set(0)

            if self.joystick2.getRawButton(3):
                self.canMotor.set(1)
            elif self.joystick2.getRawButton(2):
                self.canMotor.set(-1)
            else:
                self.canMotor.set(0)
            
            if self.joystick1.getTrigger():
                self.reverse = 1
            if self.joystick2.getTrigger():
                self.reverse = -1
                
                
            self.x = self.joystick1.getX() * self.reverse
            self.y = self.joystick1.getY() * self.reverse
            self.rotation = (self.joystick2.getX() / 2)
            
            self.robot_drive.mecanumDrive_Cartesian((self.x), (self.y), (self.rotation), 0,)
            
            
            wpilib.Timer.delay(0.005)
            
if __name__ == '__main__':
    wpilib.run(MyRobot)
