import wpilib
class Forklift (object):
    def __init__ (self):
        pass
    
    def set(self, setpoint):
        self.setpoint = setpoint
    
    def zeroEnc(self):
        self.zero=self.encoderToInch(CANMotor.getEncPosition())
    
    def doit(self):
        self.CANMotor.set(self.inchToEncoder(self.position))



class tote_Forklift (Forklift):
    def __init__ (self, CANMotor):
        self.CANMotor=CANMotor
        self.CANMotor = CANMotor
        self.setpoint=CANMotor.getEncPosition()
        self.position = (self.setpoint*1440)/5.75
        #List of positions in inches from 0
        Pn1=0
        P0=1
        P1=2
        P2=3
        P3=4
        
        
        self.lim1 =  wpilib.DigitalInput(1)
        self.lim2 = wpilib.DigitalInput(2)
        self.toteCheckTimer = wpilib.Timer()
    
    def inchToEncoder(self,c):
        return (c*1440)/5.75   
    def encoderToInch(self,c):
        return (c*5.75)/1440 
    
    def toteCheck(self):
        if(self.lim1.get() and self.lim2.get()):
            if not self.toteCheckTimer.get()>0:
                self.toteCheckTimer.start()
        else:
            self.toteCheckTimer.stop()
            self.toteCheckTimer.reset()
        if self.toteCheckTimer.hasPeriodPassed(.5):
            self.toteCheckTimer.stop()
            self.toteCheckTimer.reset()
            return True
        return False


class can_Forklift (Forklift):
    def __init__ (self, CANMotor):
        self.CANMotor = CANMotor
        self.setpoint=CANMotor.getEncPosition()
        self.position = (self.setpoint*1440)/9.625
        #List of positions in inches from 0
        P1=0
        P2=1
        P3=2
    
    def inchToEncoder(self,c):
        return (c*1440)/9.625
    def encoderToInch(self,c):
        return (c*9.625)/1440