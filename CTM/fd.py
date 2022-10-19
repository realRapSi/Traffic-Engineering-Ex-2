class FD:
    def __init__(self, freeflow_speed=100, jam_density=200, max_flow=200, lanes):
        self.freeflow_speed = freeflow_speed
        self.jam_density = jam_density
        self.max_flow = max_flow
        self.lanes = lanes