
import wpilib
from networktables.networktable import NetworkTable
import logging
logger = logging.getLogger("forklift")
import enum

class ForkliftMode(enum.Enum):
    MANUAL = 1
    AUTO = 2

class Forklift (object):
    
    def __init__ (self, limit_port, init_down_speed):
        self.testFirst = True
        self.target_position = None
        self.target_index = None
        
        self.init_down_speed = init_down_speed
        
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
        
        self.sd = NetworkTable.getTable('SmartDashboard')
        
    
    def get_target_position(self):
        return self.target_position
    
    def set_manual(self, value):
        '''
            :param value: Motor value between -1 and 1
        '''
        self.want_manual = True
        self.manual_value = value
    
    
    def _detect_position_index(self, offset, pos_idx):
        '''Returns the current position index'''
        
        if self.mode == ForkliftMode.AUTO:
            return self.target_index
        
        if not self.isCalibrated:
            return None
        
        # If we're not in auto mode, we need to try and detect where the
        # forklift is... 
        
        current_pos = self.get_position()
        
        for i, pos in enumerate(self.positions):
            pos_value = pos.value
            if current_pos < pos_value + offset:
                return i + pos_idx
            
        return (len(self.positions) - 1) + pos_idx
    
    def raise_forklift(self):
        '''Raises the forklift by one position'''   
        target_index = self._detect_position_index(-170, -1)
        
        if target_index == -1:
            target_index = 0
        
        if target_index is None:
            index = 1
        else:
            index = target_index + 1
            
        if index >= len(self.positions):
            index = len(self.positions)-1
        
        self._set_position(index)
    
    def lower_forklift(self):
        '''Lowers the forklift by one position'''
        
        target_index = self._detect_position_index(170, 0)
        
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
    
    def set_auto_position(self, target):
        self.want_auto = True
        self.target_index = 0
        self.target_position = target 
        
    def on_target(self):
        if abs(self.get_position()-self.target_position)<170:
            return True
        return False
    
    def _calibrate(self):
        '''Moves the motor towards the limit switch if needed'''
        if not self.isCalibrated:
            if self.get_limit_switch():
                self.motor.set(self.init_down_speed)
            else:
                self.motor.set(0)
                self.motor.setSensorPosition(0)
            
                self.motor.changeControlMode(wpilib.CANTalon.ControlMode.Position)
                self.isCalibrated = True
                
                self.on_calibrate()
    
    def on_calibrate(self):
        pass
    
    def doit(self):
        if self.want_manual:
            self.mode = ForkliftMode.MANUAL
        elif self.want_auto:
            self.mode = ForkliftMode.AUTO
            
        if self.last_mode != self.mode:
            if self.mode == ForkliftMode.MANUAL:
                self.motor.changeControlMode(wpilib.CANTalon.ControlMode.PercentVbus)
            elif self.mode == ForkliftMode.AUTO:
                self.new_pid = [e.value for e in self.wanted_pid]
                if self.isCalibrated:
                    # Only switch the control mode if we're not calibrating!
                    self.motor.changeControlMode(wpilib.CANTalon.ControlMode.Position)
            else:
                raise ValueError("INVALID MODE")
                
            
            self.last_mode = self.mode
        
        if self.mode == ForkliftMode.MANUAL:
            self.motor.set(self.manual_value)
            self.target_index = -1
        
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
            
        self.want_auto = False
        self.want_manual = False
        self.manual_value = 0
        
    def update_sd(self, name):
        
        self.sd.putNumber('%s|Encoder' % name, self.motor.getEncPosition())
        self.sd.putBoolean('%s|Calibrated' % name, self.isCalibrated)
        self.sd.putBoolean('%s|Manual' % name, self.mode == ForkliftMode.MANUAL)
        self.sd.putBoolean('%s|Limit' % name, self.get_limit_switch())
        if self.target_position is None:
            self.sd.putNumber('%s|Target Position' % name, -1)
        else:
            self.sd.putNumber('%s|Target Position' % name, self.target_index)
        

class ToteForklift(Forklift):
    def __init__ (self, motor, sensor, limit_port):
        super().__init__(limit_port, -1)
        
        self.sensor = sensor
        
        self.motor = motor
        
        sd = NetworkTable.getTable('SmartDashboard')
        
        self.positions = [
            sd.getAutoUpdateValue('Tote Forklift|bottom', 400),
            sd.getAutoUpdateValue('Tote Forklift|stack1', 4300),
            sd.getAutoUpdateValue('Tote Forklift|stack2', 7638),
            sd.getAutoUpdateValue('Tote Forklift|stack3', 9250),
            sd.getAutoUpdateValue('Tote Forklift|stack4', 10200),
            sd.getAutoUpdateValue('Tote Forklift|stack5', 11600),
            sd.getAutoUpdateValue('Tote Forklift|stack6', 11600),
          ]
        
        self.wanted_pid = (
            sd.getAutoUpdateValue('Tote Forklift|P', 10),
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
    
    def get_limit_switch(self):
        return self.limit.get()
    
    def get_position(self):
        return self.sensor.tote_enc

class CanForklift(Forklift):
    def __init__ (self, motor, sensor ,limit_port):
        super().__init__(limit_port, -1)
        
        self.sensor = sensor
        
        self.motor = motor
        
        sd = NetworkTable.getTable('SmartDashboard')
        self.positions = [
            sd.getAutoUpdateValue('Can Forklift|bottom', 0),
            sd.getAutoUpdateValue('Can Forklift|stack1', 1513),
            sd.getAutoUpdateValue('Can Forklift|stack2', 3559),
            sd.getAutoUpdateValue('Can Forklift|stack3', 5855),
            sd.getAutoUpdateValue('Can Forklift|stack4', 7715),
            sd.getAutoUpdateValue('Can Forklift|top', 10100),
        ]
        
        self.up_pid = (
            sd.getAutoUpdateValue('Can Forklift|Up P', 10),
            sd.getAutoUpdateValue('Can Forklift|Up I', 0),
            sd.getAutoUpdateValue('Can Forklift|Up D', 0)
        )
        
        self.down_pid = (
            sd.getAutoUpdateValue('Can Forklift|Down P', 10),
            sd.getAutoUpdateValue('Can Forklift|Down I', 0),
            sd.getAutoUpdateValue('Can Forklift|Down D', 0)
        )
        
        self.wanted_pid = self.up_pid
        
        self.motor.enableForwardSoftLimit(False)
        
        
    def _set_position(self, index):
        Forklift._set_position(self, index)
        
        target_position = self.get_target_position() 
        if target_position is None or target_position > self.get_position():
            self.wanted_pid = self.up_pid
        else:
            self.wanted_pid = self.down_pid
            
        self.new_pid = [e.value for e in self.wanted_pid]
    
    def on_calibrate(self):
        self.motor.setForwardSoftLimit(19000)
        self.motor.enableForwardSoftLimit(True)
        
    def set_pos_holding(self):
        self._set_position(5)
        
    set_pos_top = set_pos_holding
        
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
        
    def set_pos_7000(self):
        self.set_auto_position(7000)
    
    def get_limit_switch(self):
        return not self.motor.isRevLimitSwitchClosed()
    
    def get_position(self):
        return self.sensor.can_enc
    