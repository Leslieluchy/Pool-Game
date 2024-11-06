import curses
import math
import time
import random
from enum import Enum

class PowerUp(Enum):
    WIDER_PADDLE = 1
    SLOWER_BALL = 2
    EXTRA_POINT = 3

def draw_sphere(stdscr, x, y, radius, char='o'):
    # Improved sphere drawing with different characters for better visibility
    chars = ['∙', '○', '●', '◎', '◉']  # Different sized ball characters
    current_char = chars[min(int(radius)-1, len(chars)-1)]
    
    for angle in range(0, 360, 10):
        radians = math.radians(angle)
        sphere_x = int(radius * math.cos(radians)) + x
        sphere_y = int(radius * math.sin(radians) / 2) + y
        if 0 <= sphere_x < curses.COLS and 0 <= sphere_y < curses.LINES:
            try:
                stdscr.addch(sphere_y, sphere_x, current_char, curses.color_pair(1) | curses.A_BOLD)
            except curses.error:
                pass

def draw_paddle(stdscr, paddle_x, paddle_y, paddle_width, color_pair, is_powered_up=False):
    paddle_char = '█' if is_powered_up else '═'
    for i in range(paddle_width):
        if 0 <= paddle_x + i < curses.COLS:
            try:
                stdscr.addch(paddle_y, paddle_x + i, paddle_char, 
                            curses.color_pair(color_pair) | curses.A_BOLD)
            except curses.error:
                pass

def draw_power_up(stdscr, x, y, type):
    symbols = {
        PowerUp.WIDER_PADDLE: 'W',
        PowerUp.SLOWER_BALL: 'S',
        PowerUp.EXTRA_POINT: 'P'
    }
    try:
        stdscr.addch(y, x, symbols[type], curses.color_pair(4) | curses.A_BOLD)
    except curses.error:
        pass

def show_tutorial(stdscr):
    stdscr.clear()
    messages = [
        "Welcome to Enhanced Pong!",
        "",
        "Controls:",
        "Player 1 (Bottom): LEFT/RIGHT Arrow Keys",
        "Player 2 (Top): A/D Keys",
        "",
        "Power-ups:",
        "W - Wider Paddle",
        "S - Slower Ball",
        "P - Extra Point",
        "",
        "Tips:",
        "- Ball speeds up over time",
        "- Collect power-ups for advantages",
        "- Hit the ball with paddle edges for angle shots",
        "",
        "Press SPACE to start..."
    ]
    
    for i, msg in enumerate(messages):
        try:
            stdscr.addstr(curses.LINES//2 - len(messages)//2 + i, 
                         curses.COLS//2 - len(msg)//2, 
                         msg, 
                         curses.color_pair(2))
        except curses.error:
            pass
    
    stdscr.refresh()
    while stdscr.getch() != ord(' '):
        pass

def countdown_timer(stdscr):
    for i in range(3, 0, -1):
        stdscr.clear()
        msg = f"Starting in {i}..."
        try:
            stdscr.addstr(curses.LINES // 2, curses.COLS // 2 - len(msg) // 2,
                         msg, curses.color_pair(2) | curses.A_BOLD)
        except curses.error:
            pass
        stdscr.refresh()
        time.sleep(1)

def apply_power_up(power_up_type, paddle, ball):
    if power_up_type == PowerUp.WIDER_PADDLE:
        paddle['width'] = min(20, paddle['width'] + 4)
    elif power_up_type == PowerUp.SLOWER_BALL:
        ball['speed'] = max(0.5, ball['speed'] * 0.7)
    elif power_up_type == PowerUp.EXTRA_POINT:
        scores[paddle] += 3
    
    paddle['powered_up'] = True
    paddle['power_up_time'] = time.time()

def remove_power_up(paddle):
    paddle['width'] = 12  # Reset to default width
    paddle['powered_up'] = False

