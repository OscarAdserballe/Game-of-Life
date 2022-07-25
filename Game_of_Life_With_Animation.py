import random                  
import copy                  
import time
# Most users don't have matplotlib, however, and so it is tested whether the user has this module using a try/except block. 
# Program will only output a text-based version of the game if the user doesn't have matplotlib
# If the user does have this library, a more vivid animation of the game will display, using the FuncAnimation function from the matplotlib library.                  
try:                         
    import matplotlib                       
    from matplotlib import pyplot as plt    
    has_module= True                        
except ModuleNotFoundError:
    has_module = False

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
    
# helper functino that counts how many times a sub-list is contained in a list
#Function determining how many times a list is contained inside a list of lists. Used in the next function to determine whether that grid has already been seen an x amount of times
def nb_times_list_in_list(some_list, list_of_lists): 
    counter = 0
    for i in list_of_lists:
        if i == some_list:  
            counter += 1
    return counter  

#The function responsible for actually running the game, which takes 3 parametres: The delay is the time in seconds that will pass between each generation; grid is the grid that the player will play with, which has already been randomly generated per their instructions; and the display-parametre which is set by default to True, which tells the function whether or not to display the game.
def game_loop(delay, grid, display=True):   
    # store previous gens.
    # may potentially use a lot of memory       
    previous_grids = [] 
    next_grid = []
    number_of_generations = 1   
    # if grid has already been seen before, it's in an infinite loop, but not unchanging.
    # deterministic nature of the game.
    # chosen 5 instead of 2, so the user gets to see the "last" grid a few times
    while nb_times_list_in_list(grid, previous_grids) < 5:  
        previous_grids.append(grid) 
        next_grid, number_of_cells = next_gen(grid)
        # if user did not have matplotlib  
        if display:            
            display_grid(grid)
            print("This is generation nr.", number_of_generations, "containing", number_of_cells, "live cells.")
            print()     

        # if steady state
        if grid == next_grid:
            break

        number_of_generations += 1      
        grid = next_grid
        time.sleep(delay)   
    if not display:        
        return number_of_generations

# Ask for user inputs for the grid, and check whether they're appropriate. 
# The checks done on the inputs, however, are in no way exhaustive, and a creative user could easily break the program.
try:                
    dimension = int(input("What should the dimension of the grid be? Please answer with a single integer\n"))
    percentage_to_fill_of_grid = int(input("What percentage of the grid should contain live cells\n"))
    if dimension <= 0 or percentage_to_fill_of_grid > 100 or percentage_to_fill_of_grid <= 0:   #Certain conditions imposed on user-inputs. In case they are not met, the user is asked to run the program again later in the final else block of the code.
        run_program = False
    else:
        run_program = True
except:
    print("Please run this program again, and input integers and proper values. Note, the percentage input should be a whole number from 0 to 100, and the dimension can be any whole number larger than 0.")

initial_amount_of_live_cells = int(percentage_to_fill_of_grid * dimension*dimension/100)    #Basic conversion from a percentage of a grid that should be filled, to the numerical amount of cells that should be alive in the first grid.
grid = build_first_grid(dimension, initial_amount_of_live_cells)    #Builds the initial grid that will be used henceforth.

# if user has matplotlib, visual version will run
if has_module and run_program:
    fig = plt.figure()         
    ax = plt.axes()    
    #.imshow() displays the plot, as if it were a grid - exactly what is needed for our purposes. 
    # cmap is short for the colour map and determines the colors that will be used. 
    # Binary just uses black and white. 
    # This line is the first frame in the animation         
    img = ax.imshow(grid, cmap="binary")        

    #Creates the next frame for the animation
    def animate(i, img, grid):          
        print("Generation", i+1)                 
        new_grid = next_gen(grid)[0]
        img.set_data(new_grid)
        grid[:] = new_grid[:]
        return img

    #Using game_loop to determine how many frames the animation should run, otherwise it'll just keep going while using an ever-increasing amount of memory
    amount_of_frames = game_loop(0, grid, display=False)    
    print("Animation will run for", amount_of_frames, "frames/generations")
    animation = matplotlib.animation.FuncAnimation(fig, animate, fargs=(img, grid), interval=300, frames=amount_of_frames, repeat=False) 
    #plt.show()  #displays the plot on the user's screen

    #In case one would like to save the animation as a gif, instead of immediately running it in python
    animation.save('life10slow.gif')       

# user will only see text-based version due to lackign matplotlib
elif run_program and not has_module:
    game_loop(5, grid)          

else:
    print("Please run this program again, and input integers and proper values. Note, the percentage input should be a whole number from 0 to 100, and the dimension can be any whole number larger than 0.")