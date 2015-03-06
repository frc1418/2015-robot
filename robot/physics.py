import wpilib
from pyfrc.physics.drivetrains import mecanum_drivetrain
from components import forklift

class PhysicsEngine:
    
    
    def __init__(self, controller):
        self.controller = controller
        
        # keep track of the tote encoder position
        
        # keep track of the can encoder position
        self.toteAct = 1000
        self.tote = forklift.ToteForklift
        self.can = forklift.CanForklift
    def initialize(self, hal_data):
        hal_data['dio'][0]['value'] = True
        hal_data['dio'][1]['value'] = True
        hal_data['dio'][2]['value'] = True
        hal_data['dio'][3]['value'] = True
        
        self.controller.add_gyro_channel(0)
        
    def update_sim(self, hal_data, now, tm_diff):
        # Simulate the tote forklift
        try:

            toteDict = hal_data['CAN'][5]
            canDict = hal_data['CAN'][15]
        except:

            pass

        else:

            if toteDict['mode_select'] == wpilib.CANTalon.ControlMode.PercentVbus:
                self.toteAct += int(toteDict['value']*tm_diff*2333/1023)
                toteDict['enc_position'] += int(toteDict['value']*tm_diff*2333/1023)

            elif toteDict['mode_select'] == wpilib.CANTalon.ControlMode.Position:

                if toteDict['enc_position']<toteDict['value']:
                    self.toteAct += int(tm_diff*2333/1023)
                    toteDict['enc_position'] += int(tm_diff*2333)

                else:
                    self.toteAct = int(tm_diff*2333/1023)
                    toteDict['enc_position'] -= int(tm_diff*2333)

        
            if canDict['mode_select'] == wpilib.CANTalon.ControlMode.PercentVbus:

                canDict['enc_position'] += int(canDict['value']*tm_diff*2333/1023)

            elif canDict['mode_select'] == wpilib.CANTalon.ControlMode.Position:

                if canDict['enc_position']<canDict['value']:

                    canDict['enc_position'] += int(tm_diff*2333)

                else:

                    canDict['enc_position'] -= int(tm_diff*2333)
            
            if self.toteAct == 0:
                hal_data['dio'][2]['value'] = False
        # Simulate the can forklift
        
        # Do something about the distance sensors?
        
        
        # Simulate the drivetrain
        lf_motor = hal_data['pwm'][0]['value']
        lr_motor = hal_data['pwm'][1]['value']
        rf_motor = -hal_data['pwm'][2]['value']
        rr_motor = -hal_data['pwm'][3]['value']
        
        vx, vy, vw = mecanum_drivetrain(lr_motor, rr_motor, lf_motor, rf_motor)
        self.controller.vector_drive(vx, vy, vw, tm_diff)
        