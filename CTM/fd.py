class Fd:
    def __init__(self, freeflow_speed=100, jam_density=200, max_flow=200, lanes):
        #init
        self.freeflow_speed = freeflow_speed
        self.jam_density = jam_density
        self.max_flow = max_flow
        self.lanes = lanes

        #calculations
        self.jam_density_total = self.lane * self.jam_density
        self.maximum_fow_total = self.lane * self.max_flow
        self.critical_density = self.maximum_flow_total / self.free_flow_speed
        self.wavespeed = self.maximum_flow_total / (self.jam_density_total - self.critical_density)