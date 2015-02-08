import wpilib

class SharpIR2Y0A02:
    #large Distance
    def __init__(self,num):
        self.Distance = wpilib.AnalogInput(num)
        
    def getDistance(self):
        return max(  min(  ((  max(self.Distance.getVoltage(),0.00001)/22.73)**(1/-0.7533))  ,200)  ,30)
    def getVoltage(self):
        return self.Distance.getVoltage()

class SharpIRGP2Y0A41SK0F:
    #short Distance
    def __init__(self,num):
        self.Distance = wpilib.AnalogInput(num)

    def getDistance(self):
        return max(  min(    ((  max(self.Distance.getVoltage(),0.00001)/7.330)**(1/-0.7685))  ,35)  ,4)
    def getVoltage(self):
        return self.Distance.getVoltage()

class CombinedSensor:
    def __init__(self, longDist, longOff, shortDist, shortOff):
        self.longDistance = longDist
        self.shortDistance = shortDist
        self.longOff = longOff
        self.shortOff = shortOff
        
    def getDistance(self):
        
        long = self.longDistance.getDistance()
        short = self.shortDistance.getDistance()
        
        if short < 30:
            return short - self.shortOff
        else:
            return long - self.longOff
