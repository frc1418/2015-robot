import wpilib
class Forklift (object):
    def __init__ (self, port, ONE, TWO, THREE, FOUR = 0):
        self.one = ONE
        self.two = TWO
        self.three = THREE
        self.four = FOUR
        self.motor = wpilib.Talon(port)
        self.setpoint=0
    def set(self, setPoint):
        self.setpoint = setPoint
        
    def zeroEnc(self):
        if not first:
            if not self.lim1.get():
                self.motor.set(-1)
            else:
                self.motor.set(0)
                #self.motor.setSensorPosition(0)
            #self.motor.changeControlMode(CanTalon.ControlMode.Position)
            first = True
    
    def doit(self):
        #takes inches, gives motor encoder values
        self.motor.set(self.setpoint)

class tote_Forklift (Forklift):
    def __init__ (self, port, ONE,TWO,THREE,):
        Forklift.__init__(self, port, ONE,TWO,THREE)
        
        self.lim = wpilib.DigitalInput(1)
        
class can_Forklift (Forklift):
    def __init__ (self, port, ONE, TWO, THREE, FOUR):
        Forklift.__init__(self, port, ONE, TWO, THREE, FOUR)
        self.lim = wpilib.DigitalInput(2)
    
    