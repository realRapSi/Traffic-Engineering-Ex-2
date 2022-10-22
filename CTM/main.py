#libraries
import numpy as np
import matplotlib.pyplot as plt

#files
from cell_new import Cell
from fd import Fd
from source import Source

#parameters
SIMULATION_STEPS  = 20
TIMESTEP = 10/3600

#initialize FD
fundamental_diagram = Fd(lanes=3)

#initialize all cells
cell1 = Cell(1, 0, 0.5, 0, False, False, 0, 3, fundamental_diagram, TIMESTEP)
cell2 = Cell(2, 0, 0.5, 0, False, False, 0, 3, fundamental_diagram, TIMESTEP)
cell3 = Cell(3, 0, 0.5, 0, False, False, 0, 3, fundamental_diagram, TIMESTEP)
#define demand and initialize upstream cell
demand = [2000]
upstream = Source(0, demand, TIMESTEP)

#linking cells
upstream.next_cell = cell1
cell1.previous_cell = upstream
cell1.next_cell = cell2
cell2.previous_cell = cell1
cell2.next_cell = cell3
cell3.previous_cell = cell2

cells = [upstream, cell1, cell2, cell3]

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

    #advance simulation
    simstep += 1


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
plt.show()