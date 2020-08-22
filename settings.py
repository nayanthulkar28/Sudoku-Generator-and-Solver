#sudoku generator
import random

board = [[0 for i in range(9)] for j in range(9)]
show = 0.35

def fillSmallBox(i, j, grid):
    available_num = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for row in range(3):
        for col in range(3):
            num = random.choice(available_num)
            grid[i+row][j+col] = num
            available_num.remove(num)

def fillDiagonal(grid):
    i = 0
    while(i < 9):
        fillSmallBox(i, i, grid)
        i = i + 3

def unUsedInRow(i, num, grid):
    for j in range(9):
        if grid[i][j] == num:
            return False
    return True

def unUsedInCol(j, num, grid):
    for i in range(9):
        if grid[i][j] == num:
            return False
    return True

def unUsedInBox(i, j, num, grid):
    for row in range(3):
        for col in range(3):
            if grid[(3 * i) + row][(3 * j) + col] == num:
                return False
    return True

def checkIfSafe(i, j, num, grid):
     if unUsedInRow(i, num, grid) and unUsedInCol(j, num, grid) and unUsedInBox(i // 3, j // 3, num, grid):
         return True
     return False

def fillRemaining(i, j, grid):
    if i // 3 == j // 3:
        j = j + 3
    if j == 9:
        i = i + 1
        j = 0
    if i == 9:
        return True
    if i // 3 == j // 3:
        j = j + 3
    for num in range(9):
        if checkIfSafe(i, j, num + 1, grid):
            grid[i][j] = num + 1
            if fillRemaining(i, j + 1, grid):
                return True
            grid[i][j] = 0
    return False

def removeElements(board):
    for i in range(9):
        for j in range(9):
            num = random.random()
            if num > show:
                board[i][j] = 0

def generateBoard(board):
    fillDiagonal(board)
    fillRemaining(0, 0, board)
    removeElements(board)

def generateBoard2():
    for i in range(9):
        for j in range(9):
            num = random.random()
            if num < show:
                available_num = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                while 1:
                    n = random.choice(available_num)
                    if checkIfSafe(i, j, n, board):
                        board[i][j] = n
                        break
    return board

def shuffleSudoku():
    board = [[0 for i in range(9)] for j in range(9)]
    generateBoard(board)
    return board

#dimentions of window
WIDTH = 600
HEIGHT = 600

#colours
BLUE = [0, 106, 113]
WHITE = [225, 225, 225]
SELECTCOLOUR = [155, 222, 172]
LOCKEDCELLSCOLOUR = [60, 165, 157]
INCORRECTCELLSCOLOUR = [240, 138, 93]
RED = [129, 0, 0]

#boards
testBoard1 = [[0 for x in range(9)] for y in range(9)]
testBoard2 = shuffleSudoku()

#positions and sizes
grid_pos = [75, 100]
cellSize = 50
grid_size = cellSize * 9
