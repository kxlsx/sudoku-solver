import pygame
import json
import os


def get_options() -> list:
    optionsPath = os.path.abspath(os.path.dirname(__file__))[:-3] + r'\assets\config.json'
    iconPath = os.path.abspath(os.path.dirname(__file__))[:-3] + r'\assets\icon.ico'

    try:
        with open(optionsPath, 'r') as optionsFile:
            options = json.load(optionsFile)

        options['icon'] = pygame.image.load(iconPath)
        return options
    except FileNotFoundError:
        raise FileNotFoundError('options.json not found in the assets folder')


options = get_options()

icon = options['icon']
colors = options['colors']
resolution = options['resolution']
cellSize = options['cellSize']
textSize = options['textSize']
framerate = options['framerate']
difficulty = options['difficulty']
