import curses
import math
import time

# drawing the sphere
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

    # Countdown before starting the game
    countdown_timer(stdscr)

    # Game timing
    start_time = time.time()
    speed_increase_interval = 1  # seconds
    initial_sleep_time = 0.05
    sleep_time = initial_sleep_time

    # Game loop
    while True:
        stdscr.clear()

        # Draw sphere
        draw_sphere(stdscr, x, y, radius)

        # Draw paddles
        draw_paddle(stdscr, paddle1_x, paddle1_y, paddle_width, 2)
        if num_players == 2:  # Draw the top paddle only if 2 players
            draw_paddle(stdscr, paddle2_x, paddle2_y, paddle_width, 3)

        # Display scores
        stdscr.addstr(0, 2, f"Player 1 Score: {score_p1}", curses.color_pair(2))
        if num_players == 2:
            stdscr.addstr(0, curses.COLS - 20, f"Player 2 Score: {score_p2}", curses.color_pair(3))

        # Move sphere
        x += direction_x
        y += direction_y

        # Bounce off walls (left and right)
        if x + radius >= curses.COLS - 1 or x - radius <= 0:
            direction_x *= -1

        # Player 1 paddle bounce
        if (y + radius >= paddle1_y and paddle1_x <= x <= paddle1_x + paddle_width):
            direction_y *= -1
            score_p1 += 1

        # Bounce off top wall in 1-player mode, or use Player 2 paddle in 2-player mode
        if num_players == 1:
            if y - radius <= 0:  # Bounce off top wall
                direction_y *= -1
        elif num_players == 2:
            if (y - radius <= paddle2_y and paddle2_x <= x <= paddle2_x + paddle_width):
                direction_y *= -1
                score_p2 += 1

        # Check if the sphere goes below player 1's paddle (game over for player 1)
        if y + radius >= curses.LINES - 1:
            if num_players == 2:
                if score_p1 > score_p2:
                    winner = "Player 1 Wins!"
                elif score_p2 > score_p1:
                    winner = "Player 2 Wins!"
                else:
                    winner = "It's a Draw!"
            else:
                winner = "Game Over!"
            game_over = True

        # Check if the sphere goes above player 2's paddle (game over for player 2)
        if num_players == 2 and y - radius <= 0:
            if score_p1 > score_p2:
                winner = "Player 1 Wins!"
            elif score_p2 > score_p1:
                winner = "Player 2 Wins!"
            else:
                winner = "It's a Draw!"
            game_over = True

        # Player 1 (bottom) paddle movement
        key = stdscr.getch()
        if key == curses.KEY_LEFT:
            move_left_p1 = True
            move_right_p1 = False
        elif key == curses.KEY_RIGHT:
            move_right_p1 = True
            move_left_p1 = False
        elif key == -1:  # No key pressed
            move_left_p1 = move_right_p1 = False

        # Player 2 (top) paddle movement
        if num_players == 2:
            if key == ord('a'):
                move_left_p2 = True
                move_right_p2 = False
            elif key == ord('d'):
                move_right_p2 = True
                move_left_p2 = False
            elif key == -1:  # No key pressed
                move_left_p2 = move_right_p2 = False

        # Update paddles based on movement flags
        if move_left_p1 and paddle1_x > 0:
            paddle1_x -= 4
        if move_right_p1 and paddle1_x + paddle_width < curses.COLS:
            paddle1_x += 4
        if num_players == 2:
            if move_left_p2 and paddle2_x > 0:
                paddle2_x -= 4
            if move_right_p2 and paddle2_x + paddle_width < curses.COLS:
                paddle2_x += 4

        # Increase speed every 1 seconds
        elapsed_time = time.time() - start_time
        if int(elapsed_time) % speed_increase_interval == 0 and elapsed_time > 0:
            sleep_time *= 0.85

        # Quit condition
        if game_over:
            stdscr.addstr(curses.LINES // 2, curses.COLS // 2 - len(winner) // 2, winner, curses.color_pair(2))
            stdscr.addstr(curses.LINES // 2 + 1, curses.COLS // 2 - 10, "Press 'q' to Quit")
            stdscr.refresh()

            # Wait for 'q' to quit
            while True:
                key = stdscr.getch()
                if key == ord('q'):
                    return

        stdscr.refresh()
        time.sleep(sleep_time)  # Use dynamic sleep time


def main(stdscr):
    # Intro screen to choose mode
    stdscr.clear()
    stdscr.addstr(curses.LINES // 2 - 1, curses.COLS // 2 - 7, "Select Mode:")
    stdscr.addstr(curses.LINES // 2, curses.COLS // 2 - 10, "1. 1-Player Mode")
    stdscr.addstr(curses.LINES // 2 + 1, curses.COLS // 2 - 10, "2. 2-Player Mode")
    stdscr.addstr(curses.LINES // 2 + 3, curses.COLS // 2 - 15, "Press 'q' to Quit")
    stdscr.refresh()

    # Wait for a valid selection
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
