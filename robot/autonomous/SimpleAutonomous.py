from robotpy_ext.autonomous import timed_state, StatefulAutonomous
from common.custom_stateful import SensorStatefulAutonomous

from components.drive import Drive
from components.forklift import CanForklift, ToteForklift
from components.alignment import Alignment

class CanAutonomous(StatefulAutonomous):
    
    MODE_NAME='Can Pickup'
    
    can_forklift = CanForklift
    drive = Drive
    
    def initialize(self):
        pass
    
    @timed_state(duration=2, next_state='strafe', first=True)
    def can_lift(self):
        self.can_forklift.set_pos_stack2()
        self.drive.angle_rotation(0)
    
    @timed_state(duration=1, next_state='drive_forward')
    def strafe(self):
        self.drive.move(0, .5, 0)
        self.drive.angle_rotation(0)
    
    @timed_state(duration=4,next_state='turn')
    def drive_forward(self):
        self.drive.move(-.25, 0, 0)
        self.drive.angle_rotation(0)
    
    @timed_state(duration=4)
    def turn(self):
        #self.drive.move(-.1, 0, .3)
        self.drive.angle_rotation(90)
        
    
class ToteAutonomous(StatefulAutonomous):
    
    MODE_NAME='Tote Pickup'
    DEFAULT = False
    
    tote_forklift = ToteForklift
    drive = Drive
    
    def initialize(self):
        pass
    
    @timed_state(duration=.5, next_state='get_tote1', first=True)
    def calibrate(self, initial_call):
        
        if initial_call:
            self.tote_forklift.set_pos_bottom()
            
        if self.tote_forklift.isCalibrated:
            self.next_state('get_tote1')
        
    @timed_state(duration=1, next_state='wait_tote1')
    def get_tote1(self):
        self.drive.move(-.3, 0, 0)
        self.tote_forklift.set_pos_stack1()
    
    @timed_state(duration=2, next_state='goto_tote2')
    def wait_tote1(self):
        self.drive.move(0, 0, 0)
        
    @timed_state(duration=1, next_state='get_tote2')
    def goto_tote2(self):
        self.drive.move(-.3, 0, 0)
        
    @timed_state(duration=1, next_state='backwards')
    def get_tote2(self):
        self.drive.move(-.3, 0, 0)
        self.tote_forklift.set_pos_stack2()
    
    @timed_state(duration=4.3)
    def backwards(self):
        '''Get into the autonomous zone'''
        self.drive.move(.25, 0, 0)

class DualAutonomous(StatefulAutonomous):
    
    MODE_NAME = 'Dual Auto'
    DISABLED = True # let's not bother with this
    
    tote_forklift = ToteForklift  
    can_forklift = CanForklift
    
    drive = Drive
    align = Alignment
    
    def initialize(self):
        pass
    def on_enable(self):
        StatefulAutonomous.on_enable(self)
    def on_iteration(self, tm):
        super().on_iteration(tm)
    
    @timed_state(duration = 1, next_state='align', first = True)
    def can_lift(self):
        self.can_forklift.set_pos_stack1()
    @timed_state(duration=1, next_state='strafe')
    def align(self):
        self.align.align()
    @timed_state(duration= 3, next_state='drop_tote')
    def strafe(self):
        self.drive.move(0, -1, 0)
    @timed_state(duration=1, next_state='drive')
    def drop_tote(self):
        self.tote_forklift.set_pos_bottom()
    @timed_state(duration=2, next_state='drop_can')
    def drive(self):
        self.drive.move(1,0, 0)
    @timed_state(duration=2, next_state='reverse')
    def drop_can(self):
        self.can_forklift.set_pos_bottom()
    @timed_state(duration=1)
    def reverse(self):
        self.drive.move(-1, 0, 0)
    
    
    
    
    
    
    
    
    