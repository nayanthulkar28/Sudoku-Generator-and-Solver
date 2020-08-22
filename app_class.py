import pygame
import sys
from settings import *
from buttonClass import *
from solution import *


class App:
    def __init__(self):
        # initialize all pygame module
        pygame.init()
        # initialize the display mode in which set mode displays the window
        self.window = pygame.display.set_mode([WIDTH, HEIGHT])
        self.running = True
        self.grid = shuffleSudoku()
        self.selected = None
        self.mousePos = None
        self.state = "playing"
        self.gameOver = False
        self.finished = False
        self.cellChange = False
        self.playingButton = []
        self.menuButton = []
        self.endButton = []
        self.lockedCells =[]
        self.incorrectCells = []
        self.font = pygame.font.SysFont("arial", cellSize // 2)
        self.load()

    def run(self):
        while self.running:
            if self.state == "playing":
                self.playing_events()
                self.playing_update()
                self.playing_draw()

        # uninitialize pygame modules
        pygame.quit()
        # exits from python program
        sys.exit()

#####  PLAYING STATE FUNCTIONS  #####

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.mouseOnGrid()
                if selected:
                    self.selected = selected
                else:
                    self.selected = None
                if self.mouseOnNewGame():
                    self.grid = shuffleSudoku()
                    self.setLockedCells()
                    self.gameOver = False
                if self.mouseOnSolveForMe():
                    for i in range(9):
                        for j in range(9):
                            if [j, i] not in self.lockedCells:
                                self.grid[i][j] = 0
                    solveSudoku(0, 0, self.grid, self.window)
                    self.incorrectCells = []
                    self.gameOver = True
            if event.type == pygame.KEYDOWN:
                if self.selected != None and self.selected not in self.lockedCells:
                    if self.isInt(event.unicode):
                        self.grid[self.selected[1]][self.selected[0]] = int(event.unicode)
                        self.cellChange = True

    def playing_update(self):
        self.mousePos = pygame.mouse.get_pos()
        for button in self.playingButton:
            button.update(self.mousePos)
        if self.cellChange:
            if self.selected not in self.incorrectCells:
                self.incorrectCells.append(self.selected)
            self.checkAllCells()
            if self.allCellsDone() and len(self.incorrectCells) == 0:
                self.gameOver = True

    def playing_draw(self):
        self.window.fill(BLUE)
        for button in self.playingButton:
            button.draw(self.window)
        if self.selected:
            self.drawSelection(self.window, self.selected)
        self.shadeLockedCells(self.window, self.lockedCells)
        self.shadeIncorrectCells(self.window, self.incorrectCells)
        self.drawNumbers(self.window)
        self.drawGrid(self.window)
        if self.gameOver:
            self.drawGameOver(self.window, "GAME OVER", [150, 300])
        pygame.display.update()
        self.cellChange = False

####   BOARD CHECHING FUNCTIONS   ####

    def allCellsDone(self):
        for row in self.grid:
            for num in row:
                if num==0:
                    return False
        return True

    def checkAllCells(self):
        temp = self.incorrectCells
        for cell in temp:
            if self.checkRows(cell) and self.checkCols(cell) and self.checkSmallGrid(cell):
                self.incorrectCells.remove(cell)


    def checkRows(self, cell):
        j = cell[0]+1
        while(j <= 8):
            if self.grid[cell[1]][j] != 0 and self.grid[cell[1]][cell[0]] == self.grid[cell[1]][j]:
                return False
            j = j + 1
        j = cell[0]-1
        while(j>=0):
            if self.grid[cell[1]][j] != 0 and self.grid[cell[1]][cell[0]] == self.grid[cell[1]][j]:
                return False
            j = j - 1
        return True

    def checkCols(self, cell):
        i = cell[1] + 1
        while (i <= 8):
            if self.grid[i][cell[0]] != 0 and self.grid[cell[1]][cell[0]] == self.grid[i][cell[0]]:
                return False
            i = i + 1
        i = cell[1] - 1
        while (i >= 0):
            if self.grid[i][cell[0]] != 0 and self.grid[cell[1]][cell[0]] == self.grid[i][cell[0]]:
                return False
            i = i - 1
        return True

    def checkSmallGrid(self, cell):
        x = cell[1] // 3
        y = cell[0] // 3
        for i in range(3):
            for j in range(3):
                if [j + (3 * y), i + (3 * x)] != cell and self.grid[i + (3 * x)][j + (3 * y)] != 0:
                    if self.grid[i + (3 * x)][j + (3 * y)] == self.grid[cell[1]][cell[0]]:
                        return False
        return True


####   HELPING FUNCTIONS  ####

    def shadeIncorrectCells(self, window, incorrect):
        for cell in incorrect:
            pygame.draw.rect(window, INCORRECTCELLSCOLOUR,
                             [(cell[0] * cellSize) + grid_pos[0], (cell[1] * cellSize) + grid_pos[1],
                              cellSize, cellSize])

    def shadeLockedCells(self, window, lockedCells):
        for cell in lockedCells:
            pygame.draw.rect(window, LOCKEDCELLSCOLOUR,
                             [(cell[0] * cellSize) + grid_pos[0], (cell[1] * cellSize) + grid_pos[1],
                              cellSize, cellSize])

    def drawNumbers(self, window):
        for xidx, row in enumerate(self.grid):
            for yidx, num in enumerate(row):
                if num != 0:
                    pos = [(yidx * cellSize) + grid_pos[0], (xidx * cellSize) + grid_pos[1]]
                    self.textToScreen(window, str(num), pos)

    def drawSelection(self, window, selected):
        pygame.draw.rect(window, SELECTCOLOUR, [grid_pos[0] + selected[0] * cellSize,
                                       grid_pos[1] + selected[1] * cellSize,
                                       cellSize, cellSize])

    def drawGrid(self, window):
        pygame.draw.rect(window, WHITE, [grid_pos[0], grid_pos[1], cellSize*9, cellSize*9], 2)
        for x in range(9):
            if x % 3 != 0:
                pygame.draw.line(window, WHITE, [grid_pos[0] + (x * cellSize), grid_pos[1]],
                                 [grid_pos[0] + (x * cellSize), grid_pos[1] + cellSize*9])
                pygame.draw.line(window, WHITE, [grid_pos[0], grid_pos[1] + (x * cellSize)],
                                 [grid_pos[0] + cellSize*9, grid_pos[1] + (x * cellSize)])
            else:
                pygame.draw.line(window, WHITE, [grid_pos[0] + (x * cellSize), grid_pos[1]],
                                 [grid_pos[0] + (x * cellSize), grid_pos[1] + cellSize*9], 3)
                pygame.draw.line(window, WHITE, [grid_pos[0], grid_pos[1] + (x * cellSize)],
                                 [grid_pos[0] + cellSize*9, grid_pos[1] + (x * cellSize)], 3)

    def drawGameOver(self, window, text, pos):
        font = pygame.font.SysFont("Dyuti", 70)
        f = font.render(text, False, RED)
        fwidth = f.get_width()
        fheight = f.get_height()
        pygame.draw.rect(window, RED, [pos[0] - 30, pos[1] - 20, fwidth + 60, fheight + 40], 5)
        window.blit(f, pos)

    def mouseOnGrid(self):
        x = self.mousePos[0]
        y = self.mousePos[1]
        xmin = grid_pos[0]
        xmax = grid_pos[0] + (cellSize * 9)
        ymin = grid_pos[1]
        ymax = grid_pos[1] + (cellSize * 9)
        if ((xmin <= x and x <= xmax) and (ymin <= y and y <= ymax)):
            return [(self.mousePos[0] - grid_pos[0]) // cellSize, (self.mousePos[1] - grid_pos[1]) // cellSize]
        else:
            return False

    def mouseOnNewGame(self):
        pos = self.mousePos
        newgameBTN = self.playingButton[0]
        xmin = newgameBTN.pos[0]
        xmax = newgameBTN.pos[0] + newgameBTN.image.get_width()
        ymin = newgameBTN.pos[1]
        ymax = newgameBTN.pos[1] + newgameBTN.image.get_height()
        if (xmin <= pos[0] and pos[0] <= xmax) and (ymin <= pos[1] and pos[1] <= ymax):
            return True
        return False

    def mouseOnSolveForMe(self):
        pos = self.mousePos
        solveBTN = self.playingButton[1]
        xmin = solveBTN.pos[0]
        xmax = solveBTN.pos[0] + solveBTN.image.get_width()
        ymin = solveBTN.pos[1]
        ymax = solveBTN.pos[1] + solveBTN.image.get_height()
        if (xmin <= pos[0] and pos[0] <= xmax) and (ymin <= pos[1] and pos[1] <= ymax):
            return True
        return False

    def loadButtons(self):
        self.playingButton.append(Button(20, 40, 100, 40, "New Game"))
        self.playingButton.append(Button(480, 40, 100, 40, "Solve for me"))

    def textToScreen(self, window, text, pos):
        font = self.font.render(text, False, WHITE)
        fontWidth = font.get_width()
        fontHeight = font.get_height()
        pos[0] += (cellSize - fontWidth) // 2
        pos[1] += (cellSize - fontHeight) // 2
        window.blit(font, pos)

    def load(self):
        self.loadButtons()
        self.setLockedCells()

    def setLockedCells(self):
        # setting locked cells
        self.lockedCells = []
        for yidx, row in enumerate(self.grid):
            for xidx, num in enumerate(row):
                if num != 0:
                    self.lockedCells.append([xidx, yidx])

    def isInt(self, string):
        try:
            int(string)
            return True
        except:
            return False
