from robotpy_ext.autonomous import timed_state, StatefulAutonomous

# Only for auto complete #
from components.drive import Drive
from components.forklift import ToteForklift
from components.alignment import Alignment
import wpilib

class StackAutonomous(StatefulAutonomous):
    MODE_NAME = 'Stack Auto'
    DEFAULT = True
    
    drive = Drive
    tote_forklift = ToteForklift
    align = Alignment
    
    
    def initialize(self):
        self.register_sd_var('back', .5)
        self.register_sd_var('fwd', .5)
        
        self.angRot = 0
    
    def on_enable(self):
        super().on_enable()
        self.drive.reset_gyro_angle()
        
    def on_iteration(self, tm):
        super().on_iteration(tm)
        
        # This gets executed afterwards
        self.drive.angle_rotation(self.angRot)
    
    @timed_state(duration=1.2, next_state='get_tote2', first=True)
    def calibrate(self, initial_call):
        if initial_call:
            self.tote_forklift.set_pos_stack1()
            
    @timed_state(duration=1.5, next_state='reverse')
    def get_tote2(self, initial_call):
        if initial_call:
            self.align.align()
    
    @timed_state(duration=1.2, next_state='strafe')
    def reverse(self):
            self.drive.move(.2, 0,0)
    
    @timed_state(duration = 2, next_state='get_tote_3')
    def strafe(self):
            self.drive.move(0,-1,0)
    
    @timed_state(duration=1.3, next_state='get_tote_4')
    def get_tote_3(self, initial_call):
        if initial_call:
            self.align.align()
            
    @timed_state(duration = 2, next_state='to_auto_zone')
    def get_tote_4(self, initial_call):
        if initial_call:
            self.align.align()
            
    @timed_state(duration = .5, next_state='rotate')
    def to_auto_zone(self):
            self.drive.move(.7, 0, 0)
    
    @timed_state(duration = .5, next_state='drop')
    def rotate(self):
        self.angRot = -90
        if self.drive.return_gyro_angle() < -85:
            self.next_state('drop')
    
    @timed_state(duration = 5)
    def drop(self, initial_call):
        if initial_call:
            self.tote_forklift.set_pos_bottom()
        self.drive.move(-.1, 0, 0) #based on driving experience the robot can't go over the scoring platform at this speed, so it should just drive up and stay against it
    
    
    