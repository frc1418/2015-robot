from robotpy_ext.autonomous import timed_state, StatefulAutonomous

from components.drive import Drive
from components.forklift import CanForklift
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
    
    can_forklift = CanForklift
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
        
    