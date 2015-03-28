from robotpy_ext.autonomous import timed_state, StatefulAutonomous
from common.custom_stateful import SensorStatefulAutonomous

# Only for auto complete #
from components.drive import Drive
from components.forklift import ToteForklift

import logging

class ThreeToteStrafe(SensorStatefulAutonomous):
    MODE_NAME = 'Three Tote Strafe'
    DEFAULT = True
    
    drive = Drive
    tote_forklift = ToteForklift
    
    def initialize(self):
        self.logger = logging.getLogger('three-strafe')
        self.register_sd_var('over', -1)
        self.register_sd_var('move_fwd', -.3)
        self.register_sd_var('final_fwd', -.5)
    
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
    
    @timed_state(duration=.5, next_state='get_tote1', first=True)
    def calibrate(self, initial_call):
        
        if initial_call:
            self.tote_forklift.set_pos_bottom()
            
        if self.tote_forklift.isCalibrated:
            self.logger.info("Calibrated")
            self.next_state('get_tote1')
    
    @timed_state(duration=1, next_state='back_to_wall1')
    def get_tote1(self, initial_call, state_tm):
        '''This method will drive at .1 until the robot hits the tote'''
        
        self.drive.move(self.move_fwd, 0, 0)
        
        if self.sensors.is_against_tote() or state_tm > 0.65:
            self.tote_forklift.set_pos_stack1()
            
            #self.logger.info("Against tote")
            #self.next_state('lift_tote1')
    
    @timed_state(duration=1.5, next_state='strafe_can1')
    def back_to_wall1(self, initial_call):
        
        if initial_call:
            self.tote_forklift.set_pos_stack1()
    
        y = self.drive.wall_goto()
        if y <= 0.1:
            self.next_state('strafe_can1')
            self.logger.info("Back to wall")
        
        
        #if self.tote_forklift.on_target():
        #    self.logger.info("Wait: on target again")
        #    self.next_state('strafe_can1')
    
    
    @timed_state(duration=1.8, next_state = 'go_until_tote2')
    def strafe_can1(self):
        '''strafes over for n seconds'''
        self.drive.wall_strafe(self.over)
    
    @timed_state(duration=.75, next_state='get_tote2')
    def go_until_tote2(self, initial_call):
        '''moves the rest of the way to the crate until the sensors have a reading'''
        
        self.drive.wall_strafe(self.over)
        
        if self.sensors.is_in_range():
            self.logger.info("Go: in range")
            self.next_state('get_tote2')
            
    @timed_state(duration=1, next_state='back_to_wall2')
    def get_tote2(self, initial_call, state_tm):
        '''This method will drive at .1 until the robot hits the tote'''
        
        self.drive.move(self.move_fwd, 0, 0)
        
        if self.sensors.is_against_tote() or state_tm > 0.65:
            self.tote_forklift.set_pos_stack3()
            
            #self.logger.info("Against tote")
            #self.next_state('lift_tote1')
    
    @timed_state(duration=1.5, next_state='strafe_can2')
    def back_to_wall2(self, initial_call):
        
        if initial_call:
            self.tote_forklift.set_pos_stack3()
            self.pin_servo.set(1)
    
        y = self.drive.wall_goto()
        if y <= 0.1:
            self.next_state('strafe_can2')
            self.logger.info("Back to wall2")
        
        
        #if self.tote_forklift.on_target():
        #    self.logger.info("Wait: on target again")
        #    self.next_state('strafe_can1')
    
    
    @timed_state(duration=2, next_state = 'go_until_tote3')
    def strafe_can2(self):
        '''strafes over for n seconds'''
        self.drive.wall_strafe(self.over)
    
    @timed_state(duration=.75, next_state='drive_forward')
    def go_until_tote3(self, initial_call):
        '''moves the rest of the way to the crate until the sensors have a reading'''
        
        self.drive.wall_strafe(self.over)
        
        if self.sensors.is_in_range():
            self.logger.info("Go: in range")
            self.next_state('drive_forward')
    
    #
    # Final stretch
    #
    
    #@timed_state(duration=.25, next_state='drive_forward')
    #def go_more(self):
    #    self.drive.wall_strafe(self.over)
        
  
    
    @timed_state(duration=2, next_state='drop')
    def drive_forward(self, initial_call):
        '''pushes 3rd tote into the auto zone'''
        if initial_call:
            self.tote_forklift.set_pos_stack2()
        self.drive.move(self.final_fwd, 0, 0)
    
    
    @timed_state(duration=2, next_state = 'reverse')
    def drop(self, initial_call):
        '''lowers the totes onto a stack'''
        if initial_call:
            self.tote_forklift.set_pos_stack1()
        
        if self.tote_forklift.on_target():
            self.next_state('reverse')
    
    
    @timed_state(duration=.5)
    def reverse(self):
        '''backs up so we aren't touching'''
        self.drive.move(.2, 0, 0)
