# Game-of-Life
#### Description: Conway's Game of Life in Python using matplotlib

![Homepage](/Demos/life50.gif)

An implementation of John Conway's "Game of Life" in Python.
Based on the user's system, the program either outputs a graphical version as seen above, or a text-based on in case the user does not have the module matplotlib.

The user is simply left to input the grid size they want to simulate as well as the number of live cells in the initial state.

Instead of having hard edges, the design choice made was to simulate the game as though the grid was a torus, i.e. a donut. This means that the left-hand edge connects to the right-hand edge and counts its neighbours over there.
Can easily use a lot of memory and is in no way optimised, so look out for that in case you want to try it out. It gets slightly out of hand once the user specifies a grid past 200*200 in size

There's also another program to perform a quick "Population analysis". This tries to depict the estimated life span of grids based on how many live cells they initially have.

For more detail, please see the overly-elaborate explanation inside the Presentation and Explanation folder.
