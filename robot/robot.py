#!/usr/bin/env python3

import wpilib
RelayValue = wpilib.Relay.Value

from components import drive, alignment
from components.forklift import ToteForklift, CanForklift
from common.distance_sensors import SharpIR2Y0A02, SharpIRGP2Y0A41SK0F, CombinedSensor
from common.button import Button
from common.sensor import Sensor

from components.interference_measurement import Calibrator


from networktables import NetworkTable

from robotpy_ext.misc import PreciseDelay
from robotpy_ext.autonomous import AutonomousModeSelector

class MyRobot(wpilib.SampleRobot):

    def robotInit(self):
        self.sd = NetworkTable.getTable('SmartDashboard')

        # #INITIALIZE JOYSTICKS##
        self.joystick1 = wpilib.Joystick(0)
        self.joystick2 = wpilib.Joystick(1)
        self.ui_joystick = wpilib.Joystick(2)

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
        
        self.sweeper_relay = wpilib.Relay(0)

        self.gyro = wpilib.Gyro(0)

        self.tote_motor = wpilib.CANTalon(5)
        self.can_motor = wpilib.CANTalon(15)

        self.sensor = Sensor(self.tote_motor, self.can_motor)
        
        self.tote_forklift = ToteForklift(self.tote_motor,self.sensor,2)
        self.can_forklift = CanForklift(self.can_motor,self.sensor,3)
        
        
        self.calibrator = Calibrator(self.tote_forklift, self.sensor)
        
        self.next_pos = 1

                
        self.backSensor = SharpIRGP2Y0A41SK0F(6)
        
        self.drive = drive.Drive(self.robot_drive, self.gyro, self.backSensor)

        self.align = alignment.Alignment(self.sensor, self.tote_forklift, self.drive)
        
        
        self.components = {
            'tote_forklift': self.tote_forklift,
            'can_forklift': self.can_forklift,
            'drive': self.drive,
            'align': self.align,
            'sensors': self.sensor
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
        self.ui_joystick_tote_down = Button(self.ui_joystick, 4)
        self.ui_joystick_tote_up = Button(self.ui_joystick, 6)
        self.ui_joystick_can_up = Button(self.ui_joystick, 5)
        self.ui_joystick_can_down = Button(self.ui_joystick, 3)
        
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
            
            self.sensor.update()
            
            #self.calibrator.calibrate()
            
            self.drive.move(self.joystick1.getY(), self.joystick1.getX(), self.joystick2.getX(),True)
            
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
                self.drive.isTheRobotBackwards = False
                self.align.align()
            elif self.autoLift:
                if self.sensor.toteLimitL and self.sensor.toteLimitR:
                    self.tote_forklift.raise_forklift()

            if self.joystick2.getRawButton(11):
                self.drive.reset_gyro_angle()
                
            if self.joystick2.getRawButton(8):
                self.drive.wall_strafe(-.7)
            elif self.joystick2.getRawButton(9):
                self.drive.wall_strafe(.7)

            # REVERSE DRIVE#
            if self.reverseDirection.get():
                self.drive.switch_direction()

            if self.joystick1.getRawButton(10):
                self.sweeper_relay.set(RelayValue.kForward)
            elif self.joystick1.getRawButton(11):
                self.sweeper_relay.set(RelayValue.kReverse)
            else:
                self.sweeper_relay.set(RelayValue.kOff)
            
            if self.toteTo != self.oldTote:
                if self.toteTo == 0:
                    self.tote_forklift._set_position(0)
                elif self.toteTo == 1:
                    self.tote_forklift._set_position(1)
                elif self.toteTo == 2:
                    self.tote_forklift._set_position(2)
                elif self.toteTo == 3:
                    self.tote_forklift._set_position(3)
                elif self.toteTo == 4:
                    self.tote_forklift._set_position(4)
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
                elif self.canTo == 4:
                    self.can_forklift._set_position(4)  
                elif self.canTo == 2048:
                    self.can_forklift.set_pos_top()
                elif self.canTo == 7000:
                    self.can_forklift.set_pos_7000()
                    

            self.oldCan = self.canTo
            
            if self.reverseRobot != self.oldReverseRobot:
                if self.reverseRobot == 0:
                    self.drive.switch_direction()
            self.oldReverseRobot = self.reverseRobot
            
            self.ui_joystick_buttons()
            
            self.smartdashbord_update()
            self.update()
            
            
            # Replaces wpilib.Timer.delay()
            delay.wait()

    def smartdashbord_update(self):
        
        self.sd.putNumber('backSensorValue', self.backSensor.getDistance())

        self.sensor.update_sd()
        self.can_forklift.update_sd('Can Forklift')
        self.tote_forklift.update_sd('Tote Forklift')
        
        self.sd.putNumber('gyroAngle', self.gyro.getAngle())
  
        self.toteTo = self.sd.getInt('liftTo',self.toteTo)
        self.canTo = self.sd.getInt('binTo',self.canTo)
        self.autoLift = self.sd.getBoolean('autoLift', self.autoLift)
        self.reverseRobot = self.sd.getBoolean('reverseRobot',self.reverseRobot)
        
    def ui_joystick_buttons(self):
        
        if self.ui_joystick_can_down.get():
            self.can_forklift.set_pos_bottom()
        elif self.ui_joystick_can_up.get():
            self.can_forklift.set_pos_top()
            
        if self.ui_joystick_tote_down.get():
            self.tote_forklift.set_pos_bottom()
        elif self.ui_joystick_tote_up.get():
            self.tote_forklift.set_pos_top()
                            
    def update (self):
        for component in self.components.values():
            component.doit()

    def disabled(self):
        '''Called when the robot is in disabled mode'''

        self.logger.info("Entering disabled mode")
        
        while not self.isEnabled():
            self.sensor.update()
            self.smartdashbord_update()
            wpilib.Timer.delay(.01)

    def test(self):
        '''Called when the robot is in test mode'''
        while self.isTest() and self.isEnabled():
            wpilib.LiveWindow.run()
            wpilib.Timer.delay(.01)

if __name__ == '__main__':

    wpilib.run(MyRobot)
