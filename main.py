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
