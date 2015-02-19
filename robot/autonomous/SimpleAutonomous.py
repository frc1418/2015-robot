from robotpy_ext.autonomous import timed_state, StatefulAutonomous

from components.drive import Drive
from components.forklift import CanForklift, ToteForklift
from components.alignment import Alignment
class CanAutonomous(StatefulAutonomous):
    MODE_NAME='Can Auto'
    DEFAULT=False
    
    can_forklift = CanForklift
    drive = Drive
    def initialize(self):
        pass
    def on_enable(self):
        StatefulAutonomous.on_enable(self)
    def on_iteration(self, tm):
        super().on_iteration(tm)
        
    @timed_state(duration=2, next_state='drive_forward', first=True)
    def can_lift(self):
        self.can_forklift.set_pos_stack2()
    
    @timed_state(duration=3)
    def drive_forward(self):
        self.drive.move(1, 0,0,)
        
    
class ToteAutonomous(StatefulAutonomous):
    MODE_NAME='Tote Auto'
    DEFAULT=False
    
    tote_forklift = CanForklift
    drive = Drive
    def initialize(self):
        pass
    def on_enable(self):
        StatefulAutonomous.on_enable(self)
    def on_iteration(self, tm):
        super().on_iteration(tm)
    @timed_state(duration=3,first=True)   
    def drive_forward(self):
        self.drive.move(1, 0,0,)
class DualAutonomous(StatefulAutonomous):
    MODE_NAME = 'Dual Auto'
    DEFAULT= False
    
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
    
    
    
    
    
    
    
    
    