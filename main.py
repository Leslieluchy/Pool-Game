# Countdown before starting the game
    countdown_timer(stdscr)

    # Game loop
    start_time = time.time()
    speed_increase_interval = 1  # seconds
    initial_sleep_time = 0.05
    sleep_time = initial_sleep_time

    while True:
        stdscr.clear()

        # Draw sphere
        draw_sphere(stdscr, x, y, radius)

        # Draw paddles
        draw_paddle(stdscr, paddle1_x, paddle1_y, paddle_width, 2)
        if num_players == 2:
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

        # Player 2 (top) paddle bounce or top wall in 1-player mode
        if num_players == 1:
            if y - radius <= 0:
                direction_y *= -1
        elif num_players == 2:
            if (y - radius <= paddle2_y and paddle2_x <= x <= paddle2_x + paddle_width):
                direction_y *= -1
                score_p2 += 1
