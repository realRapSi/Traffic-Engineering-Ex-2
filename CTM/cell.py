class Cell:
    def __init__(self, id, vehicles, length, flow, has_onramp, has_offramp, lanes, fd, timefactor):
        self.id = id
        self.vehicles = vehicles
        self.length = length
        self.flow = flow
        self.has_onramp = has_onramp
        self.has_offramp = has_offramp
        self.beta = 0
        self.lanes = lanes
        self.time_factor = timefactor
        self.inflow = 0
        self.outflow = 0
        self.time_step = 0
    
        # objects
        self.fd = fd
        self.previous_cell = None
        self.next_cell = None
        self.on_ramp = None
        self.off_ramp = None

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
            if self.has_onramp:
                self.inflow = self.previous_cell.outflow + self.on_ramp.outflow
            else:
                self.inflow = self.previous_cell.outflow

        #outflow
        if self.next_cell:
            if not self.next_cell.has_onramp:
                self.outflow = min((1-self.beta)*self.speed*self.density, self.next_cell.fd.wavespeed * (self.next_cell.fd.jam_density - self.next_cell.density), self.fd.maximum_flow)
            else:
                if self.next_cell.on_ramp.alinea:
                    self.next_cell.on_ramp.on_ramp_outflow_alinea(self.time_step, self.next_cell.fd.critical_density, self.next_cell.density)
                    self.outflow = min((1-self.beta)*self.speed*self.density, self.next_cell.fd.wavespeed * (self.next_cell.fd.jam_density - self.next_cell.density), self.fd.maximum_flow)
                else:
                    temp_outflow_cell = min((1-self.beta)*self.speed*self.density, self.next_cell.fd.wavespeed * (self.next_cell.fd.jam_density - self.next_cell.density), self.fd.maximum_flow)
                    temp_outflow_on_ramp = self.next_cell.on_ramp.on_ramp_temp_outflow(timestep)

                    downstream_supply = (self.next_cell.fd.wavespeed * (self.next_cell.fd.jam_density - self.next_cell.density))
                    if (temp_outflow_on_ramp + temp_outflow_cell) <= downstream_supply:
                        self.outflow = temp_outflow_cell
                        self.next_cell.on_ramp.on_ramp_update(temp_outflow_on_ramp)
                    else:
                        self.outflow = temp_outflow_cell / (temp_outflow_cell + temp_outflow_on_ramp) * downstream_supply
                        self.next_cell.on_ramp.on_ramp_update(temp_outflow_on_ramp / (temp_outflow_cell + temp_outflow_on_ramp) * downstream_supply)


            if self.outflow < 0:
                self.outflow = 0

        # last cell downstream
        elif not self.next_cell:
            self.outflow = min((1-self.beta)*self.speed*self.density, self.fd.maximum_flow)

        #vehicles
        self.vehicles = self.vehicles + self.time_factor * (self.inflow - self.outflow)

        #parameters
        if self.vehicles:
            self.density = self.vehicles / self.length
            self.flow = self.fd.get_flow(self.density)
            self.speed = self.flow / self.density
        else:
            self.density = 0
            self.flow = 0
            self.speed = 0

        self.time_step = timestep

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




        
        
