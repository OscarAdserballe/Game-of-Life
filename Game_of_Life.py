import random
import copy
import time
import datetime

# builds empty grid
def build_empty_grid(dimension):
    grid = []
    for i in range(dimension):
        grid.append([0]*dimension)
    return grid

# Fills in first grid
def build_first_grid(dimension, number_of_alive_cells):
    grid = build_empty_grid(dimension)
    for i in range(number_of_alive_cells):
        l = random.choice(range(dimension))
        c = random.choice(range(dimension))
        while grid[l][c]==1:
            l = random.choice(range(dimension))
            c = random.choice(range(dimension))
        grid[l][c]=1

    return grid


# To solve the question of how borders should be treated
# this one transforms the grid into a torus 
# example:
#                       0 0 0 0 0
#     0 1 0             0 0 1 0 0
#     1 0 0      ->     0 1 0 0 1
#     0 0 0             0 0 0 0 0
#                       0 0 1 0 0
def transform_to_circular_grid(original_grid):                                 
    if type(original_grid) == list:                                             
        # Generate copy of grid                                                
        new_grid = copy.deepcopy(original_grid)                                 
        # Adding the new left-most and right-most column                        
        for row in new_grid:
            row.insert(0, row[-1])
            row.insert(len(row), row[1])
        # Adding the top and bottom rows
        top_row_copy = new_grid[0]
        bottom_row_copy = new_grid[-1]
        new_grid.insert(0, bottom_row_copy)
        new_grid.insert(len(new_grid), top_row_copy)
    return new_grid

# for each square, it counts the number of neighbours which will determine
# the state for the square for the next generation
def count_neighbour_cells(x, y, some_transformed_grid):
    # adjust the x and y coordinate to the new grid by adding 1 to each
    x += 1
    y += 1
    # Look at nearby cells and count how many are 1s
    neighbours = 0

    # possible optimisation is using two for loops
    # with i and j, where they go between -1 and 1

    if some_transformed_grid[x+1][y-1] == 1:
        neighbours += 1
    if some_transformed_grid[x+1][y] == 1:
        neighbours += 1
    if some_transformed_grid[x+1][y+1] == 1:
        neighbours += 1
    if some_transformed_grid[x][y+1] == 1:
        neighbours += 1
    if some_transformed_grid[x][y-1] == 1:
        neighbours += 1
    if some_transformed_grid[x-1][y-1] == 1:
        neighbours += 1
    if some_transformed_grid[x-1][y] == 1:
        neighbours += 1
    if some_transformed_grid[x-1][y+1] == 1:
        neighbours += 1
    
    return neighbours

# generate the next generation of the grid
def next_gen(some_grid):
    previous_grid_number_of_alive_cells = 0
    # Start by transforming the grid to a circular one, so we can accurately count the amount of neighbours
    transformed_grid = transform_to_circular_grid(some_grid)
    next_gen_grid = build_empty_grid(len(some_grid))
    for x in range(len(some_grid)):
        for y in range(len(some_grid[0])):     #Underlying assumption that the grid's dimensions are the same
            if some_grid[x][y] == 1:
                previous_grid_number_of_alive_cells += 1
            next_gen_grid[x][y] = [some_grid[x][y], count_neighbour_cells(x, y, transformed_grid)]

    #Iterating through the new grid, and replacing the count of how many neighbours with the appropriate cell, either living or dead (1 or 0)
    #Rules are as follows:
    #Live cell with fewer than 2 neighbours die
    #Live cell with two or three live neighbours lives on
    #Live cell with more than 3 neighbours die
    #Dead cell with exactly three becomes a live cell

    for x in range(len(next_gen_grid)):
        for y in range(len(next_gen_grid[0])):
            if next_gen_grid[x][y] == [1, 1] or next_gen_grid[x][y] == [1, 0]:
                next_gen_grid[x][y] = 0
            elif next_gen_grid[x][y] == [1, 2] or next_gen_grid[x][y] == [1, 3]:
                next_gen_grid[x][y] = 1
            elif next_gen_grid[x][y][0] == 1 and next_gen_grid[x][y][1] > 3:
                next_gen_grid[x][y] = 0
            elif next_gen_grid[x][y] == [0, 3]:
                next_gen_grid[x][y] = 1
            elif next_gen_grid[x][y][0] == 0:   #Could technically use the else block for this, but wish to keep it for error logging instead
                next_gen_grid[x][y] = 0
            else:
                print("A fatal error occured!")


    return next_gen_grid, previous_grid_number_of_alive_cells

# display the grid in console
def display_grid(some_grid):
    for line in some_grid:
        for i in line:
            print("|", end="")
            if i==1:
                print("*", end="")
            else:
                print(" ", end="")
        print("|")
    

# the main game loop that will keep going until a steady state is reached
def game_loop(dimension, delay, initial_amount_of_live_cells):
    grid = build_first_grid(dimension, initial_amount_of_live_cells)
    next_grid = []
    number_of_generations = 0
    while number_of_generations<500:
        display_grid(grid)
        next_grid, number_of_cells = next_gen(grid)
        if grid == next_grid:
            break
        print("This is generation nr.", number_of_generations, "containing", number_of_cells, "live cells.")
        print()
        time.sleep(delay)
        number_of_generations += 1
        grid = next_grid
    if number_of_generations < 500:
        print("The population has reached a stable configuration after", number_of_generations, "generations with", number_of_cells, "live cells!")
    else:
        print("There is a high likelihood the population will sustain infinitely. We're stopping the program for the sake of your pc.")


time_before = datetime.datetime.now()
game_loop(10, 0.1, 40) #Game loop function takes 3 parametres: the grid's dimensions, the amount of delay between each generation showing in the console, and the starting amount of live cells.
time_after = datetime.datetime.now()
time_passed = time_after - time_before
print("Program has been running for ", time_passed)