"""
Module containing the main loop of the game and additional methods
"""

import pygame
from sudoku.sudokuboard import SudokuBoard
from sudokugrid import SudokuGrid, SudokuCell
from options import colors, cellSize, framerate, textSize, difficulty


def game_screen(display):
    resolution = display.get_size()

    # time stuff
    clock = pygame.time.Clock()


    # game objects
    board = None
    sudokuGrid = SudokuGrid([0, 0], resolution, cellSize, textSize,
                            colors['cell'], colors['text'], board,
                            colors['cellBorder'])


    # main loop
    run = True
    solveStepByStep = False
    while run:
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if isinstance(board, SudokuBoard):
                    if not solveStepByStep:
                        # solve step by step
                        if event.key == pygame.K_SPACE:
                            solveGen = board.gen_solving_step_by_step()
                            solveStepByStep = True

                    # reset board
                    if event.key == pygame.K_ESCAPE:
                        board.reset_board()
                        sudokuGrid.change_board(board)
                        sudokuGrid.change_color(newTextColor=colors['text'])

                        solveStepByStep = False

                # random board
                if event.key == pygame.K_r:
                    board = SudokuBoard('r', difficulty, '', True)
                    sudokuGrid.change_board(board)
                    sudokuGrid.change_color(newTextColor=colors['text'])

                    solveStepByStep = False

            mousePos = pygame.mouse.get_pos()
            # highlight
            for row in sudokuGrid:
                for cell in row:
                    if is_mouse_on_cell(cell, mousePos):
                        cell.color = colors['cellHover']
                    else:
                        cell.color = colors['cell']

        # do stuff
        if solveStepByStep:
            try:
                moveResult = next(solveGen)
            except StopIteration:
                solveStepByStep = False
            else:
                changedCell = sudokuGrid[moveResult.changed_coords[0]][moveResult.changed_coords[1]]
                isValid = moveResult.isValid

                if isValid:
                    changedCell.change_text(changedCell.text, colors['validTextColor'])
                else:
                    changedCell.change_text(changedCell.text, colors['invalidTextColor'])

                sudokuGrid.change_board(moveResult.board)


        # draw stuff
        sudokuGrid.draw_grid(display, colors['squares'])
        pygame.display.update()


        clock.tick(framerate)


def is_mouse_on_cell(cell: SudokuCell, mousePos: list) -> bool:
    if((mousePos[0] > cell.position[0] and mousePos[0] <= cell.position[0] + cell.size[0]) and
       (mousePos[1] > cell.position[1] and mousePos[1] <= cell.position[1] + cell.size[1])):
        return True
    else:
        return False
