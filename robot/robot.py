#!/usr/bin/env python3

import wpilib
RelayValue = wpilib.Relay.Value

from components import drive, alignment, autolift
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
        
        self.pinServo = wpilib.Servo(6)
        
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
        
        self.tote_motor = wpilib.CANTalon(5)
        self.can_motor = wpilib.CANTalon(15)

        self.sensor = Sensor(self.tote_motor, self.can_motor)
        
        self.tote_forklift = ToteForklift(self.tote_motor,self.sensor,2)
        self.can_forklift = CanForklift(self.can_motor,self.sensor,3)
        
        self.calibrator = Calibrator(self.tote_forklift, self.sensor)

        self.autoLifter = autolift.Autolift(self.sensor, self.tote_forklift) 
        
        self.backSensor = SharpIRGP2Y0A41SK0F(6)
        
        self.drive = drive.Drive(self.robot_drive, self.gyro, self.backSensor)

        self.align = alignment.Alignment(self.sensor, self.tote_forklift, self.drive, self.autoLifter)
        
        # These must have a doit function
        self.components = {
            'tote_forklift': self.tote_forklift,
            'can_forklift': self.can_forklift,
            'drive': self.drive,
            'autolift': self.autoLifter,
            'align': self.align,
            'sensors': self.sensor
        }
        
        # These do not, and get passed to autonomous mode
        self.auton_components = {
            'pin_servo': self.pinServo
        }
        
        self.auton_components.update(self.components)
        
        # #Defining Buttons##
        self.canUp = Button(self.joystick1,3)
        self.canDown = Button(self.joystick1,2)
        self.canTop = Button(self.joystick1,6)
        self.canBottom = Button(self.joystick1, 7)
        self.toteUp = Button(self.joystick2, 3)
        self.toteDown = Button(self.joystick2, 2)
        self.toteTop = Button(self.joystick2, 6)
        self.toteBottom = Button(self.joystick2, 7)
        
        self.reverseDirection = Button(self.joystick1, 1)
        
        # Secondary driver's joystick
        self.ui_joystick_tote_down = Button(self.ui_joystick, 4)
        self.ui_joystick_tote_up = Button(self.ui_joystick, 6)
        self.ui_joystick_can_up = Button(self.ui_joystick, 5)
        self.ui_joystick_can_down = Button(self.ui_joystick, 3)
        
        self.oldReverseRobot = False
        
        self.toteTo = self.sd.getAutoUpdateValue('toteTo', -1)
        self.canTo = self.sd.getAutoUpdateValue('canTo', -1)
        self.reverseRobot = self.sd.getAutoUpdateValue('reverseRobot',False)
        self.autoLift = self.sd.getAutoUpdateValue('autoLift', False)
        
        # If set, this means we go forward and try to pickup the three totes
        # that we've deposited in autonomous mode
        self.autoPickup = self.sd.getAutoUpdateValue('autoPickup', False)
        self.autoPickupSpeed = self.sd.getAutoUpdateValue('autoPickupSpeed', -0.2)
        
        
        self.control_loop_wait_time = 0.025
        self.automodes = AutonomousModeSelector('autonomous', self.auton_components)
        
    def autonomous(self):
        
        self.sd.putBoolean('autoPickup', False)
        
        self.automodes.run(self.control_loop_wait_time, self.update)
    
    
    def operatorControl(self):
        
        self.can_forklift.set_manual(0)
        self.tote_forklift.set_manual(0)
        
        delay = PreciseDelay(self.control_loop_wait_time)

        self.logger.info("Entering teleop mode")
            
        while self.isOperatorControl() and self.isEnabled():
            
            self.sensor.update()
            
            #self.calibrator.calibrate()
            
            try:
                self.drive.move(self.joystick1.getY(), self.joystick1.getX(), self.joystick2.getX(),True)
            except:
                if not self.isFMSAttached():
                    raise
            #
            # Can forklift controls
            #

            try:
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
                    
            except:
                if not self.isFMSAttached():
                    raise
            
            try:
                if self.canTo.value >= 0:
                    canTo = int(self.canTo.value)
                    if canTo == 2048:
                        self.can_forklift.set_pos_top()
                    elif canTo == 7000:
                        self.can_forklift.set_pos_7000()
                    else:
                        self.can_forklift._set_position(canTo)
                    
                    self.sd.putNumber('canTo', -1)
                    
            except:
                if not self.isFMSAttached():
                    raise
                
            ## Tote forklift controls##

            try:
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
            except:
                if not self.isFMSAttached():
                    raise
            
            if self.toteTo.value >= 0:
                toteTo = int(self.toteTo.value)
                if toteTo == 2048:
                    self.tote_forklift.set_pos_top()
                else:
                    self.tote_forklift._set_position(toteTo)
                
                self.sd.putDouble('toteTo', -1)
            
            #
            # Driver-enabled automatic alignment code
            #
            
            try:
                if self.joystick2.getTrigger():
                #    self.drive.isTheRobotBackwards = False
                #    self.align.align()
                #elif self.autoLift.value:
                    self.autoLifter.autolift()
            except:
                if not self.isFMSAttached():
                    raise            
            
            #
            # Utilities
            #
            
            try:
                if self.joystick2.getRawButton(10):
                    self.pinServo.set(0)
                if self.joystick2.getRawButton(11):
                    self.pinServo.set(1)
            except:
                if not self.isFMSAttached():
                    raise
            try:
                if self.joystick2.getRawButton(11):
                    self.drive.reset_gyro_angle()
            except:
                if not self.isFMSAttached():
                    raise        
            
            try:
                if self.joystick2.getRawButton(8):
                    self.drive.wall_strafe(-.7)
                elif self.joystick2.getRawButton(9):
                    self.drive.wall_strafe(.7)
            except:
                if not self.isFMSAttached():
                    raise
                 
            
            #
            # Reverse drive
            #
            
            try:
                if self.reverseDirection.get():
                    self.drive.switch_direction()
            except:
                if not self.isFMSAttached():
                    raise
            
            try:
                if self.reverseRobot.value != self.oldReverseRobot:
                    if self.reverseRobot.value == 0:
                        self.drive.switch_direction()
                self.oldReverseRobot = self.reverseRobot.value
            except:
                if not self.isFMSAttached():
                    raise
            
            #
            # At the end of autonomous mode, pick up the three bins in
            # front of us if enabled
            #
            
            #if self.autoPickup.value:
            #    try:
            #        # End autopickup when the driver gives joystick input
            #        if abs(self.joystick1.getX())>.1 or abs(self.joystick1.getY())>.1 or abs(self.joystick2.getX())>.1:
            #            self.sd.putBoolean('autoPickup', False)
            #        else:
            #            if not self.sensor.is_against_tote():
            #                self.drive.move(self.autoPickupSpeed.value, 0, 0)
            #            else:
            #                # Move slow once we hit the totes
            #                self.drive.move(-0.1, 0, 0)
            #            
            #            self.autoLifter.autolift()
            #        
            #    except:
            #        self.sd.putBoolean('autoPickup', False)
            #        if not self.isFMSAttached():
            #            raise
                
            try:    
                self.ui_joystick_buttons()
            except:
                if not self.isFMSAttached():
                    raise
            
            try:
                self.smartdashboard_update()
            except:
                if not self.isFMSAttached():
                    raise
            
            try:
                self.update()
            except:
                if not self.isFMSAttached():
                    raise
            
            # Replaces wpilib.Timer.delay()
            delay.wait()

    def smartdashboard_update(self):
        
        self.sensor.update_sd()
        self.can_forklift.update_sd('Can Forklift')
        self.tote_forklift.update_sd('Tote Forklift')
        
        self.sd.putNumber('backSensorValue', self.backSensor.getDistance())
        self.sd.putNumber('gyroAngle', self.gyro.getAngle())
  
        
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
            self.smartdashboard_update()
            wpilib.Timer.delay(.01)

    def test(self):
        '''Called when the robot is in test mode'''
        while self.isTest() and self.isEnabled():
            wpilib.LiveWindow.run()
            wpilib.Timer.delay(.01)
            
    def isFMSAttached(self):
        return self.ds.isFMSAttached()

if __name__ == '__main__':

    wpilib.run(MyRobot)
