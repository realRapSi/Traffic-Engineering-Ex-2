import numpy as np
class Fd:
    def __init__(self, freeflow_speed=100, jam_density=180, maximum_flow=2000, lanes=1):
        #init
        self.freeflow_speed = freeflow_speed
        self.jam_density = jam_density * lanes
        self.maximum_flow = maximum_flow * lanes
        self.lanes = lanes

        #calculations
        self.critical_density = self.maximum_flow / (self.freeflow_speed * np.exp(-1/2))
        self.wavespeed = self.maximum_flow / (self.jam_density - self.critical_density)
    
    def get_flow(self, density):
        temp_density = density * self.freeflow_speed * np.exp(-1/2 * (density / self.critical_density)**2)
        if temp_density > self.jam_density:
            return 0
        return temp_density

    def get_speed(self, density):
        return self.freeflow_speed * np.exp(-1/2 * (density / self.critical_density)**2)


