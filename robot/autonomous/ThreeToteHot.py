from robotpy_ext.autonomous import timed_state, StatefulAutonomous

class ThreeToteHot(StatefulAutonomous):
    MODE_NAME = 'Three Totes'
    
    DEFAULT = False
    
    def initialize(self):
        self.aligning = False
    def on_iteration(self, tm):
        if self.aligning:
            self.align.align()
    @timed_state(duration = 3, next_state = 'reverse1', first=True)
    def tote1(self):
        self.aligning = True
    @timed_state(duration = .7, next_state = 'strafe1')
    def reverse1(self):
        self.aligning = False
        self.drive.move(1,0,0)
    @timed_state(duration = 1, next_state = 'tote2')
    def strafe1(self):
        self.drive.move(0,-1,0)
    @timed_state(duration = 3, next_state = 'reverse2')
    def tote2(self):
        self.aligning = True
    @timed_state(duration = .7, next_state = 'strafe2')
    def reverse2(self):
        self.aligning = False
        self.drive.move(1,0,0)
    @timed_state(duration = 1, next_state = 'tote3')
    def strafe2(self):
        self.drive.move(0,-1,0)
    @timed_state(duration = 2.6)
    def tote3(self):
        self.drive.move(-1,0,0)
        self.tote_forklift.set_pos_stack2()
    
        
            
        
            
    
    