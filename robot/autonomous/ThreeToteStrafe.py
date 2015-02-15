from robotpy_ext.autonomous import timed_state, StatefulAutonomous
# Only for auto complete #
from components.drive import Drive
from components.alignment import Alignment
from components.forklift import ToteForklift
class ThreeToteStrafe(StatefulAutonomous):
    MODE_NAME = 'Three Totes Strafe'
    DEFAULT = True
    
    drive = Drive
    align = Alignment
    tote_forklift = ToteForklift
    
    def initialize(self):
        self.register_sd_var('over', -.8)
        self.register_sd_var('move_fwd', -.3)
        self.register_sd_var('tote_adjust', .15)
        self.register_sd_var('final_fwd', -.6)
    
    def on_enable(self):
        super().on_enable()
        self.drive.reset_gyro_angle()
        
    def on_iteration(self, tm):
        super().on_iteration(tm)
        
        # This gets executed afterwards
        self.drive.angle_rotation(0)
        
    #
    # First tote operations
    #
    
    @timed_state(duration=1.5, next_state='lift_tote1', first=True)
    def get_tote1(self, initial_call):
        '''This method will drive at .1 until the robot hits the tote'''
        
        if initial_call:
            self.tote_forklift.set_pos_bottom()
        
        self.drive.move(self.move_fwd, 0, 0)
        
        if self.align.is_against_tote(): 
            self.next_state('lift_tote1')
    
    
    @timed_state(duration=.75, next_state='wait_tote1')
    def lift_tote1(self, state_tm, initial_call):
        '''lifts tote until it is above the can'''
        
        if initial_call:
            self.tote_forklift.set_pos_stack2()
            
        if state_tm > .4:
            self.drive.move(self.tote_adjust, 0, 0)
    
    @timed_state(duration=3, next_state='strafe_can1')
    def wait_tote1(self):
    
        self.drive.wall_goto()
        
        if self.tote_forklift.on_target():
            self.next_state('strafe_can1')
    
    
    @timed_state(duration=1, next_state = 'go_until_tote2')
    def strafe_can1(self):
        '''strafes over for n seconds'''
        self.drive.wall_strafe(self.over)
    
    #
    # Second tote operations
    #
    
    @timed_state(duration=2, next_state='wait_forklift_tote2')
    def go_until_tote2(self, initial_call):
        '''moves the rest of the way to the crate until the sensors have a reading'''
        
        if initial_call:
            self.tote_forklift.set_pos_stack1()
        
        self.drive.wall_strafe(self.over)
        
        if self.align.is_in_range():
            if self.tote_forklift.on_target():
                self.next_state('get_tote2')
            else:
                self.next_state('wait_forklift_tote2')
   
    @timed_state(duration=1, next_state='get_tote2')
    def wait_forklift_tote2(self):
        if self.tote_forklift.on_target():
            self.next_state('get_tote2')
    
    @timed_state(duration=1.5, next_state='lift_tote2')
    def get_tote2(self, initial_call):
        '''This method will drive until the robot hits the tote'''
        
        self.drive.move(self.move_fwd, 0, 0)
        
        if self.align.is_against_tote(): 
            self.next_state('lift_tote2')
    
    
    @timed_state(duration=.75, next_state='wait_tote2')
    def lift_tote2(self, state_tm, initial_call):
        '''lifts tote until it is above the can'''
        
        if initial_call:
            self.tote_forklift.set_pos_stack4()
            
        if state_tm > .4:
            self.drive.move(self.tote_adjust, 0, 0)
    
    @timed_state(duration=3, next_state='strafe_can2')
    def wait_tote2(self):
    
        self.drive.wall_goto()
        
        if self.tote_forklift.on_target():
            self.next_state('strafe_can2')
    
    
    @timed_state(duration=1, next_state = 'go_until_tote3')
    def strafe_can2(self):
        '''strafes over for n seconds'''
        self.drive.wall_strafe(self.over)
   
    #
    # Third tote operations
    #
    
    @timed_state(duration=2, next_state='wait_forklift_tote2')
    def go_until_tote3(self, initial_call):
        '''moves the rest of the way to the crate until the sensors have a reading'''
        
        if initial_call:
            self.tote_forklift.set_pos_stack2()
        
        self.drive.wall_strafe(self.over)
        
        if self.align.is_in_range():
            self.next_state('drive_forward')
    
    #
    # Final stretch
    #
  
    
    @timed_state(duration=2, next_state='drop')
    def drive_forward(self, initial_call):
        '''pushes 3rd tote into the auto zone'''
        
        if initial_call:
            self.tote_forklift.set_pos_bottom()
        
        self.drive.move(self.final_fwd, 0, 0)
    
    
    @timed_state(duration=1, next_state = 'reverse')
    def drop(self, initial_call):
        '''lowers the totes onto a stack'''
        if initial_call:
            self.tote_forklift.set_pos_bottom()
        
        if self.tote_forklift.on_target():
            self.next_state('reverse')
    
    
    @timed_state(duration = .75)
    def reverse(self):
        '''backs up so we aren't touching'''
        self.drive.move(.2,0,0)