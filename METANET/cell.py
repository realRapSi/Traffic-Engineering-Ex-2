class Cell:
    def __init__(self, id, vehicles, length, flow, has_onramp, has_offramp, lanes, fd, timefactor, tao=22, ny=15, kappa=10, delta=1.4):
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
        self.tao = tao / 3600
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
        self.time_step = timestep

        if self.has_onramp:
            self.r = self.on_ramp.flow

        self.flow_update()
        self.density_update()
        self.speed_update()
        

    def speed_update(self):
        if self.previous_cell and self.next_cell:
            self.speed = self.speed + self.time_factor / self.tao * (self.fd.get_speed(self.density) - self.speed) \
                + (self.time_factor / self.length) * self.speed * (self.previous_cell.speed - self.speed) \
                - (self.ny * self.time_factor) / (self.tao * self.length) * (self.next_cell.density - self.density) / (self.density + self.kappa) \
                - (self.delta * self.time_factor) / (self.length * self.lambdai) * (self.r * self.speed) / (self.density + self.kappa)
                 
        if not self.next_cell:
            self.speed = self.speed + self.time_factor / self.tao * (self.fd.get_speed(self.density) - self.speed) \
                + self.time_factor / self.length * self.speed * (self.previous_cell.speed - self.speed) \
                - (self.delta * self.time_factor) / (self.length * self.lambdai) * (self.r * self.speed) / (self.density + self.kappa)
                
        if self.speed < 0:
            self.speed = 0
            
    def flow_update(self):
        self.flow = min(self.density * self.speed, self.fd.maximum_flow)
        if self.next_cell:
            self.flow = min(self.density * self.speed, self.fd.maximum_flow, self.next_cell.fd.wavespeed * (self.next_cell.fd.jam_density - self.next_cell.density))
            if self.next_cell.has_onramp:
                if self.next_cell.on_ramp.alinea:
                    self.next_cell.on_ramp.on_ramp_outflow_alinea(self.time_step, self.next_cell.fd.critical_density, self.next_cell.density)
                else:
                    temp_outflow_cell = self.flow
                    temp_outflow_on_ramp = self.next_cell.on_ramp.on_ramp_temp_outflow(self.time_step)
                    downstream_supply = self.next_cell.fd.wavespeed * (self.next_cell.fd.jam_density - self.next_cell.density)
                    if (temp_outflow_on_ramp + temp_outflow_cell) <= downstream_supply:
                        self.flow = temp_outflow_cell
                        self.next_cell.on_ramp.on_ramp_update(temp_outflow_on_ramp)
                    else:
                        self.flow = temp_outflow_cell / (temp_outflow_cell + temp_outflow_on_ramp) * downstream_supply
                        self.next_cell.on_ramp.on_ramp_update(temp_outflow_on_ramp / (temp_outflow_cell + temp_outflow_on_ramp) * downstream_supply)
      
    def density_update(self):
        if self.previous_cell:
            self.density = self.density + self.time_factor / (self.length * self.lambdai) * (self.previous_cell.flow - self.flow + self.r)

    def dump_data(self, flow=[], density=[], speed=[],):
        flow[self.id-1, self.time_step] = self.flow
        density[self.id-1, self.time_step] = self.density
        speed[self.id-1, self.time_step] = self.speed

    def performance_calculation(self):
        cell_vkt = self.time_factor * self.flow * self.length
        cell_vht = self.time_factor * self.density * self.length

        if self.has_onramp:
            cell_vht += self.on_ramp.queue * self.time_factor

        return cell_vkt, cell_vht


        
        
