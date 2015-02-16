from robotpy_ext.autonomous import timed_state, StatefulAutonomous
from common.custom_stateful import SensorStatefulAutonomous

# Only for auto complete #
from components.drive import Drive
from components.forklift import ToteForklift

import logging

class TwoToteStrafe(SensorStatefulAutonomous):
    MODE_NAME = 'Test For Matt'
    DEFAULT = True 
    
    drive = Drive
    tote_forklift = ToteForklift
    
    def initialize(self):
        self.logger = logging.getLogger('two-tote')
        self.register_sd_var('over', -.9)
        self.register_sd_var('move_fwd', -.3)
        self.register_sd_var('tote_adjust', .4)
        self.register_sd_var('final_fwd', -.5)
    
    def on_enable(self):
        super().on_enable()
        self.drive.reset_gyro_angle()
        
    def on_iteration(self, tm):
        super().on_iteration(tm)
    
    
    @timed_state(duration=10, first=True)
    def go_until_tote2(self, initial_call):
        '''moves the rest of the way to the crate until the sensors have a reading'''
        
        self.drive.wall_strafe(self.over)
        
        if self.sensors.is_in_range():
            self.logger.info("Go: in range")
            self.done()
