# import pygame and priority queue
import pygame
from queue import PriorityQueue
import tkinter as tk
from tkinter import filedialog

# Charles Jandura
# 4/8/2024
# Data Structures And Algorithms Final Project

# create a width constant of 1000
WIDTH = 1000

# create pygame window with heigh and length equal to width
WIN = pygame.display.set_mode((WIDTH, WIDTH))

# set the pygame title to Pathy
pygame.display.set_caption("Pathy")

# color constants used for drawing nodes
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
PINK = (255, 153, 204)

# create instruction screen, set title, geometry, and scaling
root = tk.Tk()
root.title("Pathy Introduction")
root.geometry("300x300")
root.tk.call('tk', 'scaling', 3.0)


# instruction screen welcome label creation and grid placement
welcomeLabel = tk.Label(root, text="Welcome to Pathy!")
welcomeLabel.grid(column=1, row=0)


# control screen welcome label creation and grid placement
controlLabel = tk.Label(root, text="Left Click: Draw\nRight Click: Erase\nC: Clear\nSpacebar: Run Program")
controlLabel.grid(column=1, row=1)

# method used to destroy instruction window upon button press
# @param none
# @return none
def okButtonClicked():

    # destroy window
    root.destroy()


# ok button creation and grid placement
okButton = tk.Button(root, text="Okay", command=okButtonClicked)
okButton.grid(column=1, row=3, pady=5)

# Node class used to create, store, and manipulate the nodes used in the algorithm
class Node:

    # python constructor with variables row, col, width, and total_rows
    def __init__(self, row, col, width, total_rows):

        # set row and col
        self.row = row
        self.col = col

        # set width and total_rows
        self.width = width
        self.total_rows = total_rows

        # multiply row and col by the width to get the position on the grid
        self.x = row * width
        self.y = col * width

        # set default color to white
        self.color = WHITE

        # blank list used to store neighbors
        self.neighbors = []

    # method used to get position of node
    # @param none
    # @return row, col
    def get_pos(self):
        return self.row, self.col

    # method used to mark a node as closed
    # @param none
    # @return color as black
    def is_closed(self):
        return self.color == BLACK

    # method used to mark a node as open
    # @param none
    # @return color as purple
    def is_open(self):
        return self.color == PURPLE
    

    # method used to mark a node as a barrier
    # @param none
    # @return color as red
    def is_barrier(self):
        return self.color == RED

    # method used to mark a node as the starting point
    # @param none
    # @return color as blue
    def is_start(self):
        return self.color == BLUE

    # method used to mark a node as the end point
    # @param none
    # @return color as pink
    def is_end(self):
        return self.color == PINK

    # method used to reset a node to default
    # @param none
    # @return none
    def reset(self):
        self.color = WHITE

    # method used to make a node the starting the node
    # @param none
    # @return none
    def make_start(self):
        self.color = BLUE

    # method used to make a node closed
    # @param none
    # @return none
    def close(self):
        self.color = BLACK

    # method used to make a node open
    # @param none
    # @return none
    def open(self):
        self.color = PURPLE

    # method used to make a node a barrier
    # @param none
    # @return none
    def make_barrier(self):
        self.color = RED

    # method used to make a node the ending point
    # @param none
    # @return none
    def make_end(self):
        self.color = PINK

    # method used to make a node into part of the path
    # @param none
    # @return none
    def make_path(self):
        self.color = GREEN

    # method used to draw a node on the grid
    # @param win
    # @return none
    def draw(self, win):
        
        # draw a rectangle on the window, set the color and coordinates
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))


    # method used to update a nodes neighbors
    # @param grid: List
    # @return none
    def update_neighbors(self, grid):

        # create an empty list named neighbors
        self.neighbors = []

        # if current row is less than total rows - 1 and isnt a barrier
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN

            # add the downwards neighbors coordinate to neighbors list
            self.neighbors.append(grid[self.row + 1][self.col])

        # if current row is greater than 0 and not a barrier
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP

            # add the upwards neighbors coordinate to neighbors list
            self.neighbors.append(grid[self.row - 1][self.col])

        # if current column is less than towal rows - 1 and isnt a barrier
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT

            # add the right neighbors coordinate to the neighbors list
            self.neighbors.append(grid[self.row][self.col + 1])

        # if current column is greater than 0 and not a barrier
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT

            # add the left neighbors coordinate to neighbors list
            self.neighbors.append(grid[self.row][self.col - 1])

