import wpilib
class tote_Forklift (object):
    def __init__ (self, Motor):
        self.forklift=forklift
        

        self.lim1 =  wpilib.DigitalInput(1)
        self.lim2 = wpilib.DigitalInput(2)
        self.toteCheckTimer = wpilib.Timer()
        #toteMotor.setPID(p,i,d)
        Pn1=0
        P0=1
        P1=2
        P2=3
        P3=4
        
        
    def toteCheck(self):
        if(self.lim1.get() and self.lim2.get()):
            if not self.toteCheckTimer.get()>0:
                self.toteCheckTimer.start()
        if self.toteCheckTimer.hasPeriodPassed(.5):
            self.toteCheckTimer.stop()
            self.toteCheckTimer.reset()
            return True
        return False


class bin_Forklift (object):
    def __init__ (self, Motor):
        self.forklift=forklift(Motor)
        P1=0
        P2=1
        P3=2
class Forklift (object):
    def __init__ (self, CANMotor):
        self.can_Motor = canMotor
        self.zero=self.canPosition
        self.setpoint=self.canPosition
        
    def setLift(self, motor, position):
        motor = motor
        position = position
        motor.set(self.position)
    
    def zeroEnc(self):
        self.zero=self.canPosition
    
    def doit(self):
        self.tote_motor.set(self.setpoint)
