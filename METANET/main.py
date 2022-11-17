# TODO
# density in cell 2 is going above jam density -> identify impact of reduced outflow in cell 2 due to onramp -> fix issue to propagate density upstream


#libraries
import numpy as np
import matplotlib.pyplot as plt
np.seterr('raise')

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
cell1 = Cell(1, 0, 0.5, 0, False, False, 3, fundamental_diagram, TIMESTEP)
cell2 = Cell(2, 0, 0.5, 0, False, False, 3, fundamental_diagram, TIMESTEP)
cell3 = Cell(3, 0, 0.5, 0, True, False, 3, fundamental_diagram, TIMESTEP)
cell4 = Cell(4, 0, 0.5, 0, False, False, 3, fundamental_diagram, TIMESTEP)
cell5 = Cell(5, 0, 0.5, 0, False, False, 3, fundamental_diagram, TIMESTEP)
cell6 = Cell(6, 0, 0.5, 0, False, False, 3, fundamental_diagram, TIMESTEP)

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

#network structure
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

#data collection
flow_data = np.zeros([6,SIMULATION_STEPS])
density_data = np.zeros([6,SIMULATION_STEPS])
speed_data = np.zeros([6,SIMULATION_STEPS])

#simulation
simstep = 0

#simulation loop
while(simstep<SIMULATION_STEPS):
    #simulation step
    for cell in cells:

        #calculate cell
        cell.update(timestep=simstep)
        
        #get data for plots
        if type(cell) is Cell:
            cell.dump_data(flow_data, density_data, speed_data)
    #advance simulation
    simstep += 1

if True:
    #plotting
    xvalues = np.linspace(0, SIMULATION_STEPS, SIMULATION_STEPS)
    yvalues = np.array([1, 2, 3, 4, 5, 6])
    X, Y = np.meshgrid(xvalues, yvalues)

    #flow graph
    fig1 = plt.figure()
    fig1.suptitle('flow', fontsize=32)
    ax1 = fig1.add_subplot(111, projection='3d')
    ax1.plot_wireframe(X, Y, flow_data)
    plt.show()

    #density graph
    fig2 = plt.figure()
    fig2.suptitle('density', fontsize=32)
    ax2 = fig2.add_subplot(111, projection='3d')
    ax2.plot_wireframe(X, Y, density_data)
    plt.show()

    #speed graph
    fig3 = plt.figure()
    fig3.suptitle('speed', fontsize=32)
    ax3 = fig3.add_subplot(111, projection='3d')
    ax3.plot_wireframe(X, Y, speed_data)
    plt.show()