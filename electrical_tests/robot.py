#!/usr/bin/env python3

import wpilib
from wpilib.cantalon import CANTalon

class MyRobot(wpilib.SampleRobot):
    
    def robotInit(self):
        self.largeDistance = wpilib.AnalogInput(0)
        self.largeDistance2 = wpilib.AnalogInput(1)
        self.smallDistance = wpilib.AnalogInput(2)
        self.smallDistance2 = wpilib.AnalogInput(3)
        self.accelerometer = wpilib.BuiltInAccelerometer(range=2)
        #self.pot = wpilib.AnalogInput(2)
        self.timercounter = 0
        self.XOfRobot=0
        self.YOfRobot=0
        
        self.talon = wpilib.CANTalon(15)
        self.talon.changeControlMode(CANTalon.ControlMode.Position)
        self.talon.setFeedbackDevice(CANTalon.FeedbackDevice.QuadEncoder)
        self.talon.setP(1)
        self.joystick = wpilib.Joystick(0)
        wpilib.SmartDashboard.putNumber('P', 1)
        self.talon.setSensorPosition(0)
        wpilib.SmartDashboard.putNumber('Pos', 50)

        
    def disabled(self):
        #self.operatorControl()
        self.talon.setSensorPosition(0)
    
    def operatorControl(self):
        #self.myRobot.setSafetyEnabled(True)
        
        while self.isOperatorControl() and self.isEnabled():    
            wpilib.SmartDashboard.putNumber('Accelerometer X', self.accelerometer.getX())
            wpilib.SmartDashboard.putNumber('Accelerometer Y', self.accelerometer.getY())
            #wpilib.SmartDashboard.putNumber('Accelerometer Z', self.accelerometer.getZ())
            
            #large distance 22.73x^-0.7533
            #small distance 7.330x^-0.7685
            self.fixedLargeValue = ((max(0.00001,self.largeDistance.getVoltage()))/22.73)**(1/-0.7533)/2.54
            self.fixedLargeValue2 = ((max(0.00001,self.largeDistance2.getVoltage()))/22.73)**(1/-0.7533)/2.54
            self.fixedSmallValue = ((max(0.00001,self.smallDistance.getVoltage()))/7.330)**(1/-0.7685)/2.54
            self.fixedSmallValue2 = ((max(0.00001,self.smallDistance2.getVoltage()))/7.330)**(1/-0.7685)/2.54

            wpilib.SmartDashboard.putNumber('largeSensorValue', self.fixedLargeValue)
            wpilib.SmartDashboard.putNumber('largeSensorValue2', self.fixedLargeValue2)
            
            wpilib.SmartDashboard.putNumber('smallSensorValue', self.fixedSmallValue)
            wpilib.SmartDashboard.putNumber('smallSensorValue2', self.fixedSmallValue2)
            
            #wpilib.SmartDashboard.putNumber('Potentiometer', self.pot.getVoltage())
            wpilib.SmartDashboard.putNumber('Enc', self.talon.getEncPosition())
            wpilib.SmartDashboard.putNumber('largeSensorValue', self.fixedLargeValue)
            wpilib.SmartDashboard.putNumber('smallSensorValue', self.fixedSmallValue)
            if wpilib.SmartDashboard.getNumber('P') is not self.talon.getP():
                print("Changing P")
                self.talon.setP(wpilib.SmartDashboard.getNumber('P'))
            self.talon.set(wpilib.SmartDashboard.getNumber('Pos')*-1)
                
            

            
            #self.XOfRobot=self.XOfRobot+(self.accelerometer.getX()*.5*(self.timercounter**2))
            #self.YOfRobot=self.YOfRobot+(self.accelerometer.getY()*.5*(self.timercounter**2))
            
            self.timercounter=self.timercounter+0.005
            wpilib.Timer.delay(0.005)
    '''        
    def convertVoltageToDistance (self, voltage, SmallerSensor):
        if(SmallerSensor):
            return ((self.voltage)/9.042)**0.8605
        else:
            return ((self.voltage)/22.73)**0.03081
        
    '''
if __name__ == '__main__':
    wpilib.run(MyRobot)
