from robotpy_ext.autonomous import timed_state, StatefulAutonomous
from common.custom_stateful import SensorStatefulAutonomous

from components.drive import Drive
from components.forklift import CanForklift, ToteForklift
from components.alignment import Alignment

class CanAutonomous(StatefulAutonomous):
    '''Picks up can and puts it into autozone'''
    MODE_NAME='Can Pickup'
    
    can_forklift = CanForklift
    drive = Drive
    
    def initialize(self):
        pass
    
    @timed_state(duration=2, next_state='strafe', first=True)
    def can_lift(self):
        '''lift can'''
        self.can_forklift.set_pos_stack2()
        self.drive.angle_rotation(0)
    
    @timed_state(duration=1, next_state='drive_forward')
    def strafe(self):
        '''strafe right so we don't go over edge of scoring platform'''
        self.drive.move(0, .5, 0)
        self.drive.angle_rotation(0)
    
    @timed_state(duration=4,next_state='turn')
    def drive_forward(self):
        '''drive forward over scoring platform'''
        self.drive.move(-.25, 0, 0)
        self.drive.angle_rotation(0)
    
    @timed_state(duration=4)
    def turn(self):
        '''rotate so we are fully contained in auto zone'''
        #self.drive.move(-.1, 0, .3)
        self.drive.angle_rotation(90)
        
    
class ToteAutonomous(StatefulAutonomous):
    '''Gets two grey totes and drives back into autozone'''
    MODE_NAME='Tote Pickup'
    DEFAULT = False
    
    tote_forklift = ToteForklift
    drive = Drive
    
    def initialize(self):
        pass
    
    @timed_state(duration=.5, next_state='get_tote1', first=True)
    def calibrate(self, initial_call):
        '''calibrate tote forklift'''
        if initial_call:
            self.tote_forklift.set_pos_bottom()
            
        if self.tote_forklift.isCalibrated:
            self.next_state('get_tote1')
        
    @timed_state(duration=1, next_state='wait_tote1')
    def get_tote1(self):
        '''drive forward and lift 1st tote'''
        self.drive.move(-.3, 0, 0)
        self.tote_forklift.set_pos_stack1()
    
    @timed_state(duration=2, next_state='goto_tote2')
    def wait_tote1(self):
        '''pause for two seconds to let forklift raise'''
        self.drive.move(0, 0, 0)
        
    @timed_state(duration=1, next_state='get_tote2')
    def goto_tote2(self):
        '''drive into second tote'''
        self.drive.move(-.3, 0, 0)
        
    @timed_state(duration=1, next_state='backwards')
    def get_tote2(self):
        '''pickup second tote'''
        self.drive.move(-.3, 0, 0)
        self.tote_forklift.set_pos_stack2()
    
    @timed_state(duration=4.3)
    def backwards(self):
        '''Get into the autonomous zone'''
        self.drive.move(.25, 0, 0)

    
    
    
    
    
    
    