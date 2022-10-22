class Source:
    def __init__(self, id, demand, timestep):
        self.id  = id
        self.demand = demand
    
        self.queue = 0
        self.vehicles = 0
        self.timestep = 0
        self.outflow = 0
        self.time_step = 0

        self.timestep_hour = timestep

        # objects
        self.next_cell = None

    def update(self, timestep):
        
        self.outflow = min(self.demand[0] + self.queue*self.timestep_hour, self.next_cell.fd.maximum_flow_total, self.next_cell.fd.wavespeed*(self.next_cell.fd.critical_density-self.next_cell.density))
        print(self.next_cell.fd.maximum_flow_total, self.demand[0] + self.queue*self.timestep_hour, abs(-self.next_cell.fd.wavespeed*(self.next_cell.fd.critical_density-self.next_cell.density)))
        print(self.outflow)
        print('---------------------------')
        if self.outflow < 0:
            self.outflow = 0
        self.queue = self.queue + (self.demand[0] - self.outflow) * self.timestep_hour
        self.time_step = timestep

    def dump_data(self, array=[]):
        array.append([self.id, self.time_step, self.outflow, self.queue])


    #todo
    def demand_function(self):
        pass