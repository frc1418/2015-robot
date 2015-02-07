import wpilib

class Forklift (object):
    def __init__ (self, motor_port, limit_port, init_down_speed):

        self.target_position = None
        self.target_index = None
        
        self.init_down_speed = init_down_speed
        
        self.motor = wpilib.CANTalon(motor_port)
        self.limit = wpilib.DigitalInput(limit_port)
        
        self.isCalibrated = False
        
        self.current_manual_mode = True
        self.manual_mode = True
        self.manual_value = 0
        
        self.pid = None
        
        
    def get_position(self):
        return self.motor.getEncPosition()
    
    def get_target_position(self):
        return self.target_position
    
    def set_manual(self, value):
        '''
            :param value: Motor value between -1 and 1
        '''
        self.manual_mode = True
        self.manual_value = value
    
    
    def _detect_position_index(self):
        '''Returns the current position index'''
        
        if not self.manual_mode:
            return self.target_index
        
        current_pos = self.get_position()
        last_pos = None
        
        for i, pos in enumerate(self.positions):
            if current_pos < pos:
                if i == 0:
                    return 0
                
                # Pick the position that is closer
                if pos - current_pos > current_pos - last_pos:
                    return i
                else:
                    return i - 1
                
            last_pos = pos
            
        return len(self.positions) - 1
    
    def raise_forklift(self):
        '''Raises the forklift by one position'''
        
        target_index = self._detect_position_index()
        
        if target_index is None:
            index = 1
        else:
            index = target_index + 1
            
        if index >= len(self.positions):
            index = len(self.positions)
        
        self._set_position(index)
    
    def lower_forklift(self):
        '''Lowers the forklift by one position'''
        
        target_index = self._detect_position_index()
        
        if target_index is None:
            index = 0
        else:
            index = target_index - 1
            
        if index < 0:
            index = 0
        
        self._set_position(index)
    
    def set_pid(self, pid):
        if self.pid != pid:
            self.pid = pid
            self.motor.setPID(*pid)
    
    def _set_position(self, index):
        self.manual_mode = False
        self.target_index = index
        self.target_position = self.positions[index]
        
    def _calibrate(self):
        '''Moves the motor towards the limit switch if needed'''
        
        if not self.isCalibrated:
            if not self.limit.get():
                self.motor.set(self.init_down_speed)
            else:
                self.motor.set(0)
                self.motor.setSensorPosition(0)
            
                self.motor.changeControlMode(wpilib.CANTalon.ControlMode.Position)
                self.isCalibrated = True
    
    def doit(self):
        
        if self.current_manual_mode != self.manual_mode:
            if self.manual_mode:
                self.motor.changeControlMode(wpilib.CANTalon.ControlMode.PercentVbus)
            elif self.isCalibrated:
                # Only switch the control mode if we're not calibrating!
                self.motor.changeControlMode(wpilib.CANTalon.ControlMode.Position)
                
            self.current_manual_mode = self.manual_mode
        
        if self.manual_mode:
            self.motor.set(self.manual_value)
        
        elif self.target_position is not None:
            
            self._calibrate()
            
            if self.isCalibrated:
                self.motor.set(self.target_position)
                
        else:
            self.motor.set(0)
                
        self.manual_value = 0

class ToteForklift(Forklift):
    def __init__ (self, motor_port, limit_port):
        super().__init__(motor_port, limit_port, -1)
        
        self.positions = [
            0,  # bottom
            1, # stack1
            2, # stack2
            3, # stack3
            4, # stack4
            5, # stack5
        ]
        
        self.set_pid((1, 0, 0))
        
    def set_pos_stack5(self):
        self._set_position(5)
        
    set_pos_top = set_pos_stack5
     
    def set_pos_stack4(self):
        self._set_position(4)
        
    def set_pos_stack3(self):
        self._set_position(3)
        
    def set_pos_stack2(self):
        self._set_position(2)
        
    def set_pos_stack1(self):
        self._set_position(1)
        
    def set_pos_bottom(self):
        self._set_position(0)
        
class CanForklift(Forklift):
    def __init__ (self, motor_port, limit_port):
        super().__init__(motor_port, limit_port, -1)
        
        self.positions = [
            0, # bottom
            1, # stack1
            2, # stack2
            3, # stack3
            4, # stack4
            5, # stack5
        ]
        
        self.down_pid = (1, 0, 0)
        self.up_pid = (1, 0, 0)
        
        #self.motor.setPID
        
    def _update_pid(self):
        if self.get_target_position() > self.get_position():
            self.set_pid(self.down_pid)
        else:
            self.set_pid(self.up_pid)
    
    
      
    def set_pos_holding(self):
        self._set_position(0)
        self._update_pid()
        
    set_pos_top = set_pos_holding
        
    def set_pos_stack4(self):
        self._set_position(4)
        self._update_pid()
        
    def set_pos_stack3(self):
        self._set_position(3)
        self._update_pid()
        
    def set_pos_stack2(self):
        self._set_position(2)
        self._update_pid()
        
    def set_pos_stack1(self):
        self._set_position(1)
        self._update_pid()
        
    def set_pos_bottom(self):
        self._set_position(0)
        self._update_pid()
    