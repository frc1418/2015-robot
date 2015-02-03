import wpilib

class Drive(object):
	'''
		The sole interaction between the robot and its driving system
		occurs here. Anything that wants to drive the robot must go
		through this class.
	'''

	def __init__(self, robotDrive , gyro):
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
		self.rotation = rotation
		
		

	
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
		
	def infrared_rotation(self, distance1, distance2):
		'''when facing the direction of the robot:
		distance 1 should be on the left
		distance 2 should be on the right
		'''
		rotation = 0
		strafe = 0
		#distance between sensors is assumed to be 12 inches
		distanceBetween = 12
		#now we find the slope
		slope = (distance2 - distance1)/((distanceBetween /  2) - (-distanceBetween /2))
		if abs(slope)>.2:
			#print("slope > 1/10")
			#gives it a "deadzone"
			if distance1>distance2:
				# then the robot is too far counterclockwise
				rotation = .1
				stafe = .1
			elif distance2 > distance1:
				#too far clockwise
				strafe = -.1
				rotation = -.1
		else:
			rotation = 0
			strafe = 0
		self.move(0, strafe, rotation / 2)
		
	#
	# Actually tells the motors to do something
	#
	def switch_direction(self, b):
		
		self.isTheRobotBackwards = not self.isTheRobotBackwards
		
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
	
