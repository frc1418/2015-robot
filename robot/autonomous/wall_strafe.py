

from components.drive import Drive
from robotpy_ext.autonomous import timed_state, StatefulAutonomous

class WallStrafe(StatefulAutonomous):

    MODE_NAME = 'Wall Strafe'

    DEFAULT = False 
    
    drive = Drive

    def initialize(self):
        self.register_sd_var('over', -.5)
        self.register_sd_var('backwards', .15)
        self.register_sd_var('fwd_min', -.2)
    
    def on_enable(self):
        super().on_enable()
        self.drive.reset_gyro_angle()

    @timed_state(duration=10.0, first=True)
    def do_the_drive(self):
        
        y = (self.align.backSensor.getDistance() - 15.0)/50.0
        
        y = max(min(self.backwards, y), self.fwd_min)
        
        self.drive.move(y, self.over, 0)
        
        self.drive.angle_rotation(0)
        
