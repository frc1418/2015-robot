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
        self.register_sd_var('over', -.5)
        self.register_sd_var('backwards', .15)
        self.register_sd_var('fwd_min', -.2)
    
    def on_enable(self):
        super().on_enable()
        self.drive.reset_gyro_angle()
        
    def on_iteration(self, tm):
        super().on_iteration(tm)
        
        # This gets executed afterwards
        self.drive.angle_rotation(0)
    
    def strafe_left(self):
        
        y = (self.align.backSensor.getDistance() - 15.0)/50.0
        y = max(min(self.backwards, y), self.fwd_min)
        
        self.drive.move(y, self.over, 0)
        
    
    
    @timed_state(duration = 1,next_state='lift_tote_one', first=True)
    def go_until_limit(self):
        '''This method will drive at .1 until the robot hits the tote'''
        
        self.tote_forklift.set_pos_bottom()
        
        if self.align.is_against_tote(): 
            self.next_state('lift_tote_one')
        else:
            self.drive.move(-.1,0,0)
    
    
    @timed_state(duration=2, next_state='strafe_n')
    def lift_tote_one(self):
        '''lifts tote until it is above the can'''
        self.tote_forklift.set_pos_stack2()
        self.next_state('strafe_n')
    
    
    @timed_state(duration=2, next_state = 'go_until_sensors')
    def strafe_n(self):
        '''strafes over for n seconds'''
        self.strafe_left()
    
    
    @timed_state(duration=2, next_state='go_until_limit_two')
    def go_until_sensors(self):
        '''moves the rest of the way to the crate until the sensors have a reading'''
        self.tote_forklift.set_pos_stack1()
        if not self.align.is_in_range():
            self.strafe_left()
   
    
    @timed_state(duration=1, next_state = 'lift_tote_two')
    def go_until_limit_two(self):
        '''move forward until the robot hits the tote'''
        if not self.align.aligned:
            self.align.align()
        if self.align.is_against_tote(): 
            self.next_state('lift_tote_two')
    
    
   
    @timed_state(duration=1, next_state='strafe_n_two')
    def lift_tote_two(self):
        '''lifts the tote over the can'''
        self.tote_forklift.set_pos_stack3()
        self.next_state('strafe_n_two')
   
    
    @timed_state(duration=2, next_state='drive_forward')
    def strafe_n_two(self):
        '''strafes for n seconds'''
        self.drive.move(0,-1,0)
    
   
    @timed_state(duration=2, next_state='drive_forward')
    def go_until_sensors_two(self):
        '''strafes until infrared sensors have a reading'''
        if not self.align.is_in_range():
            self.strafe_left()
        else:
            self.next_state('drive_forward')
  
    
    @timed_state(duration=3, next_state='drop')
    def drive_forward(self):
        '''pushes 3rd tote into the auto zone'''
        #if not self.align.aligned:
           #self.align.align()
        #else:
        self.drive.move(-1, 0, 0)
    
    
    @timed_state(duration=3, next_state = 'reverse')
    def drop(self, initial_call):
        '''lowers the totes onto a stack'''
        if initial_call:
            self.tote_forklift.set_pos_bottom()
    
    
    @timed_state(duration = .3)
    def reverse(self):
        '''backs up so we aren't touching'''
        self.drive.move(1,0,0)