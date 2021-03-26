"""
README

Built with
    1. Python 3.8.6
    2. PyGame

Installation
    1. Recommended Python version 3.8.6
    2. PyGame does not support Python version 3.9.0 as of Oct 26, 2020
    3. Install PyGame following https://www.pygame.org/wiki/GettingStarted

How to play
    1. Download file and place it in desired directory
    2. Go to directory in terminal
    3. launch sudokuSolver.py file in terminal, keeping terminal window
        side-by-side the launched GUI for additional information.
"""

import pygame

pygame.init()

"""
SETUP __________________________________________________________________________
"""
# TICKRATE is updates/second
# set TICKRATE to maximum monitor refresh rate.
TICKRATE = 60


"""
COLORS _________________________________________________________________________
"""
# each 3x3 box in the 9x9 grid will have its own color for distinction,
# C1 through C9.
# possibilities: x <= 2, x <= 5, x <= 8, y <= 2, y <= 5, y <= 8. Any
# combination of x and y yields a specific color.
C1 = (255, 200, 200)
C2 = (200, 255, 200)
C3 = (200, 200, 255)
C4 = (255, 255, 200)
C5 = (200, 255, 255)
C6 = (255, 200, 255)
C7 = (255, 200, 150)
C8 = (150, 255, 200)
C9 = (200, 150, 255)
BACKGROUND = (0, 0, 0)
COLOR_LIST = [
    [C1, C2, C3],   # [0][0-2]
    [C4, C5, C6],   # [1][0-2]
    [C7, C8, C9]    # [2][0-2]
]


def subgrid_color_picker(y, x):
    subgrid_y = y // 3      # go from 0-8 to 0-2 (whole grid to sub grid)
    subgrid_x = x // 3      # go from 0-8 to 0-2 (whole grid to sub grid)
    return COLOR_LIST[subgrid_y][subgrid_x]


"""
FONT ___________________________________________________________________________
"""
font = pygame.font.SysFont('microsoftsansserifttf', 40)


"""
GRID ___________________________________________________________________________
"""
GRID_BLOCK_SIZE = 50        # size of length of each block in pixels
GRID_BLOCK_MARGINS = 1      # size of width of margins in pixels
GRIDS_PER_SIDE = 9          # number of blocks per side


# WORLD'S HARDEST SUDOKU GRID CLAIMED BY FINNISH MATHEMATICIAN ARTO INKALA
grid = [
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 0],
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 5, 7, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 6, 8],
    [0, 0, 8, 5, 0, 0, 0, 1, 0],
    [0, 9, 0, 0, 0, 0, 4, 0, 0]
]

"""
COMPLETE GRID FROM ABOVE:
[8, 1, 2, 7, 5, 3, 6, 4, 9],
[9, 4, 3, 6, 8, 2, 1, 7, 5],
[6, 7, 5, 4, 9, 1, 2, 8, 3],
[1, 5, 4, 2, 3, 7, 8, 9, 6],
[3, 6, 9, 8, 4, 5, 7, 2, 1],
[2, 8, 7, 1, 6, 9, 5, 3, 4],
[5, 2, 1, 9, 7, 4, 3, 6, 8],
[4, 3, 8, 5, 2, 6, 9, 1, 7],
[7, 9, 6, 3, 1, 8, 4, 5, 2]
"""


"""
PRE-LOOP _______________________________________________________________________
"""
GAME_WINDOW_SIZE = (GRID_BLOCK_SIZE + GRID_BLOCK_MARGINS) * GRIDS_PER_SIDE +\
    GRID_BLOCK_MARGINS
GAME_WINDOW = pygame.display.set_mode((GAME_WINDOW_SIZE, GAME_WINDOW_SIZE))
CLOCK = pygame.time.Clock()
GAME_WINDOW.fill(BACKGROUND)
pygame.display.set_caption("Sudoku Solver")
running = True


"""
LOGIC __________________________________________________________________________
"""

"""
FIVE POSSIBILITIES FOR THE GRID:
    1. Board not completed initially and solvable
    2. Board completed initially and numbers are right
    3. Board completed initially but numbers are wrong
    4. Reset max possible value -> 1 of first non-0 entry
        note: max possible value is the highest value that is insertable at
        this location.
    5. 0s can't be filled due to all 1-9 possibilities being taken elsewhere
        along the horizontal, vertical, and inside the respective subgrid.
"""


run = True
iterations = 0
first_non_0_y = 0
first_non_0_x = 0
noChangesCount = 0
is_maxValidNum_instance = False
stopTesting = False
time_since_finish = 0

for y in range(GRIDS_PER_SIDE):
    for x in range(GRIDS_PER_SIDE):
        if grid[y][x] < 0 or grid[y][x] > 9:
            grid[y][x] = 0


def printGrid():
    print()
    for row in range(9):
        print(grid[row])
    print()


# print the initial grid to terminal
printGrid()


