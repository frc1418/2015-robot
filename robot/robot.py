#!/usr/bin/env python3

import wpilib
import math
from components import forklift, drive
from common.distance_sensors import SharpIR2Y0A02, SharpIRGP2Y0A41SK0F, CombinedSensor
from wpilib.smartdashboard import SmartDashboard

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
        self.tote_motor = wpilib.CANTalon(5)
        self.bin_motor = wpilib.CANTalon(15)
        
        #CAMERA
        try:
            self.camera = wpilib.USBCamera()
            self.camera.startCapture()
            self.camServ = wpilib.CameraServer()
            self.camServ.startAutomaticCapture(self.camera)
        except:
            self.camera = None
       
        ##ROBOT DRIVE##
        self.robot_drive = wpilib.RobotDrive(self.lr_motor, self.rr_motor, self.lf_motor, self.rf_motor)
        self.robot_drive.setInvertedMotor(0, True)
        self.robot_drive.setInvertedMotor(2, True)

        ##INITIALIZE SENSORS#
        
        
        #self.gyro = wpilib.Gyro(4)
        self.forklift = forklift.Forklift(self.tote_motor, self.bin_motor)
        
        self.drive = drive.Drive(self.robot_drive,0)
        
        #self.longDistance = SharpIR2Y0A02(0)
        #self.longDistance2 = SharpIR2Y0A02(2)
        #self.shortDistance = SharpIRGP2Y0A41SK0F(1)
        #self.shortDistance2 = SharpIRGP2Y0A41SK0F(3)
        self.combinedDistance = CombinedSensor(0,1)
        self.combinedDistance2 = CombinedSensor(2,3)
                
        
        self.components = {
            'forklift': self.forklift,
            'drive': self.drive
        }
    def operatorControl(self):
        
        print("Entering Teleop")
        while self.isOperatorControl() and self.isEnabled():
            self.drive.move((self.joystick1.getY()*-1), (self.joystick1.getX()), (self.joystick2.getX()) / 2)
            if self.joystick1.getRawButton(2):
                self.tote_motor.set(.5)
                self.drive.move((self.joystick1.getY())/2, (self.joystick1.getX())/2, (self.joystick2.getX()) / 2)
            elif self.joystick1.getRawButton(3):
                self.tote_motor.set(-.5)
                self.drive.move((self.joystick1.getY())/2, (self.joystick1.getX())/2, (self.joystick2.getX()) / 2)
            elif self.joystick2.getRawButton(3):
                self.bin_motor.set(.5)
                self.drive.move((self.joystick1.getY())/2, (self.joystick1.getX())/2, (self.joystick2.getX()) / 2)
            elif self.joystick2.getRawButton(2):
                self.bin_motor.set(-.5)
                self.drive.move((self.joystick1.getY())/2, (self.joystick1.getX())/2, (self.joystick2.getX()) / 2)
            else: 
                self.tote_motor.set(0)
                self.bin_motor.set(0)
                
            #INFARED DRIVE#
            #if(self.joystick1.getTrigger()==1):
            #        self.drive.infrared_rotation(self.combinedDistance.getDistance(),self.combinedDistance2.getDistance())
                    
            self.update()
            self.smartdashbord_update()
            wpilib.Timer.delay(.01)
        
    def smartdashbord_update(self):
        wpilib.SmartDashboard.putNumber('shortSensorValue', self.combinedDistance.getDistance())
        wpilib.SmartDashboard.putNumber('shortSensorValue2',self.combinedDistance2.getDistance())

        wpilib.SmartDashboard.putNumber('largeSensorValue', self.combinedDistance.getDistance())
        wpilib.SmartDashboard.putNumber('largeSensorValue2', self.combinedDistance2.getDistance())
        
    def update (self):
        for component in self.components.values():
            component.doit()
            
            
    def disabled(self):
        '''Called when the robot is in disabled mode'''
        while not self.isEnabled():
            self.smartdashbord_update()
            wpilib.Timer.delay(.01)

        
if __name__ == '__main__':
    
    wpilib.run(MyRobot)
