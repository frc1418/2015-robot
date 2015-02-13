
from robotpy_ext.autonomous import timed_state, StatefulAutonomous

class DriveForward(StatefulAutonomous):

    MODE_NAME = 'Drive Forward'

    DEFAULT = False 

    def initialize(self):
        pass

    @timed_state(duration=0.5, next_state='drive_forward', first=True)
    def drive_wait(self):
        pass

    @timed_state(duration=5)
    def drive_forward(self):
        self.drive.move(0, 1, 0)
