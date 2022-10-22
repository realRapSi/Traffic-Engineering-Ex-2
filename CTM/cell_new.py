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
        self.density = self.vehicles / self.length
        self.flow = self.fd.get_flow(self.density)
        self.speed = 0
        if self.density:
            self.speed = self.flow / self.density
        
    #update parameters    
    def update(self, timestep):
        
        #inflow
        if self.previous_cell:
            self.inflow = self.previous_cell.outflow
            if self.inflow < 0:
                raise ValueError("negative inflow:", self.inflow)
            
            self.vehicles += self.time_factor * self.inflow
            self.density = self.vehicles / self.length

        #outflow
        if self.next_cell:
            self.outflow = min((1-self.beta)*self.speed*self.density, self.next_cell.fd.wavespeed * (self.next_cell.fd.critical_density - self.next_cell.density), self.fd.maximum_flow_total)

            if self.outflow < 0:
                self.outflow = 0

        # last cell downstream
        else:
            self.outflow = min((1-self.beta)*self.speed*self.density, self.fd.maximum_flow_total)

        #vehicles
        self.vehicles = self.vehicles + self.time_factor * (self.inflow - self.outflow)

        #density
        if self.vehicles:
            self.density = self.vehicles / self.length
            self.flow = self.fd.get_flow(self.density)
            self.speed = self.flow / self.density
        else:
            self.density = 0
            self.flow = 0
            self.speed = 0

        self.time_step = timestep

        print('Cell Nr:', self.id)
        print('density:', self.density)
        print('flow:', self.flow)
        print('vehicles:', self.vehicles)
        print('inflow:', self.inflow)
        print('outflow:', self.outflow)
        print('cell demand:', (1-self.beta)*self.speed*self.density)
        if self.next_cell:
            print('downstream supply:', self.next_cell.fd.wavespeed * (self.next_cell.fd.critical_density - self.next_cell.density))
        print('max outflow:', self.fd.maximum_flow_total)
        print('------------------')


    def dump_data(self, array=[]):
        array.append([self.id, self.density, self.flow, self.time_step, self.vehicles, self.inflow, self.outflow])



        
        
