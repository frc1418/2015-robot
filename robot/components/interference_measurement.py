
from common.sensor import Sensor
from components.forklift import ToteForklift

class Calibrator:
    
    forklift = ToteForklift
    sensors = Sensor
    
    def __init__(self, forklift, sensors):
        self.forklift = forklift
        self.sensors = sensors
        
        self.positions = []
        
        self.first_on = None
        self.last_on = None
        
        
        self.done = False
    
    def reset(self):
        self.done = False
    
    def calibrate(self):
        
        if self.done:
            return
        
        if not self.forklift.isCalibrated:
            self.forklift.set_auto_position(0)
            return
        
        enc_pos = self.sensors.tote_enc
        
        if enc_pos > 11600:
            self.done = True
            
            with open('/home/lvuser/foo', 'w') as fp:
                fp.write(str(sorted(self.positions)))
            
            #print("Done with calibration", file=sys.stderr)
            #print(self.positions, file=sys.stderr)
        
        
        self.forklift.set_manual(0.3)
        
        if self.sensors.leftDistance < 120 or self.sensors.rightDistance < 120:
            #self.positions.add(enc_pos)
            
            if self.first_on is None:
                self.first_on = enc_pos
            self.last_on = enc_pos
            
        else:
            
            if self.first_on is not None:
                self.positions.append((self.first_on, self.last_on))
        
            self.first_on = None
            self.last_on = None

