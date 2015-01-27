import wpilib

class Forklift (object):
    def __init__ (self, liftmotor):
        self.lift_motor = liftmotor
        
       
        (distance/rotationDistance)
    def setLift(self, pos):
        self.position = pos
        self.position = distance*1440/RotationDistance

    def doit(self):
        self.lift_motor.set(self.position)
        