# check if it's possible to insert n in g[y][x] following the rules:
# 1. no duplicates of the number n in the row
# 2. no duplicates of the number n in the column
# 3. no duplicates of the number n in the subgrid that n is in
def insertable(g, y, x, n):
    # 1 and 2
    for sweep in range(GRIDS_PER_SIDE):
        if g[y][sweep] == n:
            return False
        if g[sweep][x] == n:
            return False
    # 3
    subgrid_x = (x // 3) * 3
    subgrid_y = (y // 3) * 3
    for i in range(0, 3):
        for j in range(0, 3):
            if g[subgrid_y + i][subgrid_x + j] == n:
                return False
    # if insertable (all conditions pass), return True
    return True


# draws each grid index of board and overlays text on top of their respective
    # grids
def drawBoard():
    for y in range(GRIDS_PER_SIDE):
        for x in range(GRIDS_PER_SIDE):
            pygame.draw.rect(GAME_WINDOW, subgrid_color_picker(y, x),
                             [
                (GRID_BLOCK_SIZE + GRID_BLOCK_MARGINS) * x + GRID_BLOCK_MARGINS,
                (GRID_BLOCK_SIZE + GRID_BLOCK_MARGINS) * y + GRID_BLOCK_MARGINS,
                GRID_BLOCK_SIZE,
                GRID_BLOCK_SIZE
            ])
            if grid[y][x] != 0:
                text = font.render(str(grid[y][x]), 1, (0, 0, 0))
                GAME_WINDOW.blit(text,
                                 (
                                     # the "+ 10" and "+ 5" places the numbers in the center
                                     # of their respective grids
                                     (GRID_BLOCK_SIZE + GRID_BLOCK_MARGINS) * \
                                     x + GRID_BLOCK_MARGINS + 10,
                                     (GRID_BLOCK_SIZE + GRID_BLOCK_MARGINS) * \
                                     y + GRID_BLOCK_MARGINS + 5
                                 )
                                 )
    """
    TICK FRAMES/SEC AND FLIP (INSIDE drawBoard())_______________________________
    """
    CLOCK.tick(TICKRATE)
    pygame.display.flip()


# draw the board initially
drawBoard()


def if_Zero_0s():
    global run
    zeros = 0
    temp = 0
    for y in range(GRIDS_PER_SIDE):
        for x in range(GRIDS_PER_SIDE):
            if grid[y][x] == 0:
                zeros += 1
    if zeros == 0:
        for y in range(GRIDS_PER_SIDE):
            for x in range(GRIDS_PER_SIDE):
                temp = grid[y][x]
                grid[y][x] = 0
                if insertable(grid, y, x, temp):
                    grid[y][x] = temp
                else:
                    drawBoard()
                    print("Invalid grid given\n")
                    pygame.display.set_caption("Invalid grid given")
                    run = False
                    return True
        drawBoard()
        printGrid()
        print("Grid complete\n")
        pygame.display.set_caption("Grid complete")
        run = False
        return True
    return False


stopTesting = if_Zero_0s()


def find_first_0_coords():
    global first_non_0_y
    global first_non_0_x
    if stopTesting == False:
        for y in range(GRIDS_PER_SIDE):
            for x in range(GRIDS_PER_SIDE):
                if grid[y][x] == 0:
                    first_non_0_y = y
                    first_non_0_x = x
                    return


find_first_0_coords()

maxValidNum = 0
for n in range(1, GRIDS_PER_SIDE):
    if insertable(grid, first_non_0_y, first_non_0_x, n):
        maxValidNum = n


def solve():
    global run
    global iterations
    global first_non_0_y
    global first_non_0_x
    global is_maxValidNum_instance
    global noChangesCount
    global stopTesting
    global maxValidNum

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return

        if grid[first_non_0_y][first_non_0_x] == maxValidNum:
            is_maxValidNum_instance = True
        if grid[first_non_0_y][first_non_0_x] == 1 and is_maxValidNum_instance:
            drawBoard()
            print("Grid unsolvable\n")
            pygame.display.set_caption("Grid unsolvable")
            run = False
            return

        iterations += 1
        # Speed up the solve significantly.
        if iterations % 20 == 0:
            drawBoard()

        for y in range(GRIDS_PER_SIDE):
            for x in range(GRIDS_PER_SIDE):
                if grid[y][x] == 0:
                    for n in range(1, GRIDS_PER_SIDE + 1):

                        noChangesCount += 1
                        if noChangesCount == 10:
                            print("Grid unsolvable\n")
                            pygame.display.set_caption("Grid unsolvable")
                            run = False
                            return

                        if insertable(grid, y, x, n):
                            grid[y][x] = n
                            noChangesCount = 0
                            if_Zero_0s()
                            solve()
                            grid[y][x] = 0
                            noChangesCount = 0
                    return


"""
LOOP ___________________________________________________________________________
"""
while running:

    """
    EXIT USING 'X' BUTTON ______________________________________________________
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    solve()

    TICKRATE = 1

    print(f"%d seconds until termination" % (20 - time_since_finish))
    if time_since_finish == 20:
        running = False
    time_since_finish += 1

    """
    TICK FRAMES/SEC AND FLIP ___________________________________________________
    """
    CLOCK.tick(TICKRATE)
    pygame.display.flip()


pygame.quit()
