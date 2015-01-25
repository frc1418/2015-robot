import wpilib
class SharpIR2Y0A02:
    #large Distance
    def __init__(self,num):
        self.Distance = wpilib.AnalogInput(num)
        
    def getDistance(self):
        return min(((max(0.00001,self.Distance.getVoltage()))/22.73)**(1/-0.7533),1000)


class SharpIRGP2Y0A41SK0F:
    #short Distance
    def __init__(self,num):
        self.Distance = wpilib.AnalogInput(num)

    def getDistance(self):
        return min(((max(0.00001,self.Distance.getVoltage()))/7.330)**(1/-0.7685),1000)
