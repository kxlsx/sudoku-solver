"""
Module containing grid classes
"""

import pygame
from copy import deepcopy


class Cell:
    """
    A rectangular, stationary cell, part of a Grid
    """

    def __init__(self, position: list, gridPosition: list, size: list,
                 color: list, borderColor: list=None, borderWidth: int=1):
        self.position = list(position)
        self.gridPosition = list(gridPosition)

        self.size = list(size)

        self.color = list(color)
        if not(borderColor) or not(isinstance(borderWidth, int)):
            self.borderColor = borderColor
            self.borderWidth = None
        else:
            self.borderColor = list(borderColor)
            self.borderWidth = borderWidth

    def __str__(self):
        return (('Cell' + str(self.gridPosition)) + ', ' +
                ('Pos: ' + str(self.position)) + ', ' +
                ('Color: ' + str(self.color)) + ', ' +
                ('Border Color: ' + str(self.borderColor)))


    @staticmethod
    def get_neighbors(grid, cell: list) -> list:
        """
        Returns a list of every neighboring cell
        """

        y = cell.gridPosition[0]
        x = cell.gridPosition[1]

        relYs = (-1, 0, 1)
        relXs = (-1, 0, 1)

        neighbors = []
        for relY in relYs:
            for relX in relXs:
                try:
                    nY = y + relY
                    nX = x + relX

                    if nY < 0 or nX < 0:
                        raise IndexError

                    neighbor = grid[nY][nX]
                except IndexError:
                    continue
                else:
                    neighbors.append(neighbor)
        for neighbor in neighbors:
            if neighbor.gridPosition == cell.gridPosition:
                neighbors.remove(neighbor)

        return neighbors


    def draw_self(self, display):
        cellRect = pygame.Rect(self.position, self.size)

        if isinstance(self.borderWidth, int) and self.borderColor:
            pygame.draw.rect(display, self.color, cellRect)
            pygame.draw.rect(display, self.borderColor, cellRect, self.borderWidth)
        else:
            pygame.draw.rect(display, self.color, cellRect)


class Grid:
    """
    An object storing a rectangular grid of the given size, containing
    n sized Cells and it's own coordinate system
    """

    def __init__(self, position: list, size: list, cellSize: list,
                 cellColor: list, cellBorderColor: list=None, cellBorderWidth: int=1):
        self.grid = Grid.create_grid(position, size, cellSize,
                                     cellColor, cellBorderColor, cellBorderWidth)
        self.gridBackup = deepcopy(self.grid)

        self.position = list(position)

        self.size = list(size)
        self.cellSize = list(cellSize)

        self.cellColor = list(cellColor)
        if not(cellBorderColor) or not(isinstance(cellBorderWidth, int)):
            self.cellBorderColor = cellBorderColor
            self.cellBorderWidth = None
        else:
            self.cellBorderColor = list(cellBorderColor)
            self.cellBorderWidth = cellBorderWidth

    def __getitem__(self, key):
        return self.grid[key]

    def __setitem__(self, key, value):
        self.grid[key] = value

    def __iter__(self):
        yield from self.grid

    def __len__(self):
        return len(self.grid)

    def __str__(self):
        string = ''

        for row in self:

            for cell in row:
                string += str(cell) + '\n'

        return string


    @staticmethod
    def create_grid(position: list, size: list, cellSize: list,
                    cellColor: list, cellBorderColor: list=None, cellBorderWidth: int=1) -> list:
        """
        Creates a list of lists (rows) with cells.
        Represents the Grid and its coordinate system
        """

        grid = []

        gRow = 0
        absY = position[1]
        for i in range(size[0] // cellSize[0]):
            grid.append([])

            gCell = 0
            absX = position[0]
            for j in range(size[1] // cellSize[1]):
                grid[i].append(Cell((absX, absY),
                                    (gRow, gCell),
                                    cellSize,
                                    cellColor,
                                    cellBorderColor,
                                    cellBorderWidth))

                gCell += 1
                absX += cellSize[0]

            gRow += 1
            absY += cellSize[1]

        return grid

    @staticmethod
    def get_rotated_coords(pivotCoords: list, coords: list) -> list:
        # 90 degrees
        matrix = ((0, -1),
                  (1, 0))

        relCoords = (coords[0] - pivotCoords[0],
                     coords[1] - pivotCoords[1])

        transformedCoords = (matrix[0][0] * relCoords[0] + matrix[0][1] * relCoords[1],
                             matrix[1][0] * relCoords[0] + matrix[1][1] * relCoords[1])

        rotatedCoords = [transformedCoords[0] + pivotCoords[0],
                         transformedCoords[1] + pivotCoords[1]]
        return rotatedCoords


    def draw_grid(self, display):
        for row in self:
            for cell in row:
                cell.draw_self(display)

    def change_color(self, color: list):
        for row in self:
            for cell in row:
                cell.color = color

    def reset_grid(self):
        self.grid = deepcopy(self.gridBackup)

    def reset_cell(self, gridPosition: list):
        self[gridPosition[0]][gridPosition[1]] = self.gridBackup[gridPosition[0]][gridPosition[1]]
