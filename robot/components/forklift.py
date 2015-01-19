class Forklift (object):
    def __init__ (self, liftmotor):
        self.lift_motor = liftmotor
    def setLift(self, speed):
        self.speed = speed
    def doit(self):
        self.lift_motor.set(self.speed)