import pygame
from sudoku.sudokuboard import SudokuBoard
from sudoku.sudokuexceptions import ArgumentError
from grid import Grid, Cell


class SudokuGrid(Grid):
    def __init__(self, position: list, size: list,
                 cellSize: list, textSize: int,
                 cellColor: list, textColor: list,
                 board: SudokuBoard=None,
                 cellBorderColor: list=None, cellBorderWidth: int=1,
                 font=pygame.font.get_default_font(),
                 maxTextLength: int=1,
                 cellAlign: str='centered'):
        super().__init__(position, size, cellSize,
                         cellColor, cellBorderColor, cellBorderWidth)
        if len(self) % 3 != 0 or len(self[0]) % 3 != 0:
            raise Exception('Grid length not a multiple of 3')

        if not board:
            board = tuple([[''
                            for _ in range(9)]
                           for _ in range(9)])
        self.board = board

        self.grid = SudokuGrid.create_grid(position, size,
                                           cellSize, textSize,
                                           cellColor, textColor, self.board,
                                           cellBorderColor=cellBorderColor,
                                           cellBorderWidth=cellBorderWidth,
                                           font=font,
                                           maxTextLength=maxTextLength)

        self.font = pygame.font.Font(font, textSize)
        self.textSize = textSize
        self.textColor = textColor

        if not board:
            board = tuple([[] for _ in range(9)])
        self.board = board


    @staticmethod
    def create_grid(position: list, size: list,
                    cellSize: list, textSize: int,
                    cellColor: list, textColor: list,
                    board: SudokuBoard,
                    font=pygame.font.get_default_font(),
                    maxTextLength: int=1,
                    cellBorderColor: list=None, cellBorderWidth: int=1) -> list:
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
                grid[i].append(SudokuCell((absX, absY),
                                          (gRow, gCell),
                                          cellSize,
                                          textSize,
                                          cellColor,
                                          textColor,
                                          borderColor=cellBorderColor,
                                          borderWidth=cellBorderWidth,
                                          font=font,
                                          text=board[gRow][gCell], maxTextLength=maxTextLength))

                gCell += 1
                absX += cellSize[0]

            gRow += 1
            absY += cellSize[1]

        return grid


    def draw_grid(self, display, squaresColor: list):
        super().draw_grid(display)
        self.draw_squares(display, squaresColor)

    def draw_squares(self, display, outlineColor: list):
        boardLen = len(self.board)

        squareSize = int(boardLen / 3)
        squareMaxYs = tuple(filter(lambda x: x % 3 == 0, range(boardLen)))
        squareMaxXs = tuple(filter(lambda x: x % squareSize == 0, range(boardLen)))

        for maxY in squareMaxYs:
            for maxX in squareMaxXs:
                pos = (self[maxY][maxX].position[0], self[maxY][maxX].position[1])
                size = (self[maxY][maxX].size[0] * squareSize, self[maxY][maxX].size[1] * 3)
                rect = pygame.Rect(pos, size)

                pygame.draw.rect(display, outlineColor, rect, 1)

    def update_board(self):
        self.change_board(self.board)

    def reset_board(self):
        self.board.reset_board()
        self.update_board()

    def change_board(self, newBoard: SudokuBoard,
                     newTextColor: list=None, newAlign: str=None):
        self.board = newBoard

        rowI = 0
        for row in self:
            cellI = 0
            for cell in row:
                cell.change_text(newBoard[rowI][cellI],
                                 newTextColor, newAlign)
                cellI += 1
            rowI += 1

    def change_color(self, newColor: list=None, newTextColor: list=None, newBorderColor: list=None):
        for row in self:
            for cell in row:
                cell.change_color(newColor, newTextColor, newBorderColor)


class SudokuCell(Cell):
    def __init__(self, position: list, gridPosition: list,
                 size: list, textSize: int,
                 color: list, textColor: list,
                 borderColor: list=None, borderWidth: int=1,
                 font=pygame.font.get_default_font(), text: str='', maxTextLength: int=1,
                 align: str='centered'):
        super().__init__(position, gridPosition, size,
                         color, borderColor, borderWidth)

        self.font = pygame.font.Font(font, textSize)
        self.textSize = textSize
        if len(text) > maxTextLength:
            raise ArgumentError('Text length higher than max text length ({})'.format(maxTextLength))
        self.maxTextLength = maxTextLength

        self.change_text(text, textColor, align)


    def draw_self(self, display):
        super().draw_self(display)
        display.blit(self.renderedText, self.textRect)

    def change_text(self, newText: str, newTextColor: list=None, newAlign: str=None):
        if len(newText) > self.maxTextLength:
            raise ArgumentError('Text length higher than max text length ({})'.format(self.maxTextLength))

        self.text = newText
        if newTextColor:
            self.textColor = newTextColor
        if newAlign:
            self.align = newAlign

        self.renderedText = self.font.render(self.text, True, self.textColor)
        if self.align == 'centered':
            self.textRect = self.renderedText.get_rect(center=(self.position[0] + self.size[0] // 2,
                                                               self.position[1] + self.size[1] // 2))

    def change_color(self, newColor: list=None, newTextColor: list=None, newBorderColor: list=None):
        if newColor:
            self.color = newColor
        if newTextColor:
            self.change_text(self.text, newTextColor, self.align)
        if newBorderColor:
            self.borderColor = newBorderColor
