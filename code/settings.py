import pygame
from os.path import join 
from os import walk

from support import load_stats

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720 

COLORS = {
    'black': (0, 0, 0),
    'red': (238, 26, 15),
    'gray': (128, 128, 128),
    'white': (255, 255, 255),
    'green': (0, 200, 0),
}

CONFIG = load_stats("data/stats.json")
FIGHTER_CONFIG = CONFIG["fighters"]