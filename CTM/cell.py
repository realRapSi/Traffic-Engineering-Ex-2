class Cell:
    def __init__(self, id, vehicles, length, flow, has_onramp, has_offramp, beta, lanes, fd, timefactor):
        self.id = id
        self.vehicles = vehicles
        self.length = length
        self.flow = flow
        self.has_onramp = has_onramp
        self.has_offramp = has_offramp
        self.beta = beta
        self.lanes = lanes
        self.time_factor = timefactor
        
        self.inflow = 0
        self.outflow = 0

        self.time_step = 0
    
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
    def update(self, timestep):
        
        #inflow
        if self.previous_cell:
            self.inflow = self.previous_cell.outflow
            if self.inflow < 0:
                raise ValueError("negative inflow:", self.inflow)
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
            self.outflow = min((1-self.beta)*self.speed*self.density_old, abs(-self.next_cell.fd.wavespeed*(self.next_cell.fd.critical_density-self.next_cell.density_old)/self.time_factor), self.fd.maximum_flow_total)*self.time_factor
            #print('speed*density:', self.time_factor * (1-self.beta)*self.speed*self.density_old)
            #print('next cell intake:', -self.next_cell.fd.wavespeed*(self.next_cell.fd.critical_density-self.next_cell.density_old))
            #print('max flow:', self.fd.maximum_flow_total)          
            if self.outflow < 0:
                self.outflow = 0
            temp_vehicles = self.vehicles
            self.vehicles -= self.outflow
            if self.vehicles < 0:
                self.vehicles = 0
        # last cell downstream
        else:
            self.outflow = min((1-self.beta)*self.speed*self.density_old, self.fd.maximum_flow_total)*self.time_factor
            self.vehicles -= self.outflow

        self.density_old = self.density_new
        self.time_step = timestep


    def dump_data(self, array=[]):
        array.append([self.id, self.density_old, self.flow, self.time_step, self.vehicles, self.inflow, self.outflow])



        
        
