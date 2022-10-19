class Cell:
    def __init__(self, id, vehicles, length, flow, has_onramp, has_offramp, beta, lanes, fd):
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

        # objects
        self.fd = fd
        self.previous_cell = none
        self.next_cell = none
        
        # calcs
        self.density = self.vehicles / self.length
        if not self.density == 0:
            self.speed = self.flow / self.density
        else:
            self.speed = 0
        
    #update parameters    
    def update(self):
        #inflow
        if self.previous_cell:
            self.inflow = self.previous_cell.outflow
        
        #density
        if self.vehicles:
            self.density = self.vehicles / self.length
        
        #outflow
        self.outflow = min((1-self.beta)*self.speed*self.density, self.next_cell.wavespeed*(self.next_cell.critical_density-self.next_cell.density), self.maximum_flow)
        
        
