from robotpy_ext.autonomous import timed_state, StatefulAutonomous

# Only for auto complete #
from components.drive import Drive
from components.forklift import ToteForklift
from components.alignment import Alignment

class StackAutonomous(StatefulAutonomous):
    MODE_NAME = 'Stack Auto'
    DEFAULT = True
    
    drive = Drive
    tote_forklift = ToteForklift
    align = Alignment
    
    def initialize(self):
        self.register_sd_var('back', .5)
        self.register_sd_var('fwd', .5)
    
    def on_enable(self):
        super().on_enable()
        self.drive.reset_gyro_angle()
        
    def on_iteration(self, tm):
        super().on_iteration(tm)
        
        # This gets executed afterwards
        self.drive.angle_rotation(0)
    @timed_state(duration =.5, next_state='get_tote2', first=True)
    def calibrate(self, initial_call):
        if initial_call:
            self.tote_forklift.set_pos_stack1()
        if self.tote_forklift.isCalibrated:
            self.next_state('get_tote2')
    @timed_state(duration=1.3, next_state='reverse')
    def get_tote2(self, initial_call):
        if initial_call:
            self.align.align()
    @timed_state(duration=3, next_state='drop')
    def reverse(self):
        self.drive.move(self.back, 0, 0, 0)
    
    @timed_state(duration=1.3, next_state='strafeRight')
    def drop(self):
        self.tote_forklift.set_pos_bottom()
    
    @timed_state(duration = 2, next_state='get_tote3')
    def strafeRight(self):
        self.drive.move(0, 1, 0, 0)
    
    @timed_state(duration = 3, next_state='get_tote4')
    def get_tote3(self):
        self.align.align()
    
    @timed_state(duration = 1.3, next_state='reverse2')
    def get_tote4(self):
        self.align.align()
        
    @timed_state(duration = 3, next_state='strafe')
    def reverse2(self):
        self.drive.move(self.back, 0, 0, 0)
    
    @timed_state(duration=1)
    def strafe(self):
        self.drive.move(0, -1, 0, 0)