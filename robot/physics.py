
from pyfrc.physics.drivetrains import mecanum_drivetrain

class PhysicsEngine:
    
    
    def __init__(self, controller):
        self.controller = controller
        
        # keep track of the tote encoder position
        
        # keep track of the can encoder position
    
    def initialize(self, hal_data):
        hal_data['dio'][0]['value'] = True
        hal_data['dio'][1]['value'] = True
        hal_data['dio'][2]['value'] = True
        hal_data['dio'][3]['value'] = True
        
        self.controller.add_gyro_channel(0)
    
    def update_sim(self, hal_data, now, tm_diff):
        
        # Simulate the tote forklift
        
        # Simulate the can forklift
        
        # Do something about the distance sensors?
        
        
        # Simulate the drivetrain
        lf_motor = hal_data['pwm'][0]['value']
        lr_motor = hal_data['pwm'][1]['value']
        rf_motor = -hal_data['pwm'][2]['value']
        rr_motor = -hal_data['pwm'][3]['value']
        
        vx, vy, vw = mecanum_drivetrain(lr_motor, rr_motor, lf_motor, rf_motor)
        self.controller.vector_drive(vx, vy, vw, tm_diff)
        