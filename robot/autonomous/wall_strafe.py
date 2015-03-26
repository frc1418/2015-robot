

from components.drive import Drive
from robotpy_ext.autonomous import timed_state, StatefulAutonomous

class WallStrafe(StatefulAutonomous):

    MODE_NAME = 'Test: Wall Strafe'

    DEFAULT = False 
    
    drive = Drive

    def initialize(self):
        self.register_sd_var('over', -.5)
    
    def on_enable(self):
        super().on_enable()
        self.drive.reset_gyro_angle()

    @timed_state(duration=10.0, first=True)
    def do_the_drive(self):
        
        self.drive.wall_strafe(self.over)
        
