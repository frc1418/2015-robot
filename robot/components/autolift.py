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
        self.latest = None
        
        self.last_allow = None
        
    
    def get_switch(self):
        '''Only return true if the switch has been pressed for more than 40ms'''
        
        
        if self.sensors.is_against_tote():
            
            now = self.timer.getMsClock()
            
            if self.latest is None:
                self.latest = now
            
            if (now-self.latest) > 40:
                return True
        else:
            self.latest = None
            
        return False
    
    def autolift(self):
        if self.allowLift and self.get_switch():
            self.allowLift = False
            print("raising forklift")
            self.tote_forklift.raise_forklift()
        
    def doit(self):
        now = self.timer.getMsClock()

        if not self.allowLift:
            if self.last_allow is None:
                self.last_allow = now
                
            if now - self.last_allow > 1000:
                self.last_allow = None
                self.allowLift = True
                
        else:
            self.last_allow = None