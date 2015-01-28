import wpilib

class Forklift (object):
    def __init__ (self, toteMotor,canMotor ):
        self.tote_motor = toteMotor
        self.canMotor = canMotor
        self.canPosition = 0
        self.totePosition = 0
   
    def setCanLift(self, pos):
        self.canPosition = pos
   
    def setToteLift(self, pos):
        self.totePosition = pos

    def doit(self):
        self.canMotor.set(self.canPosition)
        self.tote_motor.set(self.totePosition)
        
