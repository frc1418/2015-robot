import wpilib

class Forklift (object):
    def __init__ (self, toteMotor,canMotor ):
        self.tote_motor = toteMotor
        self.can_Motor = canMotor
        self.canPosition = self.can_Motor.getPosition()
        self.totePosition = self.tote_motor.getPosition()
   
    def setLift(self, motor, position):
        motor = motor
        position = position
        motor.set(self.position)

    def doit(self):
        #self.canMotor.set(self.canPosition)
        #self.tote_motor.set(self.totePosition)
        pass
        