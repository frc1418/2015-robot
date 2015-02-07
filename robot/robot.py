#!/usr/bin/env python3

import wpilib
import math
from components import drive
from components.forklift import tote_Forklift, can_Forklift
from common.distance_sensors import SharpIR2Y0A02, SharpIRGP2Y0A41SK0F, CombinedSensor
from wpilib.smartdashboard import SmartDashboard


class MyRobot(wpilib.SampleRobot):
    def robotInit(self):
        super().__init__()
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
        #CAMERA
        try:
            self.camera = wpilib.USBCamera()
            self.camera.startCapture()
            self.camServ = wpilib.CameraServer()
            self.camServ.startAutomaticCapture(self.camera)
        except:
            self.camera = None

        ##ROBOT DRIVE##
        self.robot_drive = wpilib.RobotDrive(self.lf_motor, self.lr_motor, self.rf_motor, self.rr_motor)
        self.robot_drive.setInvertedMotor(wpilib.RobotDrive.MotorType.kFrontRight, True)
        self.robot_drive.setInvertedMotor(wpilib.RobotDrive.MotorType.kRearRight, True)

        ##INITIALIZE SENSORS#


        #self.gyro = wpilib.Gyro(4)
        self.tote_motor = tote_Forklift(5, 1440, 2880, 4320)
        self.can_motor = can_Forklift(15, 1440, 2880, 4320, 5760)

        self.drive = drive.Drive(self.robot_drive,0)

        self.longDistanceL = SharpIR2Y0A02(0)
        self.longDistanceR = SharpIR2Y0A02(2)
        self.shortDistanceL = SharpIRGP2Y0A41SK0F(1)
        self.shortDistanceR = SharpIRGP2Y0A41SK0F(3)
        #self.combinedDistance = CombinedSensor(0,1)
        #self.combinedDistance2 = CombinedSensor(2,3)

        self.components = {
            'tote_Forklift': self.tote_motor,
            'can_Forklift': self.can_motor,
            'drive': self.drive
        }

        self.control_loop_wait_time = 0.025
        #self.automodes = AutonomousModeSelector('autonomous', self.components)



    def autonomous(self):
        self.automodes.run(self.control_loop_wait_time, self.update)

    def operatorControl(self):

        print("Entering Teleop")
        while self.isOperatorControl() and self.isEnabled():
            self.drive.move((self.joystick1.getY())**3, (self.joystick1.getX())**3, (self.joystick2.getX()) / 2)

            #tote forklift goes up
            if self.joystick1.getRawButton(2):
                self.tote_motor.set(.5)
            #tote forklift goes down
            elif self.joystick1.getRawButton(3):
                self.tote_motor.set(-.5)
            #can forklift goes down
            elif self.joystick2.getRawButton(3):
                self.can_motor.set(.5)
            #can forklift goes up
            elif self.joystick2.getRawButton(2):
                self.can_motor.set(-.5)

            else:
                self.tote_motor.set(0)
                self.can_motor.set(0)


            #INFARED DRIVE#
            if(self.joystick1.getTrigger()==1):
                self.drive.infrared_rotation(self.longDistance.getDistance(),self.longDistance.getDistance(),12)
                
            self.update()
            #self.smartdashbord_update()
            wpilib.Timer.delay(self.control_loop_wait_time)

    def smartdashbord_update(self):
        wpilib.SmartDashboard.putNumber('shortSensorValueL', self.shortDistanceL.getDistance())
        wpilib.SmartDashboard.putNumber('shortSensorValueR',self.shortDistanceR.getDistance())
        wpilib.SmartDashboard.putNumber('largeSensorValueL', self.longDistanceL.getDistance())
        wpilib.SmartDashboard.putNumber('largeSensorValueR', self.longDistanceR.getDistance())



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
