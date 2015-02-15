import wpilib

from networktables import NetworkTable

class Drive(object):
	'''
		The sole interaction between the robot and its driving system
		occurs here. Anything that wants to drive the robot must go
		through this class.
	'''

	def __init__(self, robotDrive, gyro, backInfrared):
		'''
			Constructor. 
			
			:param robotDrive: a `wpilib.RobotDrive` object
		'''
		self.isTheRobotBackwards = False
		# set defaults here
		self.x = 0
		self.y = 0
		self.rotation = 0
		self.gyro = gyro
		
		self.angle_constant = .040
		self.gyro_enabled = True
		
		self.robotDrive = robotDrive
		
		# Strafe stuff
		self.backInfrared = backInfrared
		
		sd = NetworkTable.getTable('SmartDashboard')
		self.strafe_back_speed = sd.getAutoUpdateValue('strafe_back', .15)
		self.strafe_fwd_speed = sd.getAutoUpdateValue('strafe_fwd', -.2)
		

	#
	# Verb functions -- these functions do NOT talk to motors directly. This
	# allows multiple callers in the loop to call our functions without 
	# conflicts.
	#
	
	def move(self, y, x, rotation):
		'''
			Causes the robot to move
		
			:param x: The speed that the robot should drive in the X direction. 1 is right [-1.0..1.0] 
			:param y: The speed that the robot should drive in the Y direction. -1 is forward. [-1.0..1.0] 
			:param rotation:  The rate of rotation for the robot that is completely independent of the translation. 1 is rotate to the right [-1.0..1.0]
		'''
		
		self.x = x
		self.y = y
		self.rotation = max(min(1.0, rotation), -1) / 2.0
		
		

	
	def set_gyro_enabled(self, value):
		self.gyro_enabled = value
	
	def return_gyro_angle(self):
		return self.gyro.getAngle()
	
	def reset_gyro_angle(self):
		self.gyro.reset()

	
	def set_angle_constant(self, constant):
		'''Sets the constant that is used to determine the robot turning speed'''
		self.angle_constant = constant
	
	def angle_rotation(self, target_angle):
		'''
			Adjusts the robot so that it points at a particular angle. Returns True 
		    if the robot is near the target angle, False otherwise
		   
		    :param target_angle: Angle to point at, in degrees
		    
		    :returns: True if near angle, False otherwise
		'''
		
		if not self.gyro_enabled:
			return False
		
		angleOffset = target_angle - self.return_gyro_angle()
		
		if angleOffset < -1 or angleOffset > 1:
			self.rotation = angleOffset * self.angle_constant
			self.rotation = max(min(0.5, self.rotation), -0.5)
			
			return False
		
		return True
		
	
	def set_direction(self, direction):
		self.isTheRobotBackwards = bool(direction)
	
	def switch_direction(self):
		self.isTheRobotBackwards = not self.isTheRobotBackwards
	
	def wall_strafe(self, speed):
		
		y = (self.backInfrared.getDistance() - 15.0)/50.0
		y = max(min(self.strafe_back_speed.value, y), self.strafe_fwd_speed.value)
		
		self.y = y
		self.x = speed
		
		self.angle_rotation(0)
	
	#
	# Actually tells the motors to do something
	#
	
	def doit(self):
		''' actually does stuff'''
		if(self.isTheRobotBackwards):
			self.robotDrive.mecanumDrive_Cartesian(-self.x, -self.y, self.rotation , 0)
		else:
			self.robotDrive.mecanumDrive_Cartesian(self.x, self.y, self.rotation, 0)

		# print('x=%s, y=%s, r=%s ' % (self.x, self.y, self.rotation))
		
		
		# by default, the robot shouldn't move
		self.x = 0
		self.y = 0
		self.rotation = 0
	
