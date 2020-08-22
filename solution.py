from app_class import *

board = [[0, 0, 0, 0, 0, 6, 0, 0, 9], [0, 5, 0, 2, 0, 0, 5, 4, 0], [0, 7, 0, 5, 8, 4, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 8], [1, 7, 0, 0, 0, 0, 0, 0, 0], [0, 6, 0, 0, 0, 0, 4, 2, 0], [7, 0, 6, 0, 0, 0, 6, 0, 1], [9, 8, 0, 0, 5, 1, 5, 0, 0], [0, 0, 0, 6, 0, 2, 0, 4, 0]]

def checkRow(i, num, board):
    for j in range(9):
        if board[i][j] == num:
            return False
    return True

def checkCol(j, num, board):
    for i in range(9):
        if board[i][j] == num:
            return False
    return True

def checkSmallBox(i, j, num, board):
    x = 3 * i
    y = 3 * j
    for row in range(3):
        for col in range(3):
            if board[x + row][y + col] == num:
                return False
    return True

def checkIfSafe(i, j, num, board):
    return (checkRow(i, num, board) and checkCol(j, num, board) and checkSmallBox(i // 3, j // 3, num, board))

def solveSudoku(i, j, board, window):
    if j == 9:
        i = i + 1
        j = 0
    if i == 9:
        return True
    if board[i][j] != 0:
        if solveSudoku(i, j + 1, board, window):
            return True
        return False
    else:
        for num in range(9):
            if checkIfSafe(i, j, num + 1, board):
                board[i][j] = num + 1
                if solveSudoku(i, j + 1, board, window):
                    return True
                board[i][j] = 0
        return False
