class Cell:
    def __init__(self, id, vehicles, length, flow, has_onramp, has_offramp, beta, lanes):
        self.id = id
        self.vehicles = vehicles
        self.length = length
        self.flow = flow
        self.has_onramp = has_onramp
        self.has_offramp = has_offramp
        self.beta = beta
        self.lanes = lanes
        
        self.inflow = 0
        self.outflow = 0
        
        # calcs
        self.density = self.vehicles / self.length
        if not self.density == 0:
            self.speed = self.flow / self.density
        else:
            self.speed = 0
        # fixed variables
        self.jam_density_per_lane = 180
        self.free_flow_speed = 100
        self.maximum_flow_per_lane = 2000
        
        self.jam_density = self.lane * self.jam_density_per_lane
        self.maximum_flow = self.lane * self.maximum_flow_per_lane
        
        self.critical_density = self.maximum_flow / self.free_flow_speed
        self.wavespeed = self.maximum_flow / (self.jam_density - self.critical_density)
        
    def inflow_updater(self, inflow):
        self.inflow = inflow
        
    def update(self, next_cell):
        
        self.outflow = min((1-self.beta)*self.speed*self.density, next_cell.wavespeed*(next_cell.critical_density-next_cell.density), self.maximum_flow)
        
        
