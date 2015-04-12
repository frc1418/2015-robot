
FRC Team 1418 Robot Code
========================

This code is released from Team 1418's 2015 robot. Team 1418 had one of their
best years yet in 2015. 

They had a great performance at George Mason University at the Greater DC Regional,
finishing as the #2 seed, and led the #2 alliance to the semifinals with teams
1885 and 686. They were awarded the Innovation in Control award for a variety
of reasons, including their simple but effective sensor package, multiple
autonomous modes and useful touchscreen driver station interface.

Highlights of the code
----------------------

* Full pyfrc integration for testing & robot simulation
* Unit tests over the robot code with 70% code coverage
* Complex autonomous mode support
	* Multiple working autonomous modes used in competition
		* Three Tote Strafe - Picks up three totes and makes a Tote Stack worth 20 points
		* Can Pickup - Picks up a single can and puts it in the auto zone
		* Tote Pickup - Picks up a single tote and puts it in the auto zone
		* Tote Pickup II - Pick up two totes from the landfill, and move back into the auto zone
		* Drive Forward - Drives the robot into the auto zone
	* Automatic support for tuning the autonomous mode parameters
	  via the UI
* Two forklifts, one for cans and one for totes
	* Encoder-based PID control allows operator to pick up and deposit totes/cans quickly and accurately
	* Fully controllable via NetworkTables
* Mecanum drive

The autonomous mode stuff will be rolled into pyfrc in the near future, so
that it can be used by more teams. 


Deploying onto the robot
------------------------

The robot code is written in Python, and so to run it you must install 
RobotPy onto the robot. Refer to the instructions accompanying RobotPy
for more information. 

With the pyfrc library installed, you can deploy the code onto the robot
by running robot.py with the following arguments:

	$ python robot.py deploy
	
This will run the unit tests and upload the code to the robot of your
choice.

Testing/Simulation
------------------

The robot code has full integration with pyfrc. You can use the various
simulation/testing options of the code by running robot.py directly. With
pynetworktables installed, you can use netsim mode of pyfrc to test the
robot code and the driver station UI together. 


Code Structure
==============

.
	You are here.

robot/
	robot/
		The robot code lives here
		tests/
			py.test-based unit tests that test the code and can be run via pyfrc

	electrical_test/
			Barebones code ran to make sure all of the electronics are working
		tests/
			Basic testing code to make sure we don't have syntax errors
	Crio_tests/
		Code for testing sensors on the Crio
	practice_robot/
		Barebones code for testing drive trains on the practice robot.



2015 Team 1418 Programming Team
===============================

Mentors:

	Dustin Spicuzza, lead software mentor
	dustin@virtualroadside.com
	
Students:

	Tim Winters, robot code
	Matt Puentes, robot code

	Leon Tan, Driver Station code
	Tyler Gogol, Driver Station code
	
	Ben Rice, Image Processing programmer
	Carter Fendly, Oculus Rift programmer / Image Processing programmer
