import wpilib

class Button:
    def __init__(self,joystick,buttonnum):
        self.joystick=joystick
        self.buttonnum=buttonnum
        self.latest = 0
        self.timer = wpilib.Timer()
        self.timer.start()
    def get(self):
        now = self.timer.get()
        if(self.joystick.getRawButton(self.buttonnum)):
            if (now-self.latest) > 0.025: 
                self.latest = now
                return True
        return False