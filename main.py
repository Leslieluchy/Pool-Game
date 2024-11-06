import curses
import math
import time

def draw_sphere(stdscr, x, y, radius):
    for angle in range(0, 360, 10):
        radians = math.radians(angle)
        sphere_x = int(radius * math.cos(radians)) + x
        sphere_y = int(radius * math.sin(radians) / 2) + y
        if 0 <= sphere_x < curses.COLS and 0 <= sphere_y < curses.LINES:
            stdscr.addch(sphere_y, sphere_x, 'o', curses.color_pair(1))

def draw_paddle(stdscr, paddle_x, paddle_y, paddle_width, color_pair):
    for i in range(paddle_width):
        if 0 <= paddle_x + i < curses.COLS:
            stdscr.addch(paddle_y, paddle_x + i, '=', curses.color_pair(color_pair))

def countdown_timer(stdscr):
    for i in range(3, 0, -1):
        stdscr.clear()
        stdscr.addstr(curses.LINES // 2, curses.COLS // 2 - 2, f"Starting in {i}...", curses.color_pair(2))
        stdscr.refresh()
        time.sleep(1)
        
def game(stdscr, num_players):
# Setup
curses.curs_set(0)
stdscr.nodelay(1)
stdscr.timeout(50)

# Colors
if curses.has_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Sphere color
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Player 1 paddle color
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  # Player 2 paddle color

# Sphere position and velocity
x, y = curses.COLS // 2, curses.LINES // 2
radius = 3
direction_x, direction_y = 1, 1

# Paddle properties
paddle_width = 10

# Player 1 (bottom) paddle position and movement
paddle1_x = curses.COLS // 2 - paddle_width // 2
paddle1_y = curses.LINES - 2
move_left_p1, move_right_p1 = False, False

# Player 2 (top) paddle position and movement
paddle2_x = curses.COLS // 2 - paddle_width // 2
paddle2_y = 1
move_left_p2, move_right_p2 = False, False

# Scores
score_p1 = 0
score_p2 = 0

game_over = False
winner = None
