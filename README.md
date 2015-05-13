FRC1418 2015 Robot Code
=======================

* Code: **Robot** | [UI](https://github.com/frc1418/2015-ui) | [Image Processing](https://github.com/frc1418/2015-vision) | [Oculus Rift](https://github.com/frc1418/2015-oculus)
* Factsheet: [Google Doc](https://docs.google.com/document/d/1irbUm-Qfxz_Ua2XiB5KzYWG2Ec5Xhr038NqL-k4FveA)

Introduction
------------

This code was used to control Team 1418's robot in 2015.

They had a great performance at George Mason University at the Greater DC 
Regional, finishing as the #2 seed, and led the #2 alliance to the semifinals
with teams 1885 and 686. They were awarded the Innovation in Control award for
a variety of reasons, including their simple but effective sensor package,
multiple autonomous modes and useful touchscreen driver station interface.

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

Deploying onto the robot
------------------------

The robot code is written in Python, and so to run it you must install 
RobotPy onto the robot. Refer to the instructions accompanying RobotPy
for more information. 

With the pyfrc library installed, you can deploy the code onto the robot
by running robot.py with the following arguments:

	python3 robot.py deploy
	
This will run the unit tests and upload the code to the robot of your
choice.

Testing/Simulation
------------------

The robot code has full integration with pyfrc. Make sure you have pyfrc
installed, and then you can use the various simulation/testing options
of the code by running robot.py directly.

    python3 robot.py sim

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
		CrioTests/
			Code for testing sensors on the Crio
		practice_robot/
			Barebones code for testing drive trains on the practice robot.

Authors
=======

Students:

* Tim Winters
* Matt Puentes
* Katherine Reinke
* Rachel Baek

Dustin Spicuzza, mentor
