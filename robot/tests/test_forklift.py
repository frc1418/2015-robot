
import wpilib

from common.sensor import Sensor
from components.forklift import ToteForklift

def test_detect_position(hal_data):
    
    tote_motor = wpilib.CANTalon(1)
    can_motor = wpilib.CANTalon(2)
    
    sensors = Sensor(tote_motor, can_motor)
    
    forklift = ToteForklift(tote_motor, sensors, 5)
    forklift.set_manual(0)
    
    can = hal_data['CAN'][1]
    
    # Should return None when not calibrated
    assert forklift.isCalibrated == False
    assert forklift._detect_position_index(170, 0) == None
    
    forklift.isCalibrated = True

    keys = [
        'Tote Forklift|bottom',
        'Tote Forklift|stack1',
        'Tote Forklift|stack2',
        'Tote Forklift|stack3',
        'Tote Forklift|stack4',
        'Tote Forklift|stack5',
        'Tote Forklift|stack6',
    ]
    
    # set positions to known values
    for i, key in enumerate(keys):
        wpilib.SmartDashboard.putNumber(key, i*1000)
    
    can['enc_position'] = 5
    sensors.update()
    
    assert forklift.get_position() == 5
    
    down_tests = [
        # encoder, expected position, offset
        (-2000, 0, 0),
        (-200, 0, 0),
        (150, 0, 0),
        (500, 1, 0),
        (800, 1, 0),
        (900, 1, 0),
        (1000, 1, 0),
        (1150, 1, 0),
        (1500, 2, 1),
        (1700, 2, 1),
        (2000, 2, 1),
        (2150, 2, 1),
        (2500, 3, 2)   
    ]
    
    for enc_value, expected_pos, expected_idx in down_tests:
        print(enc_value)
        can['enc_position'] = enc_value
        sensors.update()
        
        assert forklift._detect_position_index(170, 0) == expected_pos
        
        forklift.set_manual(0)
        forklift.lower_forklift()
    
        assert forklift.target_index == expected_idx
        
    up_tests = [
        # encoder, expected position + 1, target_inde
        (-2000, -1, 1),
        (-150, 0, 1),
        (200, 0, 1),
        (500, 0, 1),
        (850, 1, 2),
        (900, 1, 2),
        (1000, 1, 2),
        (1200, 1, 2),
        (1500, 1, 2),
        (1700, 1, 2),
        (1900, 2, 3),
        (2000, 2, 3),
        (2200, 2, 3),
        (2500, 2, 3)   
    ]
    
    for enc_value, expected_pos, expected_idx in up_tests:
        print(enc_value)
        can['enc_position'] = enc_value
        sensors.update()
        
        assert forklift._detect_position_index(-170, -1) == expected_pos
    
        forklift.set_manual(0)
        forklift.raise_forklift()
    
        assert forklift.target_index == expected_idx
    