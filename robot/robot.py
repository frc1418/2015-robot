#!/usr/bin/env python3

import wpilib
from components import drive, alignment
from components.forklift import ToteForklift, CanForklift
from common.distance_sensors import SharpIR2Y0A02, SharpIRGP2Y0A41SK0F
from common.button import Button

from robotpy_ext.autonomous import AutonomousModeSelector

class MyRobot(wpilib.SampleRobot):
    
    def robotInit(self):
        print("Team 1418's 2015 Code")

        ##INITIALIZE JOYSTICKS##
        self.joystick1 = wpilib.Joystick(0)
        self.joystick2 = wpilib.Joystick(1)

        #hello
        ##INITIALIZE MOTORS##
        self.lf_motor = wpilib.Talon(0)
        self.lr_motor = wpilib.Talon(1)
        self.rf_motor = wpilib.Talon(2)
        self.rr_motor = wpilib.Talon(3)

        ##ROBOT DRIVE##
        self.robot_drive = wpilib.RobotDrive(self.lf_motor, self.lr_motor, self.rf_motor, self.rr_motor)
        self.robot_drive.setInvertedMotor(wpilib.RobotDrive.MotorType.kFrontRight, True)
        self.robot_drive.setInvertedMotor(wpilib.RobotDrive.MotorType.kRearRight, True)

        ##INITIALIZE SENSORS#


        self.gyro = wpilib.Gyro(0)
        self.tote_forklift = ToteForklift(5, 2)
        self.can_forklift = CanForklift(15, 3)
        self.lim1 = wpilib.DigitalInput(0)
        self.lim2= wpilib.DigitalInput(1)
        

        self.drive = drive.Drive(self.robot_drive,0)
        

        self.longDistanceL = SharpIR2Y0A02(1) ## Robot's left
        self.longDistanceR = SharpIR2Y0A02(2) ## Robot's right
        self.shortDistanceL = SharpIRGP2Y0A41SK0F(3) ## Robot's left
        self.shortDistanceR = SharpIRGP2Y0A41SK0F(4) ## Robot's right

        self.align = alignment.Alignment(self.shortDistanceL, self.shortDistanceR)
        
        self.components = {
            'tote_Forklift': self.tote_forklift,
            'can_Forklift': self.can_forklift,
            'drive': self.drive
        }

        self.control_loop_wait_time = 0.025
        self.automodes = AutonomousModeSelector('autonomous', self.components)
        
        ##Defining Buttons##
        #self.canUp = Button(self.joystick1,3)
        #self.canDown = Button(self.joystick1,2)
        #self.canTop = Button(self.joystick1,6)
        #self.canBottom = Button(self.joystick1,7)
        self.toteUp = Button(self.joystick2,3)
        self.toteDown = Button(self.joystick2,2)
        self.toteTop = Button(self.joystick2,6)
        self.toteBottom = Button(self.joystick2,7)
        
        self.triggerPressed = False



    def autonomous(self):
        self.automodes.run(self.control_loop_wait_time, self.update)

    def operatorControl(self):

        #self.can_forklift.set_manual(0)
        #self.tote_forklift.set_manual(0)

        self.logger.info("Entering teleop mode")
        
        while self.isOperatorControl() and self.isEnabled():
            self.drive.move(self.joystick1.getY(), self.joystick1.getX(), self.joystick2.getX())

            #
            # Can forklift controls
            #
            

            if self.joystick1.getRawButton(5):
                self.can_forklift.set_manual(1)
                
            elif self.joystick1.getRawButton(4):
                self.can_forklift.set_manual(-1)
            #========DO NOT UNCOMMENT===========
            #elif self.canUp.get():
            #    self.can_forklift.raise_forklift()
            #    
            #elif self.canDown.get():
            #    self.can_forklift.lower_forklift()
            #    
            #if self.canTop.get():
            #    self.can_forklift.set_pos_top()
            #elif self.canBottom.get():
            #    self.can_forklift.set_pos_bottom()
            #============================ 
            #
            # Tote forklift controls
            #
             
            if self.joystick2.getRawButton(5):
                self.tote_forklift.set_manual(1)
                
            elif self.joystick2.getRawButton(4):
                self.tote_forklift.set_manual(-1)
            
            elif self.toteUp.get():
                self.tote_forklift.raise_forklift()
                
            elif self.toteDown.get():
                self.tote_forklift.lower_forklift()
                
            if self.toteTop.get():
                self.tote_forklift.set_pos_top()
            elif self.toteBottom.get():
                self.tote_forklift.set_pos_bottom()
                
                
            #INFRARED DRIVE#
            if self.joystick2.getTrigger():
                self.drive.move(0, 0, self.align.get_speed())
            
            #REVERSE DRIVE#
            if self.joystick1.getTrigger() and (self.triggerPressed==False):
                self.drive.switch_direction()
                self.triggerPressed = True
            if self.joystick1.getTrigger()==False:
                self.triggerPressed=False

            
            self.smartdashbord_update()
            self.update()
            wpilib.Timer.delay(self.control_loop_wait_time)

    def smartdashbord_update(self):
       # wpilib.SmartDashboard.putNumber('shortSensorValueL', self.shortDistanceL.getDistance())
       # wpilib.SmartDashboard.putNumber('shortSensorValueR',self.shortDistanceR.getDistance())
       # wpilib.SmartDashboard.putNumber('largeSensorValueL', self.longDistanceL.getDistance())
       # wpilib.SmartDashboard.putNumber('largeSensorValueR', self.longDistanceR.getDistance())
        if self.can_forklift.target_position is None:
            wpilib.SmartDashboard.putNumber('Can Target', -1)
        else:   
            wpilib.SmartDashboard.putNumber('Can Target', self.can_forklift.target_position)
        wpilib.SmartDashboard.putDouble('Can Encoder', self.can_forklift.motor.getEncPosition())
        if self.tote_forklift.target_position is None:
            wpilib.SmartDashboard.putNumber('Tote Target', -1)
        else:
            wpilib.SmartDashboard.putNumber('Tote Target', self.tote_forklift.target_position)
        wpilib.SmartDashboard.putDouble('Tote Encoder', self.tote_forklift.motor.getEncPosition())
    
    



    def update (self):
        for component in self.components.values():
            component.doit()

    def disabled(self):
        '''Called when the robot is in disabled mode'''
        
        self.logger.info("Entering disabled mode")
        
        while not self.isEnabled():
            self.smartdashbord_update()
            wpilib.Timer.delay(.01)

    def test(self):
        '''Called when the robot is in test mode'''
        while self.isTest() and self.isEnabled():
            wpilib.LiveWindow.run()
            wpilib.Timer.delay(.01)

if __name__ == '__main__':

    wpilib.run(MyRobot)
