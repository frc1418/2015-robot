import wpilib

class tote_Forklift (object):
    def __init__ (self, toteMotor):
        self.tote_motor = toteMotor
        self.totePosition = self.tote_motor.getEncPosition()
        self.zero=self.totePosition
        self.lim1 =  wpilib.DigitalInput(1)
        self.lim2 = wpilib.DigitalInput(2)
        self.toteCheckTimer = wpilib.Timer()
        self.setpoint=self.totePosition
        #toteMotor.setPID(p,i,d)
        Pn1=0
        P0=1
        P1=2
        P2=3
        P3=4
        
    def setLift(self, motor, position):
        motor = motor
        position = position
        motor.set(self.position)
    
    def zeroEnc(self):
        self.zero=self.canPosition
        
    def setSetPoint(self, point):
        self.setpoint = point
    
    def toteCheck(self):
        if(self.lim1.get() and self.lim2.get()):
            if not self.toteCheckTimer.get()>0:
                self.toteCheckTimer.start()
        if self.toteCheckTimer.hasPeriodPassed(.5):
            self.toteCheckTimer.stop()
            self.toteCheckTimer.reset()
            return True
        return False
    
    def doit(self):
        self.tote_motor.set(self.setpoint)

class bin_Forklift (object):
    def __init__ (self, canMotor):
        self.can_Motor = canMotor
        self.canPosition = self.can_Motor.getEncPosition()
        self.zero=self.canPosition
        self.setpoint=self.canPosition
        
    def zeroEnc(self):
        self.zero=self.canPosition
        
    def setSetPoint(self, point):
        self.setpoint = point
        
    def setLift(self, motor, position):
        motor = motor
        position = position
        motor.set(self.position)

    def doit(self):
        self.can_Motor.set(self.setpoint)
    