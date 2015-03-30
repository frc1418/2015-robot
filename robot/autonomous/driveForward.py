
from robotpy_ext.autonomous import timed_state, StatefulAutonomous

class DriveForward(StatefulAutonomous):

    MODE_NAME = 'Drive Forward'

    DEFAULT = False 

    def initialize(self):
        pass

    @timed_state(duration=4.2, first=True)
    def drive_forward(self):
        '''drives forward from alliance wall into auto zone'''
        self.drive.move(.25, 0, 0)
