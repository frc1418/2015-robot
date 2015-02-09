import wpilib

class SharpIR2Y0A02:
    #large Distance
    def __init__(self,num):
        self.Distance = wpilib.AnalogInput(num)
        
    def getDistance(self):
        #13.40x^(-0.7806)
        return max(  min(  ((  max(self.Distance.getVoltage(),0.00001)/13.40)**(1/-0.7806))  ,200)  ,30)
    def getVoltage(self):
        return self.Distance.getVoltage()

class SharpIRGP2Y0A41SK0F:
    #short Distance
    def __init__(self,num):
        self.Distance = wpilib.AnalogInput(num)

    def getDistance(self):
        #9.592x^(-0.8819)
        return max(  min(    ((  max(self.Distance.getVoltage(),0.00001)/9.592)**(1/-0.8819))  ,35)  ,4)
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
