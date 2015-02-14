
from components.forklift import ToteForklift

def test_detect_position(hal_data):
    
    forklift = ToteForklift(1, 1)
    forklift.set_manual(0)
    
    can = hal_data['CAN'][1]
    
    # Should return None when not calibrated
    assert forklift.isCalibrated == False
    assert forklift._detect_position_index(250) == None
    
    forklift.isCalibrated = True
    
    # set positions to known values
    for i, pos in enumerate(forklift.positions):
        pos.value = i*1000
    
    can['enc_position'] = 5
    assert forklift.get_position() == 5
    
    down_tests = [
        # encoder, expected position, offset
        (-2000, 0, 0),
        (-200, 0, 0),
        (200, 0, 0),
        (500, 1, 0),
        (800, 1, 0),
        (900, 1, 0),
        (1000, 1, 0),
        (1200, 1, 0),
        (1500, 2, 1),
        (1700, 2, 1),
        (2000, 2, 1),
        (2200, 2, 1),
        (2500, 3, 2)   
    ]
    
    for enc_value, expected_pos, expected_idx in down_tests:
        can['enc_position'] = enc_value
        assert forklift._detect_position_index(250) == expected_pos
        
        forklift.set_manual(0)
        forklift.lower_forklift()
    
        assert forklift.target_index == expected_idx
        
    up_tests = [
        # encoder, expected position + 1, target_inde
        (-2000, 0, 1),
        (-200, 1, 1),
        (200, 1, 1),
        (500, 1, 1),
        (800, 2, 2),
        (900, 2, 2),
        (1000, 2, 2),
        (1200, 2, 2),
        (1500, 2, 2),
        (1700, 2, 2),
        (1900, 3, 3),
        (2000, 3, 3),
        (2200, 3, 3),
        (2500, 3, 3)   
    ]
    
    for enc_value, expected_pos, expected_idx in up_tests:
        print(enc_value)
        can['enc_position'] = enc_value
        assert forklift._detect_position_index(-250) == expected_pos
    
        forklift.set_manual(0)
        forklift.raise_forklift()
    
        assert forklift.target_index == expected_idx
    