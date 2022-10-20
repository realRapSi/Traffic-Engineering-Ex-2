from cell import Cell
from fd import Fd

fundamental_diagram = Fd(lanes=3)

cell1 = Cell(1, 200, 0.5, 0, False, False, 0, 3, fundamental_diagram, time_seconds=15)
cell2 = Cell(2, 0, 0.5, 0, False, False, 0, 3, fundamental_diagram, time_seconds=15)
cell3 = Cell(3, 0, 0.5, 0, False, False, 0, 3, fundamental_diagram, time_seconds=15)

cell1.next_cell = cell2
cell2.previous_cell = cell1
cell2.next_cell = cell3
cell3.previous_cell = cell2

cells = [cell1, cell2, cell3]

#testing
x = 0
while(x<90):
    for cell in cells:
        print("(", cell.id, ")", cell.vehicles)
        print("--------------------------------")
        cell.update()
        print(cell.vehicles)
        print("--------------------------------")

    x+=1