def game(stdscr, num_players):
    # Setup
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(30)

    # Colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)

    show_tutorial(stdscr)

    # Initial game state
    ball = {
        'x': curses.COLS // 2,
        'y': curses.LINES // 2,
        'radius': 2,
        'dx': 1,
        'dy': 1,
        'speed': 0.5  # Reduced speed for slower movement
    }

    paddle_width = 12
    paddle_speed = 2

    paddles = {
        'p1': {
            'x': curses.COLS // 2 - paddle_width // 2,
            'y': curses.LINES - 2,
            'width': paddle_width,
            'powered_up': False,
            'power_up_time': 0
        },
        'p2': {
            'x': curses.COLS // 2 - paddle_width // 2,
            'y': 1,
            'width': paddle_width,
            'powered_up': False,
            'power_up_time': 0
        }
    }

    power_ups = []
    power_up_spawn_time = time.time()
    power_up_duration = 10
    scores = {'p1': 0, 'p2': 0}
    game_over = False
    winner = None

    countdown_timer(stdscr)

    start_time = time.time()
    last_power_up_time = start_time

    while True:
        stdscr.clear()
        current_time = time.time()

        # Spawn power-ups periodically
        if current_time - last_power_up_time > 5:  # Every 5 seconds
            if random.random() < 0.3:  # 30% chance to spawn
                power_ups.append({
                    'x': random.randint(5, curses.COLS-5),
                    'y': random.randint(5, curses.LINES-5),
                    'type': random.choice(list(PowerUp))
                })
            last_power_up_time = current_time

        # Draw and update power-ups
        for power_up in power_ups[:]:
            draw_power_up(stdscr, power_up['x'], power_up['y'], power_up['type'])

            # Check collision with ball
            if (abs(power_up['x'] - ball['x']) < 2 and
                abs(power_up['y'] - ball['y']) < 2):
                if ball['dy'] > 0:  # Ball going down, give to player 1
                    apply_power_up(power_up['type'], paddles['p1'], ball)
                else:  # Ball going up, give to player 2
                    apply_power_up(power_up['type'], paddles['p2'], ball)
                power_ups.remove(power_up)

        # Draw game elements
        draw_sphere(stdscr, int(ball['x']), int(ball['y']), ball['radius'])
        draw_paddle(stdscr, paddles['p1']['x'], paddles['p1']['y'],
                    paddles['p1']['width'], 2, paddles['p1']['powered_up'])
        if num_players == 2:
            draw_paddle(stdscr, paddles['p2']['x'], paddles['p2']['y'],
                        paddles['p2']['width'], 3, paddles['p2']['powered_up'])

        # Display scores
        try:
            stdscr.addstr(0, 2, f"P1: {scores['p1']}", curses.color_pair(2) | curses.A_BOLD)
            if num_players == 2:
                stdscr.addstr(0, curses.COLS - 10, f"P2: {scores['p2']}",
                            curses.color_pair(3) | curses.A_BOLD)
        except curses.error:
            pass

        # Update ball position
        ball['x'] += ball['dx'] * ball['speed']
        ball['y'] += ball['dy'] * ball['speed']

        # Ball physics - bounce off walls
        if ball['x'] >= curses.COLS - ball['radius'] or ball['x'] <= ball['radius']:
            ball['dx'] *= -1
            ball['dx'] *= 0.995  # Less deceleration on wall hits

        # Modified top wall behavior for single-player mode
        if num_players == 1 and ball['y'] <= 0:
            ball['dy'] *= -1
            ball['speed'] *= 1.02  # Slower speed increase
            scores['p1'] += 1  # Award point for successful wall bounce

        # Paddle collision detection
        for player, paddle in paddles.items():
            if player == 'p1' and ball['dy'] > 0:  # Ball moving down
                if (ball['y'] >= paddle['y'] - 1 and
                        paddle['x'] <= ball['x'] <= paddle['x'] + paddle['width']):
                    ball['dy'] *= -1
                    relative_hit = (ball['x'] - paddle['x']) / paddle['width']
                    ball['dx'] = (relative_hit - 0.5) * 2
                    scores['p1'] += 1
                    ball['speed'] *= 1.02  # Slower speed increase

            elif player == 'p2' and num_players == 2 and ball['dy'] < 0:  # Ball moving up
                if (ball['y'] <= paddle['y'] + 1 and
                        paddle['x'] <= ball['x'] <= paddle['x'] + paddle['width']):
                    ball['dy'] *= -1
                    relative_hit = (ball['x'] - paddle['x']) / paddle['width']
                    ball['dx'] = (relative_hit - 0.5) * 2
                    scores['p2'] += 1
                    ball['speed'] *= 1.02  # Slower speed increase

        # Modified game over conditions
        if (num_players == 2 and (ball['y'] >= curses.LINES - 1 or ball['y'] <= 0)) or \
            (num_players == 1 and ball['y'] >= curses.LINES - 1):
            if num_players == 2:
                if scores['p1'] > scores['p2']:
                    winner = "Player 1 Wins!"
                elif scores['p2'] > scores['p1']:
                    winner = "Player 2 Wins!"
                else:
                    winner = "It's a Draw!"
            else:
                winner = f"Game Over! Final Score: {scores['p1']}"
            game_over = True

        # Handle input and other game logic...


        # Handle input
        key = stdscr.getch()
        
        # Player 1 controls
        if key == curses.KEY_LEFT and paddles['p1']['x'] > 0:
            paddles['p1']['x'] -= paddle_speed
        elif key == curses.KEY_RIGHT and paddles['p1']['x'] + paddles['p1']['width'] < curses.COLS:
            paddles['p1']['x'] += paddle_speed

        # Player 2 controls
        if num_players == 2:
            if key == ord('a') and paddles['p2']['x'] > 0:
                paddles['p2']['x'] -= paddle_speed
            elif key == ord('d') and paddles['p2']['x'] + paddles['p2']['width'] < curses.COLS:
                paddles['p2']['x'] += paddle_speed

        # Check power-up expiration
        for player in ['p1', 'p2']:
            if paddles[player]['powered_up']:
                if current_time - paddles[player]['power_up_time'] > power_up_duration:
                    remove_power_up(paddles[player])

        # Game over logic
        if game_over:
            try:
                stdscr.addstr(curses.LINES // 2, curses.COLS // 2 - len(winner) // 2,
                             winner, curses.color_pair(5) | curses.A_BOLD)
                stdscr.addstr(curses.LINES // 2 + 1, curses.COLS // 2 - 10,
                             "Press 'q' to Quit", curses.color_pair(2))
            except curses.error:
                pass
            stdscr.refresh()
            
            while True:
                key = stdscr.getch()
                if key == ord('q'):
                    return

        stdscr.refresh()
        time.sleep(max(0.01, 0.05 - (current_time - start_time) / 100))

def main(stdscr):
    # Intro screen
    stdscr.clear()
    title = "ENHANCED PONG"
    try:
        stdscr.addstr(curses.LINES // 2 - 2, curses.COLS // 2 - len(title) // 2,
                     title, curses.A_BOLD)
        stdscr.addstr(curses.LINES // 2, curses.COLS // 2 - 10, "1. 1-Player Mode")
        stdscr.addstr(curses.LINES // 2 + 1, curses.COLS // 2 - 10, "2. 2-Player Mode")
        stdscr.addstr(curses.LINES // 2 + 2, curses.COLS // 2 - 10, "q. Quit")
    except curses.error:
        pass
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key == ord('1'):
            game(stdscr, num_players=1)
            break
        elif key == ord('2'):
            game(stdscr, num_players=2)
            break
        elif key == ord('q'):
            break

if __name__ == "__main__":
    curses.wrapper(main)