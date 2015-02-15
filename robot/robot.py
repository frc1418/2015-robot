#!/usr/bin/env python3

import wpilib
from components import drive, alignment
from components.forklift import ToteForklift, CanForklift
from common.distance_sensors import SharpIR2Y0A02, SharpIRGP2Y0A41SK0F, CombinedSensor
from common.button import Button

from networktables import NetworkTable

from robotpy_ext.misc import PreciseDelay
from robotpy_ext.autonomous import AutonomousModeSelector

class MyRobot(wpilib.SampleRobot):

    def robotInit(self):
        
        self.sd = NetworkTable.getTable('SmartDashboard')

        # #INITIALIZE JOYSTICKS##
        self.joystick1 = wpilib.Joystick(0)
        self.joystick2 = wpilib.Joystick(1)

        # hello
        # #INITIALIZE MOTORS##
        self.lf_motor = wpilib.Talon(0)
        self.lr_motor = wpilib.Talon(1)
        self.rf_motor = wpilib.Talon(2)
        self.rr_motor = wpilib.Talon(3)

        # #ROBOT DRIVE##
        self.robot_drive = wpilib.RobotDrive(self.lf_motor, self.lr_motor, self.rf_motor, self.rr_motor)
        self.robot_drive.setInvertedMotor(wpilib.RobotDrive.MotorType.kFrontRight, True)
        self.robot_drive.setInvertedMotor(wpilib.RobotDrive.MotorType.kRearRight, True)

        # #INITIALIZE SENSORS#


        self.gyro = wpilib.Gyro(0)
        self.tote_forklift = ToteForklift(5, 2)
        self.can_forklift = CanForklift(15, 3)

        self.toteLimitL = wpilib.DigitalInput(0) ##Left limit switch
        self.toteLimitR = wpilib.DigitalInput(1) ##Right limit switch

        self.next_pos = 1


        self.drive = drive.Drive(self.robot_drive, self.gyro)
        
        self.longDistanceL = SharpIR2Y0A02(1)  # # Robot's left
        self.longDistanceR = SharpIR2Y0A02(3)  # # Robot's right
        self.shortDistanceL = SharpIRGP2Y0A41SK0F(2)  # # Robot's left
        self.shortDistanceR = SharpIRGP2Y0A41SK0F(7)  # # Robot's right
        
        self.backSensor = SharpIRGP2Y0A41SK0F(6)

        self.leftSensors = CombinedSensor(self.longDistanceL, 19.5, self.shortDistanceL, 6)
        self.rightSensors = CombinedSensor(self.longDistanceR, 19.5, self.shortDistanceR, 5)

        self.align = alignment.Alignment(self.leftSensors, self.rightSensors, self.backSensor,
                                         self.toteLimitL, self.toteLimitR,
                                         self.tote_forklift, self.drive)
        
        
        self.components = {
            'tote_forklift': self.tote_forklift,
            'can_forklift': self.can_forklift,
            'drive': self.drive,
            'align': self.align
        }

        self.control_loop_wait_time = 0.025
        self.automodes = AutonomousModeSelector('autonomous', self.components)

        # #Defining Buttons##
        self.canUp = Button(self.joystick1,3)
        self.canDown = Button(self.joystick1,2)
        self.canTop = Button(self.joystick1,6)
        self.canBottom = Button(self.joystick1,7)
        self.toteUp = Button(self.joystick2, 3)
        self.toteDown = Button(self.joystick2, 2)
        self.toteTop = Button(self.joystick2, 6)
        self.toteBottom = Button(self.joystick2, 7)

        self.reverseDirection = Button(self.joystick1, 1)
        #self.alignTrigger = Button(self.joystick2, 1)
        
        self.toteTo=0
        self.oldTote=0
        self.canTo=0
        self.oldCan=0
        self.reverseRobot = False
        self.oldReverseRobot = False
        self.autoLift = False
        
    def autonomous(self):
        self.automodes.run(self.control_loop_wait_time, self.update)

    def operatorControl(self):

        self.can_forklift.set_manual(0)
        self.tote_forklift.set_manual(0)
        
        delay = PreciseDelay(self.control_loop_wait_time)

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

            elif self.canUp.get():
                self.can_forklift.raise_forklift()

            elif self.canDown.get():
                self.can_forklift.lower_forklift()

            if self.canTop.get():
                self.can_forklift.set_pos_top()
            elif self.canBottom.get():
                self.can_forklift.set_pos_bottom()

            # #Tote forklift controls##


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


            # INFRARED DRIVE#
            if self.joystick2.getTrigger():
                self.align.align()


            # REVERSE DRIVE#
            if self.reverseDirection.get():
                self.drive.switch_direction()

            if self.can_forklift.motor.isRevLimitSwitchClosed():
                self.can_forklift.motor.setSensorPosition(0)
            
            
            if self.toteTo != self.oldTote:
                if self.toteTo == 0:
                    self.tote_forklift._set_position(0)
                elif self.toteTo == 1:
                    self.tote_forklift._set_position(1)
                elif self.toteTo == 2:
                    self.tote_forklift._set_position(2)
                elif self.toteTo == 3:
                    self.tote_forklift._set_position(3)
                elif self.toteTo == 2048:
                    self.tote_forklift.set_pos_top()
            self.oldTote = self.toteTo
            
            if self.canTo != self.oldCan:
                if self.canTo == 0:
                    self.can_forklift._set_position(0)
                elif self.canTo == 1:
                    self.can_forklift._set_position(1)
                elif self.canTo == 2:
                    self.can_forklift._set_position(2)
                elif self.canTo == 3:
                    self.can_forklift._set_position(3)
                elif self.canTo == 2048:
                    self.can_forklift.set_pos_top()

            self.oldCan = self.canTo
            
            if self.reverseRobot != self.oldReverseRobot:
                if self.reverseRobot == 0:
                    self.drive.switch_direction()
            self.oldReverseRobot = self.reverseRobot
            
            
            self.smartdashbord_update()
            self.update()
            
            # Replaces wpilib.Timer.delay()
            delay.wait()

    def smartdashbord_update(self):
        self.sd.putNumber('shortSensorValueL', self.shortDistanceL.getDistance())
        self.sd.putNumber('shortSensorValueR', self.shortDistanceR.getDistance())
        self.sd.putNumber('longSensorValueL', self.longDistanceL.getDistance())
        self.sd.putNumber('longSensorValueR', self.longDistanceR.getDistance())
        self.sd.putNumber('shortSensorVoltageL', self.shortDistanceL.getVoltage())
        self.sd.putNumber('shortSensorVoltageR', self.shortDistanceR.getVoltage())
        self.sd.putNumber('longSensorVoltageL', self.longDistanceL.getVoltage())
        self.sd.putNumber('longSensorVoltageR', self.longDistanceR.getVoltage())
        
        self.sd.putNumber('backSensorValue', self.backSensor.getDistance())

        self.can_forklift.update_sd('Can Forklift')
        self.tote_forklift.update_sd('Tote Forklift')
        
        self.sd.putBoolean('toteLimitL', self.toteLimitL.get())
        self.sd.putBoolean('toteLimitR', self.toteLimitR.get())
  
        self.toteTo = self.sd.getInt('liftTo',self.toteTo)
        self.canTo = self.sd.getInt('binTo',self.canTo)
        self.autoLift = self.sd.getBoolean('autoLift', self.autoLift)
        self.reverseRobot = self.sd.getBoolean('reverseRobot',self.reverseRobot)
    
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
