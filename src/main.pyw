"""
Main module used to run the game
"""

import pygame
from screens import game_screen
from options import resolution, icon

if __name__ == '__main__':
    pygame.init()

    display = pygame.display.set_mode(resolution)
    pygame.display.set_icon(icon)
    pygame.display.set_caption('sudoku-solver')

    game_screen(display)

    pygame.quit()
