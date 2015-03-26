'''
Created on Mar 22, 2015

@author: winterst
'''
import wpilib

class Autolift(object):
    
    def __init__(self, sensor, forklift):
        self.timer = wpilib.Timer()
        self.allowLift = True
        
        self.sensors = sensor
        self.tote_forklift = forklift
        self.latest = 0
        
    def get_switch(self):
        '''Returns the value of the button. If the button is held down, then
        True will only be returned once every 200ms'''
        
        now = self.timer.getMsClock()
        if(self.sensors.is_against_tote()):
            if (now-self.latest) > 40: 
                self.latest = now
                return True
        return False
    
    def autolift(self):
        if self.allowLift and self.get_switch():
            self.allowLift = False
            print("Auto lifting!")
            self.tote_forklift.raise_forklift()
        
    def doit(self):
        if not self.allowLift:
            self.allowLift = not self.sensors.is_against_tote()
    