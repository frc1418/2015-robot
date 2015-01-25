import wpilib
class SharpIR2Y0A02:
    #large Distance
    def __init__(self):
        self.largeDistance = wpilib.AnalogInput(1)
        self.largeDistance2 = wpilib.AnalogInput(3)
    def getDistance(self):
        return min(((max(0.00001,self.largeDistance.getVoltage()))/22.73)**(1/-0.7533)/2.54,1000)


class SharpIRGP2Y0A41SK0F:
    #short Distance
    def __init__(self):
        self.smallDistance2 = wpilib.AnalogInput(4)
        self.smallDistance = wpilib.AnalogInput(2)

    def getDistance(self):
        return min(((max(0.00001,self.smallDistance.getVoltage()))/7.330)**(1/-0.7685)/2.54,1000)