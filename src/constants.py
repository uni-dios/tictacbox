"""
LogiQube - Constants and Configuration
"""

# Board dimensions
BOARD_SIZE = 4  # 4x4x4 cube

# Player representations
EMPTY = 0
PLAYER_X = 1
PLAYER_O = 2

# Game states
STATE_PLAYING = "playing"
STATE_WIN = "win"
STATE_DRAW = "draw"

# UI Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
PLANE_SIZE = 160  # Size of each cell in pixels
PLANE_MARGIN = 20  # Margin between planes
CELL_SIZE = 40  # Size of each cell
GRID_PADDING = 10  # Padding around each plane grid

# Colors (RGB)
COLOR_BG = (20, 20, 30)
COLOR_GRID = (100, 100, 120)
COLOR_PLANE_BG = (40, 40, 50)
COLOR_HOVER = (80, 80, 100)
COLOR_X = (255, 100, 100)  # Red
COLOR_O = (100, 150, 255)  # Blue
COLOR_WIN_LINE = (255, 215, 0)  # Gold
COLOR_TEXT = (255, 255, 255)
COLOR_BUTTON = (70, 70, 90)
COLOR_BUTTON_HOVER = (90, 90, 110)

# Game modes
MODE_HUMAN_VS_HUMAN = "human_vs_human"
MODE_HUMAN_VS_AI = "human_vs_ai"

# AI difficulty levels
AI_EASY = "easy"
AI_MEDIUM = "medium"
AI_HARD = "hard"
