class Cell:
    def __init__(self, id, vehicles, length, flow, has_onramp, has_offramp, lanes, fd, timefactor, thao=22, ny=15, kappa=10, delta=1.4):
        self.id = id
        self.vehicles = vehicles
        self.length = length
        self.flow = flow
        self.has_onramp = has_onramp
        self.has_offramp = has_offramp
        self.lanes = lanes
        self.time_factor = timefactor
        self.speed = 100
        self.time_step = 0
        self.r = 0
        self.density = 0

        #model parameters
        self.thao = thao / 3600
        self.ny = ny
        self.kappa = kappa
        self.delta = delta
        self.lambdai = self.lanes

        #objects
        self.fd = fd
        self.previous_cell = None
        self.next_cell = None
        self.on_ramp = None
        
    #update parameters    
    def update(self, timestep):
        self.density_update()
        self.speed_update()
        self.flow_update()
        self.time_step = timestep


    def speed_update(self):
        if self.previous_cell and self.next_cell:
            self.speed = self.speed + self.time_factor / self.thao * (self.fd.get_speed(self.density) - self.speed) \
                + self.time_factor / self.length * self.speed * (self.previous_cell.speed - self.speed) \
                - (self.ny * self.time_factor) / (self.thao * self.length) * (self.next_cell.density - self.density) / (self.density + self.kappa) \
                - (self.delta * self.time_factor) / (self.length * self.lambdai) * (self.r * self.speed) / (self.density + self.kappa)
        
        if not self.next_cell:
            self.speed = self.speed + self.time_factor / self.thao * (self.fd.get_speed(self.density) - self.speed) \
                + self.time_factor / self.length * self.speed * (self.previous_cell.speed - self.speed) \
                - (self.delta * self.time_factor) / (self.length * self.lambdai) * (self.r * self.speed) / (self.density + self.kappa)
    def flow_update(self):
        self.flow = self.fd.get_flow(self.density)

    def density_update(self):
        if self.previous_cell:
            self.density = self.density + self.time_factor / (self.length * self.lambdai) * (self.previous_cell.flow - self.flow + self.r)

    def dump_data(self, flow=[], density=[], speed=[],):
        flow[self.id-1, self.time_step] = self.flow
        density[self.id-1, self.time_step] = self.density
        speed[self.id-1, self.time_step] = self.speed




        
        
