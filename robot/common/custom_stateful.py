
from robotpy_ext.autonomous import StatefulAutonomous

class SensorStatefulAutonomous(StatefulAutonomous):
    
    def on_iteration(self, tm):
        self.sensors.update()
        return StatefulAutonomous.on_iteration(self, tm)
