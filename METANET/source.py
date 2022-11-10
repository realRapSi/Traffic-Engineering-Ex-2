import numpy as np
class Source:
    def __init__(self, id, timestep, demand_points=[], demand_values=[]):
        self.id  = id
        self.demand_points = demand_points
        self.demand_values = demand_values
        self.current_demand = 0
        self.queue = 0
        self.vehicles = 0
        self.timestep = 0
        self.flow = 0
        self.speed = 0
        self.time_step = 0
        self.timestep_hour = timestep

        # objects
        self.next_cell = None

    def update(self, timestep):
        self.current_demand = self.demand_function(simstep= timestep)
        self.flow = min(self.current_demand + self.queue / self.timestep_hour, self.next_cell.fd.maximum_flow, self.next_cell.fd.wavespeed*(self.next_cell.fd.jam_density-self.next_cell.density))

        if self.flow < 0:
            self.flow = 0
        self.queue += (self.current_demand - self.flow) * self.timestep_hour
        self.time_step = timestep
        #print(self.current_demand + self.queue / self.timestep_hour, self.next_cell.fd.maximum_flow, self.next_cell.fd.wavespeed*(self.next_cell.fd.jam_density-self.next_cell.density))

    def dump_data(self, flow=[], density=[], speed=[]):
        pass

    def demand_function(self, simstep):
        current_timestep = simstep * self.timestep_hour
        return np.interp(current_timestep, self.demand_points, self.demand_values)

