from robotpy_ext.autonomous import timed_state, StatefulAutonomous
class ThreeToteHot(StatefulAutonomous):
    MODE_NAME = 'Three Totes'
    
    DEFAULT = False
        
    def initialize(self):
        self.aligning = False
        self.aligned = self.align.aligned
        self.angle = 0

        
        #self.register_sd_var('driveSpeed', .3)
        #self.register_sd_var('rotateLeftTime', 5)
        #self.register_sd_var('rotateRightTime', 5)
        #self.register_sd_var('driveForwardTime', 5)
    def on_enable(self):
        StatefulAutonomous.on_enable(self)
    def on_iteration(self, tm):
        super().on_iteration(tm)
        if tm<5:
            self.angle = self.angle - 180/199
        elif tm<10:
            self.angle = self.angle + 180/199
        
        
        
    @timed_state(duration=0, next_state = 'first_forward', first=True)
    def raise_lift(self):
        self.tote_forklift.raise_forklift()
        self.next_state('first_forward')
    @timed_state(duration=.25, next_state='drive_left')
    def first_forward(self):
        self.drive.move(-.35, 0,0)
    @timed_state(duration=5, next_state = 'drive_right')
    def drive_left(self):
        self.drive.move(-.35,0,0)
        self.drive.angle_rotation(self.angle)
        if not self.sensors.toteLimitLSensor and not self.sensors.toteLimitR:
            self.tote_forklift.set_pos_stack1()
    @timed_state(duration=5)
    def drive_right(self):
        self.drive.move(-.35,0,0)
        self.drive.angle_rotation(self.angle)
        if not self.sensors.toteLimitL and not self.sensors.toteLimitR:
            self.tote_forklift.set_pos_stack2()
    @timed_state(duration=5)
    def drive_forward(self):
        self.drive.move(-.35,0,0)
        self.drive.angle_rotation(0)
        
            
        
            
    
    