# method used to get the distance between the selected nodes
# @param p1: Node, p2: Node
# @return abs: abs
def get_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

# method used to operate the main a* algorithm
# @param draw: Func, grid: List, end: Node
# @return Boolean
def run_algorithm(draw, grid, start, end):

    # priority queue names open set
    # these are the nodes that we are considering 
    # for the shortest path
    open_set = PriorityQueue()

    # count used to break ties in open_set
    count = 0

    # create empty set to store where we came from
    came_from = {}

    # put new entry into open_set with initial f score, current count, and starting node 
    open_set.put((0, count, start))

    # list comprehension used to set the initial g score of "inf" for each node
    g_score = {spot: float("inf") for row in grid for spot in row}

    # set the first nodes g score to 0
    g_score[start] = 0

    # list comprehension used to the initial f score of "inf" for each node
    f_score = {spot: float("inf") for row in grid for spot in row}

    # set the starting nodes f score equal to the distance between it and the end node
    f_score[start] = get_distance(start.get_pos(), end.get_pos())

    # create an open set hash with starting node within it
    # this is used to check what is inside the priority queue since
    # we cannot see the data inside normally, just the position
    open_set_view_data = {start}

    # while open set isnt empty
    while not open_set.empty():

        # allow the user to exit out of the program mid algorithm
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # get the current node within open set
        current = open_set.get()[2]

        # remove the current node from open set hash
        open_set_view_data.remove(current)

        # if looking at the end point
        if current == end:

            # construct the path using came_from, end, and draw function
            construct_path(came_from, end, draw)

            # override the end nodes color
            # without this, the end node would end up with the paths color
            # this is simply for clarity
            end.make_end()

            # return that we have reached the end point and stop the algorithm
            return True

        # loop used to check the current nodes neighbors
        for neighbor in current.neighbors:

            # set a temporary g_score of 1 for current node since we
            # are always 1 node away
            temp_g_score = g_score[current] + 1

            # if temp g score is less than the neighbors g score
            if temp_g_score < g_score[neighbor]:

                # set the node we came from to be the current node
                came_from[neighbor] = current

                # set the neighbors g score to the temp g score
                g_score[neighbor] = temp_g_score

                # set the neighbors f score equal to the temporary g score plus the distance
                # between the current and end ndoes
                f_score[neighbor] = temp_g_score + get_distance(neighbor.get_pos(), end.get_pos())

                # if neighbor isnt in open set hash
                if neighbor not in open_set_view_data:

                    # uptick the current count
                    count += 1

                    # put the f score, count, and neighbor into the open set
                    open_set.put((f_score[neighbor], count, neighbor))

                    # add the neighbor into the open set hash
                    open_set_view_data.add(neighbor)

                    # make the neighbor an open node
                    neighbor.open()

        # draw the current node
        draw()

        # if current node isnt the starting node
        if current != start:

            # make it closed
            # this simply denotes which nodes we have checked already
            current.close()

    # return False as long as we havent seen the end point
    return False

# method used to get the current mouse position
# @param pos, rows, width
# @return row, col
def get_clicked_pos(pos, rows, width):

    # set the size of each square
    gap = width // rows

    # x and y coordinated are equal to mouse position
    y, x = pos

    # current row is equal to y value divided by gap
    row = y // gap

    # current col is equal to x value divided by gap
    col = x // gap

    # return row and col
    return row, col

