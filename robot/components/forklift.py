import wpilib

class Forklift (object):
    def __init__ (self, toteMotor,canMotor ):
        self.tote_motor = toteMotor
        self.canMotor = canMotor
   
    def setCanLift(self, pos):
        self.canPosition = pos
   
    def setToteLift(self, pos):
        self.position = pos

    def doit(self):
        self.canMotor.set(canPosition)
        self.tote_motor.set(self.position)
        
