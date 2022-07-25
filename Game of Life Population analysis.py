from Game_of_Life import next_gen
from Game_of_Life import build_first_grid
import math
import matplotlib.pyplot as plt

# brief program just to study how the amount of initial live cells affect the 
# the estimated survival time of a given grid.
# and outputs in the form of a grid.

def main_loop(dimension, live_cells):
    grid = build_first_grid(dimension, live_cells)
    next_grid = []
    number_of_generations = 0
    while number_of_generations<500:
        next_grid, number_of_cells = next_gen(grid)
        if grid == next_grid:
            break
        number_of_generations += 1
        grid = next_grid
    cell_population_at_stable_state = number_of_cells
    generations_till_stable_state = number_of_generations
    return cell_population_at_stable_state, generations_till_stable_state


dimension = 20
inital_amount_of_live_cells = 0
iterations_per_value = 5

dict_with_values = {}
max_amount_of_cells_in_stable_population = 0
for i in range(100):
    inital_amount_of_live_cells += 4
    sum_of_cell_populations = 0
    sum_of_generations = 0
    for j in range(iterations_per_value):
        cells_at_stable_state, generations_till_stable_state = main_loop(dimension, inital_amount_of_live_cells)
        sum_of_cell_populations += cells_at_stable_state
        sum_of_generations += generations_till_stable_state
        if cells_at_stable_state > max_amount_of_cells_in_stable_population:
            max_amount_of_cells_in_stable_population = cells_at_stable_state
    average_of_cell_populations = round(sum_of_cell_populations/iterations_per_value, 2)
    average_of_generations = round(sum_of_generations/iterations_per_value, 2)
    list_to_add_to_dict = [average_of_cell_populations, round(average_of_generations/100, 2)]
    #print(average_of_cell_populations, "is the average amount of living cells at a populations stable state, with", inital_amount_of_live_cells, "cells to start with in a", dimension, "x", dimension, "grid")
    dict_with_values[inital_amount_of_live_cells] = list_to_add_to_dict
print(max_amount_of_cells_in_stable_population)

x_axis_data = []
y_axis_data = []
for i in dict_with_values:
    x_axis_data.append(i)
    y_axis_data.append(dict_with_values[i][0])
plt.plot(x_axis_data, y_axis_data)

x_axis_data = []
y_axis_data = []
for i in dict_with_values:
    x_axis_data.append(i)
    y_axis_data.append(dict_with_values[i][1])
plt.plot(x_axis_data, y_axis_data)

plt.axhline(y=0, color="black", linestyle="dashed")

plt.show()
