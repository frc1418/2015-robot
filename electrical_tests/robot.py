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
        
        ##INITIALIZE JOYSTICKS##
        self.joystick1 = wpilib.Joystick(0)
        self.joystick2 = wpilib.Joystick(1)

        
        ##INITIALIZE MOTORS##
        self.lf_motor = wpilib.Talon(0)
        self.lr_motor = wpilib.Talon(1)
        self.rf_motor = wpilib.Talon(2)
        self.rr_motor = wpilib.Talon(3)
        self.forkliftMotor = wpilib.CANTalon(5)
        self.forkliftMotor2 = wpilib.CANTalon(15)
        self.forkliftMotor.changeControlMode(CANTalon.ControlMode.PercentVbus)
        self.forkliftMotor2.changeControlMode(CANTalon.ControlMode.PercentVbus)
        
        
        ##SMART DASHBOARD
        wpilib.SmartDashboard.putNumber('Pos', 1440)
        wpilib.SmartDashboard.putNumber('P', .001)
        wpilib.SmartDashboard.putNumber('Dist', '3')

        ##ROBOT DRIVE##
        self.robot_drive = wpilib.RobotDrive(self.lf_motor, self.lr_motor, self.rf_motor, self.rr_motor)
        self.robot_drive.setInvertedMotor(wpilib.RobotDrive.MotorType.kFrontRight, True)
        self.robot_drive.setInvertedMotor(wpilib.RobotDrive.MotorType.kRearRight, True)

    def disabled(self):
        #self.talon.setSensorPosition(0)
        wpilib.Timer.delay(.01)
    
    def operatorControl(self):
        #self.myRobot.setSafetyEnabled(True)
        
        while self.isOperatorControl() and self.isEnabled():    
            
            '''
            wpilib.SmartDashboard.putNumber('Enc', self.talon.getEncPosition())
            
            if wpilib.SmartDashboard.getNumber('P') is not self.talon.getP():
                self.talon.setP(wpilib.SmartDashboard.getNumber('P'))
            
            position = (wpilib.SmartDashboard.getNumber('Dist')*1440)/5.75
            canPosition = (wpilib.SmartDashboard.getNumber('Dist')*1440)/9.625
            self.talon.set(wpilib.SmartDashboard.getNumber('Pos')*-1)
            #self.XOfRobot=self.XOfRobot+(self.accelerometer.getX()*.5*(self.timercounter**2))
            #self.YOfRobot=self.YOfRobot+(self.acwcelerometer.getY()*.5*(self.timercounter**2))
            '''
            Canset1=0
            if self.joystick1.getRawButton(2):
                Canset1=(.75)
            if self.joystick1.getRawButton(3):
                Canset1=(-.75)
            
            self.forkliftMotor.set(Canset1)
            #print("setting 1 to %n",Canset1)

            Canset2=0
            if self.joystick2.getRawButton(3):
                Canset2=(.75)
            if self.joystick2.getRawButton(2):
                Canset2=(-.5)
            
            self.forkliftMotor2.set(Canset2)
            #print("setting 2 to %n",Canset2)
            
            self.x=self.joystick1.getX()
            self.y=self.joystick1.getY()
            self.rotation=(self.joystick2.getX() / 2)
            
            self.robot_drive.mecanumDrive_Cartesian((self.x), (self.y), (self.rotation), 0)

            wpilib.Timer.delay(0.005)
            
if __name__ == '__main__':
    wpilib.run(MyRobot)
