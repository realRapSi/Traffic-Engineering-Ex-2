#libraries
import numpy as np
import matplotlib.pyplot as plt

#files
from cell import Cell
from fd import Fd
from source import Source

#parameters
SIMULATION_STEPS  = 500
TIMESTEP = 10/3600

#initialize FD
fundamental_diagram = Fd(lanes=3)

#initialize all cells
cell1 = Cell(1, 0, 0.5, 0, False, False, 0, 3, fundamental_diagram, TIMESTEP)
cell2 = Cell(2, 0, 0.5, 0, False, False, 0, 3, fundamental_diagram, TIMESTEP)
cell3 = Cell(3, 0, 0.5, 0, True, False, 0, 3, fundamental_diagram, TIMESTEP)
cell4 = Cell(4, 0, 0.5, 0, False, False, 0, 3, fundamental_diagram, TIMESTEP)
cell5 = Cell(5, 0, 0.5, 0, False, False, 0, 1, fundamental_diagram, TIMESTEP)
cell6 = Cell(6, 0, 0.5, 0, False, False, 0, 3, fundamental_diagram, TIMESTEP)

#define upstream demand
demand_upstream_points = [0, 450/3600, 3150/3600, 3600/3600, 5000/3600]
demand_upstream_values = [0, 4000, 4000, 0, 0]
#initialize upstream cell
upstream = Source(0, TIMESTEP, demand_upstream_points, demand_upstream_values)

#define on-ramp demand
demand_onramp_points = [0, 900/3600, 2700/3600, 3600/3600, 5000/3600]
demand_onramp_values = [0, 2500, 2500, 0, 0]
#initialize on-ramp cell
on_ramp1 = Source(7, TIMESTEP, demand_onramp_points, demand_onramp_values)

#linking cells
upstream.next_cell = cell1
cell1.previous_cell = upstream
cell1.next_cell = cell2
cell2.previous_cell = cell1
cell2.next_cell = cell3
cell3.previous_cell = cell2
cell3.next_cell = cell4
cell4.previous_cell = cell3
cell4.next_cell = cell5
cell5.previous_cell = cell4
cell5.next_cell = cell6
cell6.previous_cell = cell5
on_ramp1.next_cell = cell3
cell3.on_ramp = on_ramp1


cells = [upstream, cell1, cell2, cell3, cell4, cell5, cell6]

#testing
simstep = 0
flow_cell1 = []
flow_cell2 = []
speed_cell1 = []
speed_cell2 = []
density_cell1 = []
density_cell2 = []

source_outflow = []
source_queue = []

outflow_cell1 = []
outflow_cell2 = []

flow_data = np.zeros([7,SIMULATION_STEPS])
density_data = np.zeros([7,SIMULATION_STEPS])
#simulation
while(simstep<SIMULATION_STEPS):
    #simulation step
    for cell in cells:
        #calculate cell
        cell.update(timestep=simstep)

        #data plotting
        if cell.id == 1:
            flow_cell1.append(cell.flow)
            speed_cell1.append(cell.speed)
            density_cell1.append(cell.density)
            outflow_cell1.append(cell.outflow)
        elif cell.id == 2:
            flow_cell2.append(cell.flow)
            speed_cell2.append(cell.speed)
            density_cell2.append(cell.density)
            outflow_cell2.append(cell.outflow)
        elif cell.id == 0:
            source_outflow.append(cell.outflow)
            source_queue.append(cell.queue)
        
        cell.dump_data(flow_data, density_data)
    #advance simulation
    simstep += 1

xvalues = np.linspace(0, SIMULATION_STEPS, SIMULATION_STEPS)
yvalues = np.array([0, 1, 2, 3, 4, 5, 6])

X, Y = np.meshgrid(xvalues, yvalues)

fig1 = plt.figure()
fig1.suptitle('flow')
ax1 = fig1.add_subplot(111, projection='3d')
ax1.plot_wireframe(X, Y, flow_data)
plt.show()

fig2 = plt.figure()
fig2.suptitle('density')
ax2 = fig2.add_subplot(111, projection='3d')
ax2.plot_wireframe(X, Y, density_data)
plt.show()


#plot
fig, ax = plt.subplots(6, 1)

t = np.linspace(0, SIMULATION_STEPS, SIMULATION_STEPS)
ax[0].plot(t, flow_cell1)
ax[0].plot(t, flow_cell2)
ax[1].plot(t, speed_cell1)
ax[1].plot(t, speed_cell2)
ax[2].plot(t, density_cell1)
ax[2].plot(t, density_cell2)
ax[3].plot(t, outflow_cell1)
ax[3].plot(t, outflow_cell2)
ax[4].plot(t, source_outflow)
ax[5].plot(t, source_queue)

ax[0].set_title('flow')
ax[1].set_title('speed')
ax[2].set_title('density')
ax[3].set_title('Outflow')
ax[4].set_title('Upstream outflow')
ax[5].set_title('Upstream queue')

fig.tight_layout()
#plt.show()