# method used to store our notes in a 3 dimensional list
# @param rows, width
# @return grid: List
def create_grid(rows, width):

    # create an empty list named grid
    grid = []

    # create the size of each grid "square"
    gap = width // rows

    # loop for amount of rows
    for i in range(rows):

        # append a new 'column' to our list
        grid.append([])

        # loop for amount of rows
        for j in range(rows):

            # create a new node with current coordinates
            node = Node(i, j, gap, rows)

            # append the node into correct spot in the grid
            grid[i].append(node)

    # return grid
    return grid


# method used to draw the grid lines
# @param win, rows, width
# @return none
def draw_grid(win, rows, width):

    # set the size of each grid "square"
    gap = width // rows

    # loop for amount of rows
    for i in range(rows):

        # draw a grey line using width and gap parameters as our rows
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))

        # loop for amount of rows
        for j in range(rows):

            # draw a grey line using width and gap parameters as our columns
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

# method used display our grid
# @param win, grid: List, rows, width
# @return none
def draw(win, grid, rows, width):

    # fill the window with color white
    win.fill(WHITE)

    # loop for each row in our grid
    for row in grid:

        # loop for each spot in our row
        for spot in row:

            # draw each spot on the grid
            spot.draw(win)

    # draw our grid lines
    draw_grid(win, rows, width)

    # update the pygame display window
    pygame.display.update()

# method used to construct the path
# @param came_from: set, current: Node, draw: Func
# @return none
def construct_path(came_from, current, draw):

    # while current node is in the came_from dictionary
    while current in came_from:

        # update current to which node we came from
        current = came_from[current]

        # turn the current node into a path
        current.make_path()

        # draw the node
        draw()


# main method used to run the main logic of the program
# @param win, width
# @return none
def main(win, width):

    # set the constant amount of rows to 50
    ROWS = 50

    # call make_grid in order to initialize our grid using rows and width
    grid = create_grid(ROWS, width)

    # initialize start and end to None
    start = None
    end = None

    # set run to true, used to control main while loop
    run = True

    # while running
    while run:

        # draw the grid
        draw(win, grid, ROWS, width)

        # display instruction screen
        root.mainloop()

        # if user clicks the close button then close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # if left mouse is clicked
            if pygame.mouse.get_pressed()[0]:

                # get the position of the mouse
                pos = pygame.mouse.get_pos()

                # set the coordinates of the selected square
                row, col = get_clicked_pos(pos, ROWS, width)

                # create a new 'spot' in our grid using its coordinates
                spot = grid[row][col]

                # if a starting point hasnt been placed and isnt an end point
                if not start and spot != end:

                    # create and set starting point
                    start = spot
                    start.make_start()

                # elif the there isnt an end point and the start point has been created
                elif not end and spot != start:

                    # create and set out end point
                    end = spot
                    end.make_end()

                # elif end and starting points have been created already
                elif spot != end and spot != start:

                    # make the current spot a barrier
                    spot.make_barrier()

            # if right mouse is clicked
            elif pygame.mouse.get_pressed()[2]:

                # get the mouses current position
                pos = pygame.mouse.get_pos()

                # save the coordinates of the mouse
                row, col = get_clicked_pos(pos, ROWS, width)

                # save the current spot in grid
                spot = grid[row][col]

                # reset the spot
                spot.reset()

                # if selected spot was the starting point
                if spot == start:

                    # erase the starting point
                    start = None

                # elif selected spot was the ending point
                elif spot == end:

                    # erase the ending point
                    end = None

            # if use presses a key
            if event.type == pygame.KEYDOWN:

                # check if the key was the space bar and if there is a start and end point
                if event.key == pygame.K_SPACE and start and end:

                    # loop for amount of rows in grid
                    for row in grid:

                        # loop for amount of spots in row
                        for spot in row:

                            # update the current spots neighbors
                            spot.update_neighbors(grid)

                    # run the algorithm using a lamba draw function, grid, start, and end
                    run_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                # if user presses the "c" key
                if event.key == pygame.K_c:

                    # erase the starting point
                    start = None

                    # erase the end point
                    end = None

                    # reinitialize the grid with default parameters
                    grid = create_grid(ROWS, width)
    
    # quit the display once the loop is broken
    pygame.quit()


# call main method
main(WIN, WIDTH)