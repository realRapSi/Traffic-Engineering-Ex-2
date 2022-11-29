#libraries
import numpy as np
import matplotlib.pyplot as plt
np.seterr('raise')

#files
from cell import Cell
from fd import Fd
from source import Source

#scenario selection
scenario = input('Scenario? a/b/c: ')
alinea = input('Alinea ramp metering active? y/n: ')
alinea_k = 0
alinea_optimisation = False
if alinea == 'y':
    try:
        alinea_k = float(input('K value for ALINEA? (float): ' ))
        alinea_optimisation = input('run k factor optimisation? y/n: ')
    except:
        print('not a float value. Enter a float value')
        alinea_k = float(input('K value for ALINEA?: '))
        alinea_optimisation = input('run k factor optimisation? y/n: ')

if alinea_optimisation == 'y':
    alinea_optimisation = True
else:
    alinea_optimisation = False
#parameters default
SIMULATION_STEPS  = 500
TIMESTEP = 10/3600
ALINEA = False
ALINEA_K = 0
LANES_PER_CELL = 3
LANES_PER_CELL_5= 3
DEMAND_PEAK_UPSTREAM = 4000
DEMAND_PEAK_ONRAMP = 2000

if scenario == 'a':
    if alinea == 'y':
        ALINEA = True
        ALINEA_K = alinea_k
    else:
        ALINEA = False
        ALINEA_K = 0
    LANES_PER_CELL = 3
    LANES_PER_CELL_5= 3
    DEMAND_PEAK_UPSTREAM = 4000
    DEMAND_PEAK_ONRAMP = 2000

elif scenario == 'b':
    if alinea == 'y':
        ALINEA = True
        ALINEA_K = alinea_k
    else:
        ALINEA = False
        ALINEA_K = 0
    LANES_PER_CELL = 3
    LANES_PER_CELL_5= 3
    DEMAND_PEAK_UPSTREAM = 4000
    DEMAND_PEAK_ONRAMP = 2500

elif scenario == 'c':
    if alinea == 'y':
        ALINEA = True
        ALINEA_K = alinea_k
    else:
        ALINEA = False
        ALINEA_K = 0
    LANES_PER_CELL = 3
    LANES_PER_CELL_5= 1
    DEMAND_PEAK_UPSTREAM = 1500
    DEMAND_PEAK_ONRAMP = 1500

#initialize all cells
cell1 = Cell(1, 0, 0.5, 0, False, False, LANES_PER_CELL, Fd(lanes=LANES_PER_CELL), TIMESTEP)
cell2 = Cell(2, 0, 0.5, 0, False, False, LANES_PER_CELL, Fd(lanes=LANES_PER_CELL), TIMESTEP)
cell3 = Cell(3, 0, 0.5, 0, True, False, LANES_PER_CELL, Fd(lanes=LANES_PER_CELL), TIMESTEP)
cell4 = Cell(4, 0, 0.5, 0, False, False, LANES_PER_CELL, Fd(lanes=LANES_PER_CELL), TIMESTEP)
cell5 = Cell(5, 0, 0.5, 0, False, False, LANES_PER_CELL_5, Fd(lanes=LANES_PER_CELL_5), TIMESTEP)
cell6 = Cell(6, 0, 0.5, 0, False, False, LANES_PER_CELL, Fd(lanes=LANES_PER_CELL), TIMESTEP)

#define upstream demand
demand_upstream_points = [0, 450/3600, 3150/3600, 3600/3600, 5000/3600]
demand_upstream_values = [0, DEMAND_PEAK_UPSTREAM, DEMAND_PEAK_UPSTREAM, 0, 0]
#initialize upstream cell
upstream = Source(0, TIMESTEP, demand_upstream_points, demand_upstream_values, False)

#define on-ramp demand
demand_onramp_points = [0, 900/3600, 2700/3600, 3600/3600, 5000/3600]
demand_onramp_values = [0, DEMAND_PEAK_ONRAMP, DEMAND_PEAK_ONRAMP, 0, 0]
#initialize on-ramp cell
on_ramp1 = Source(7, TIMESTEP, demand_onramp_points, demand_onramp_values, ALINEA, ALINEA_K)

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


#for optimsation of k factor (alinea)
temp_best_k = 0
temp_min_vht = None
temp_min_vht = None
k_runner = 0

#simulation
while k_runner <= 100:
    #initialize on-ramp cell
    if alinea_optimisation:
        on_ramp1 = Source(7, TIMESTEP, demand_onramp_points, demand_onramp_values, ALINEA, k_runner)
    else:
        on_ramp1 = Source(7, TIMESTEP, demand_onramp_points, demand_onramp_values, ALINEA, ALINEA_K)

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

    #network order
    cells = [upstream, cell1, cell2, cell3, cell4, cell5, cell6]

    #data collection
    flow_data = np.zeros([6,SIMULATION_STEPS])
    density_data = np.zeros([6,SIMULATION_STEPS])
    speed_data = np.zeros([6,SIMULATION_STEPS])
    vkt = 0
    vht = 0

    #simulation
    simstep = 0

    #simulation loop
    while(simstep<SIMULATION_STEPS):
        #simulation step
        for cell in cells:

            #calculate cell
            cell.update(timestep=simstep)

            #update performance parameters
            temp_vkt, temp_vht = cell.performance_calculation()
            vkt += temp_vkt
            vht += temp_vht
            
            #get data for plots
            if type(cell) is Cell:
                cell.dump_data(flow_data, density_data, speed_data)
        #advance simulation
        simstep += 1

    if not alinea_optimisation:
        print('VHT:', vht, 'VKT:', vkt)
        break
    else:
        if not temp_min_vht == None:
            if temp_min_vht > vht:
                temp_min_vht = vht
                temp_min_vkt = vkt
                temp_best_k = k_runner
        else:
            temp_min_vht = vht
            temp_min_vkt = vkt

        k_runner += 0.1
if alinea_optimisation: 
    print('optimized results\nBest K:',temp_best_k, 'Minimal VHT:',temp_min_vht, 'Minimal VKT:',temp_min_vkt)

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
    ax1.set_ylabel('Cell #')
    ax1.set_xlabel('Time [10 s]')
    ax1.set_zlabel('Flow [veh / h]')
    plt.show()

    #density graph
    fig2 = plt.figure()
    fig2.suptitle('density', fontsize=32)
    ax2 = fig2.add_subplot(111, projection='3d')
    ax2.plot_wireframe(X, Y, density_data)
    ax2.set_ylabel('Cell #')
    ax2.set_xlabel('Time [10 s]')
    ax2.set_zlabel('Density [veh / km]')
    plt.show()

    #speed graph
    fig3 = plt.figure()
    fig3.suptitle('speed', fontsize=32)
    ax3 = fig3.add_subplot(111, projection='3d')
    ax3.plot_wireframe(X, Y, speed_data)
    ax3.set_ylabel('Cell #')
    ax3.set_xlabel('Time [10 s]')
    ax3.set_zlabel('Velocity [km / h]')
    plt.show()