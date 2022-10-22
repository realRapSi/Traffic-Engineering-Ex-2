class Fd:
    def __init__(self, freeflow_speed=100, jam_density=180, max_flow=2000, lanes=1):
        #init
        self.freeflow_speed = freeflow_speed
        self.jam_density = jam_density
        self.max_flow = max_flow
        self.lanes = lanes

        #calculations
        self.jam_density_total = self.lanes * self.jam_density
        self.maximum_flow_total = self.lanes * self.max_flow
        self.critical_density = self.maximum_flow_total / self.freeflow_speed
        self.wavespeed = abs(self.maximum_flow_total / (self.critical_density - self.jam_density_total))

    
    def get_flow(self, density):
        flow = 0
        if density >= self.critical_density:
            flow = (density - self.critical_density) * self.wavespeed + self.maximum_flow_total
        elif density < self.critical_density:
            flow = density * self.freeflow_speed

        return flow
