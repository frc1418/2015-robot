
import wpilib
from networktables.networktable import NetworkTable

import enum

class ForkliftMode(enum.Enum):
    MANUAL = 1
    AUTO = 2

class Forklift (object):
    
    
    
    def __init__ (self, motor_port, limit_port, init_down_speed):

        self.target_position = None
        self.target_index = None
        
        self.init_down_speed = init_down_speed
        
        self.motor = wpilib.CANTalon(motor_port)
        self.limit = wpilib.DigitalInput(limit_port)
        
        self.isCalibrated = False
        
        self.want_manual = False
        self.manual_value = 0
        
        self.want_auto = False
        
        self.mode = ForkliftMode.MANUAL
        self.last_mode = ForkliftMode.MANUAL
        
        # These need to be set by subclasses
        self.wanted_pid = None
        self.current_pid = (0, 0, 0)
        self.new_pid = None
        
        
    def get_position(self):
        return self.motor.getEncPosition()
    
    def get_target_position(self):
        return self.target_position
    
    def set_manual(self, value):
        '''
            :param value: Motor value between -1 and 1
        '''
        self.want_manual = True
        self.manual_value = value
    
    
    def _detect_position_index(self):
        '''Returns the current position index'''
        
        if self.mode == ForkliftMode.AUTO:
            return self.target_index
        
        # If we're not in auto mode, we need to try and detect where the
        # forklift is... 
        
        current_pos = self.get_position()
        last_pos = None
        
        for i, pos in enumerate(self.positions):
            pos_value = pos.value
            if current_pos < pos_value:
                if i == 0:
                    return 0
                
                # Pick the position that is closer
                if pos_value - current_pos > current_pos - last_pos:
                    return i
                else:
                    return i - 1
                
            last_pos = pos_value
            
        return len(self.positions) - 1
    
    def raise_forklift(self):
        '''Raises the forklift by one position'''
        
        target_index = self._detect_position_index()
        
        if target_index is None:
            index = 1
        else:
            index = target_index + 1
            
        if index >= len(self.positions):
            index = len(self.positions)-1
        
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
    
    def _set_position(self, index):
        self.want_auto = True
        self.target_index = index
        self.target_position = self.positions[index].value
        
    def _calibrate(self):
        '''Moves the motor towards the limit switch if needed'''
        print("Calibrating")
        if not self.isCalibrated:
            if self.limit.get():
                self.motor.set(self.init_down_speed)
            else:
                self.motor.set(0)
                self.motor.setSensorPosition(0)
            
                self.motor.changeControlMode(wpilib.CANTalon.ControlMode.Position)
                self.isCalibrated = True
    
    def doit(self):
        
        if self.want_manual:
            self.mode = ForkliftMode.MANUAL
        elif self.want_auto:
            self.mode = ForkliftMode.AUTO
        
        if self.last_mode != self.mode:
            if self.mode == ForkliftMode.MANUAL:
                self.motor.changeControlMode(wpilib.CANTalon.ControlMode.PercentVbus)
            elif self.isCalibrated:
                # Only switch the control mode if we're not calibrating!
                self.motor.changeControlMode(wpilib.CANTalon.ControlMode.Position)
                self.new_pid = [e.value for e in self.wanted_pid]
            
            self.last_mode = self.mode
        
        if self.mode == ForkliftMode.MANUAL:
            self.motor.set(self.manual_value)
        
        elif self.mode == ForkliftMode.AUTO:
            
            self._calibrate()
            
            if self.isCalibrated:
                
                # Update the PID values if necessary
                if self.current_pid != self.new_pid:
                    self.motor.setPID(*self.new_pid)
                    self.current_pid = self.new_pid
                
                self.motor.set(self.target_position)
                
        else:
            self.motor.set(0)
               
        self.manual_value = 0

class ToteForklift(Forklift):
    def __init__ (self, motor_port, limit_port):
        super().__init__(motor_port, limit_port, -1)
        
        sd = NetworkTable.getTable('SmartDashboard')
        
        self.positions = [
            sd.getAutoUpdateValue('Tote Forklift|bottom', 0),
            sd.getAutoUpdateValue('Tote Forklift|stack1', 1),
            sd.getAutoUpdateValue('Tote Forklift|stack2', 2),
            sd.getAutoUpdateValue('Tote Forklift|stack3', 3),
            sd.getAutoUpdateValue('Tote Forklift|stack4', 4),
            sd.getAutoUpdateValue('Tote Forklift|stack5', 5),
          ]
        
        self.wanted_pid = (
            sd.getAutoUpdateValue('Tote Forklift|P', 1),
            sd.getAutoUpdateValue('Tote Forklift|I', 0), 
            sd.getAutoUpdateValue('Tote Forklift|D', 0)
        )
            
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
      
        sd = NetworkTable.getTable('SmartDashboard')
        
        self.positions = [
            sd.getAutoUpdateValue('Can Forklift|bottom', 0),
            sd.getAutoUpdateValue('Can Forklift|stack1', 1),
            sd.getAutoUpdateValue('Can Forklift|stack2', 2),
            sd.getAutoUpdateValue('Can Forklift|stack3', 3),
            sd.getAutoUpdateValue('Can Forklift|stack4', 4),
            sd.getAutoUpdateValue('Can Forklift|stack5', 5),
        ]
        
        self.up_pid = (
            sd.getAutoUpdateValue('Can Forklift|Up P', 1),
            sd.getAutoUpdateValue('Can Forklift|Up I', 0),
            sd.getAutoUpdateValue('Can Forklift|Up D', 0)
        )
        
        self.down_pid = (
            sd.getAutoUpdateValue('Can Forklift|Down P', 1),
            sd.getAutoUpdateValue('Can Forklift|Down I', 0),
            sd.getAutoUpdateValue('Can Forklift|Down D', 0)
        )
        
        
    def _update_pid(self):
        target_position = self.get_target_position() 
        if target_position is None or target_position > self.get_position():
            self.wanted_pid = self.up_pid
        else:
            self.wanted_pid = self.down_pid
            
        self.new_pid = [e.value for e in self.wanted_pid]
        
    
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
    