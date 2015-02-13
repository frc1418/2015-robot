#!/usr/bin/env python3

import wpilib
from components import drive, alignment
from components.forklift import ToteForklift, CanForklift
from common.distance_sensors import SharpIR2Y0A02, SharpIRGP2Y0A41SK0F, CombinedSensor
from common.button import Button

from robotpy_ext.misc import PreciseDelay
from robotpy_ext.autonomous import AutonomousModeSelector

class MyRobot(wpilib.SampleRobot):

    def robotInit(self):
        print("Team 1418's 2015 Code")

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

        try:
            self.camera = wpilib.USBCamera()
            self.camera.startCapture()
            self.camera.setExposureAuto()
            self.cameraServer = wpilib.CameraServer()
            self.cameraServer.startAutomaticCapture(self.camera)
        except:
            self.camera = None
        self.longDistanceL = SharpIR2Y0A02(1)  # # Robot's left
        self.longDistanceR = SharpIR2Y0A02(3)  # # Robot's right
        self.shortDistanceL = SharpIRGP2Y0A41SK0F(2)  # # Robot's left
        self.shortDistanceR = SharpIRGP2Y0A41SK0F(7)  # # Robot's right

        self.leftSensors = CombinedSensor(self.longDistanceL, 19.5, self.shortDistanceL, 6)
        self.rightSensors = CombinedSensor(self.longDistanceR, 19.5, self.shortDistanceR, 5)

        self.align = alignment.Alignment(self.leftSensors, self.rightSensors,
                                         self.toteLimitL, self.toteLimitR,
                                         self.tote_forklift, self.drive)
        
        
        self.components = {
            'tote_Forklift': self.tote_forklift,
            'can_Forklift': self.can_forklift,
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


    def autonomous(self):
        self.automodes.run(self.control_loop_wait_time, self.update)

    def operatorControl(self):

        # self.can_forklift.set_manual(0)
        # self.tote_forklift.set_manual(0)
        
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

            self.smartdashbord_update()
            self.update()
            
            # Replaces wpilib.Timer.delay()
            delay.wait()

    def smartdashbord_update(self):
        wpilib.SmartDashboard.putNumber('shortSensorValueL', self.shortDistanceL.getDistance())
        wpilib.SmartDashboard.putNumber('shortSensorValueR', self.shortDistanceR.getDistance())
        wpilib.SmartDashboard.putNumber('longSensorValueL', self.longDistanceL.getDistance())
        wpilib.SmartDashboard.putNumber('longSensorValueR', self.longDistanceR.getDistance())
        wpilib.SmartDashboard.putNumber('shortSensorVoltageL', self.shortDistanceL.getVoltage())
        wpilib.SmartDashboard.putNumber('shortSensorVoltageR', self.shortDistanceR.getVoltage())
        wpilib.SmartDashboard.putNumber('longSensorVoltageL', self.longDistanceL.getVoltage())
        wpilib.SmartDashboard.putNumber('longSensorVoltageR', self.longDistanceR.getVoltage())

        if self.can_forklift.target_position is None:
            wpilib.SmartDashboard.putNumber('canTarget', -1)
        else:
            wpilib.SmartDashboard.putNumber('canTarget', self.can_forklift.target_position)
        wpilib.SmartDashboard.putDouble('canEncoder', self.can_forklift.motor.getEncPosition())

        if self.tote_forklift.target_position is None:
            wpilib.SmartDashboard.putNumber('toteTarget', -1)
        else:
            wpilib.SmartDashboard.putNumber('toteTarget', self.tote_forklift.target_position)
        wpilib.SmartDashboard.putDouble('toteEncoder', self.tote_forklift.motor.getEncPosition())

        wpilib.SmartDashboard.putBoolean('toteLimitL', self.toteLimitL.get())
        wpilib.SmartDashboard.putBoolean('toteLimitR', self.toteLimitR.get())

        wpilib.SmartDashboard.putBoolean('toteCalibrated', self.tote_forklift.isCalibrated)
        wpilib.SmartDashboard.putBoolean('canCalibrated', self.can_forklift.isCalibrated)




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
