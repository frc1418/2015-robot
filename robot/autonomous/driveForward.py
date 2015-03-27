
from robotpy_ext.autonomous import timed_state, StatefulAutonomous

class DriveForward(StatefulAutonomous):

    MODE_NAME = 'Drive Forward'

    DEFAULT = False 

    def initialize(self):
        pass

    @timed_state(duration=2, first=True)
    def drive_forward(self):
        self.drive.move(-.5, 0, 0)
