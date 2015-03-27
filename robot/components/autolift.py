'''
Created on Mar 22, 2015

@author: winterst
'''
import wpilib

class Autolift(object):
    
    def __init__(self, sensor, forklift):
        
        self.allowLift = True
        
        self.sensors = sensor
        self.tote_forklift = forklift
        
        self.switch_timer = wpilib.Timer()
        self.allow_timer = wpilib.Timer()
        
        self.last_allow = None
    
    def get_switch(self):
        '''Only return true if the switch has been pressed for more than 40ms'''
        
        if self.sensors.is_against_tote():
            
            if not self.switch_timer.running:
                self.switch_timer.start()
            
            if self.switch_timer.hasPeriodPassed(0.04):
                self.switch_timer.stop()
                return True
        else:
            if self.switch_timer.running:
                self.switch_timer.stop()
            
        return False
    
    def autolift(self):
        if self.allowLift and self.get_switch():
            self.allowLift = False
            self.tote_forklift.raise_forklift()
        
    def doit(self):

        if not self.allowLift:
            
            if not self.allow_timer.running:
                self.allow_timer.start()
                
            if self.allow_timer.hasPeriodPassed(1.5):
                self.allow_timer.stop()
                self.allowLift = True

