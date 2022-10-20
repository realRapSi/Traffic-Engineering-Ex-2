class Cell:
    def __init__(self, id, vehicles, length, flow, has_onramp, has_offramp, beta, lanes, fd, time_seconds):
        self.id = id
        self.vehicles = vehicles
        self.length = length
        self.flow = flow
        self.has_onramp = has_onramp
        self.has_offramp = has_offramp
        self.beta = beta
        self.lanes = lanes
        self.time_seconds = time_seconds
        self.time_factor = self.time_seconds / 3600
        
        self.inflow = 0
        self.outflow = 0
    
        # objects
        self.fd = fd
        self.previous_cell = None
        self.next_cell = None

         # main parameters
        self.density_new = self.vehicles / self.length
        self.density_old = self.density_new
        self.flow = self.fd.get_flow(self.density_new)
        self.speed = 0
        if self.density_old:
            self.speed = self.flow / self.density_old
        
    #update parameters    
    def update(self):
        
        #inflow
        if self.previous_cell:
            self.inflow = self.previous_cell.outflow
            self.vehicles += self.inflow

        #density
        if self.vehicles:
            self.density_new = self.vehicles / self.length
            self.flow = self.fd.get_flow(self.density_new)
            self.speed = self.flow / self.density_new
        else:
            self.density = 0
            self.flow = 0
            self.speed = 0

        #outflow
        if self.next_cell:
            self.outflow = int(min((1-self.beta)*self.speed*self.density_old, -self.next_cell.fd.wavespeed*(self.next_cell.fd.critical_density-self.next_cell.density_old), self.fd.maximum_flow_total)*self.time_factor)
            self.vehicles -= self.outflow
        # last cell downstream
        else:
            self.outflow = int(min((1-self.beta)*self.speed*self.density_old, self.fd.maximum_flow_total)*self.time_factor)
            self.vehicles -= self.outflow
        self.density_old = self.density_new


        
        
