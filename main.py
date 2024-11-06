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

        # Paddle movement
        key = stdscr.getch()
        if key == curses.KEY_LEFT:
            move_left_p1 = True
            move_right_p1 = False
        elif key == curses.KEY_RIGHT:
            move_right_p1 = True
            move_left_p1 = False
        elif key == -1:
            move_left_p1 = move_right_p1 = False

        if num_players == 2:
            if key == ord('a'):
                move_left_p2 = True
                move_right_p2 = False
            elif key == ord('d'):
                move_right_p2 = True
                move_left_p2 = False
            elif key == -1:
                move_left_p2 = move_right_p2 = False

        # Update paddle positions
        if move_left_p1 and paddle1_x > 0:
            paddle1_x -= 4
        if move_right_p1 and paddle1_x + paddle_width < curses.COLS:
            paddle1_x += 4
        if num_players == 2:
            if move_left_p2 and paddle2_x > 0:
                paddle2_x -= 4
            if move_right_p2 and paddle2_x + paddle_width < curses.COLS:
                paddle2_x += 4

        # Increase speed every 1 second
        elapsed_time = time.time() - start_time
        if int(elapsed_time) % speed_increase_interval == 0 and elapsed_time > 0:
            sleep_time *= 0.85

        # Quit if game is over
        if game_over:
            stdscr.addstr(curses.LINES // 2, curses.COLS // 2 - len(winner) // 2, winner, curses.color_pair(2))
            stdscr.addstr(curses.LINES // 2 + 1, curses.COLS // 2 - 10, "Press 'q' to Quit")
            stdscr.refresh()

            while True:
                key = stdscr.getch()
                if key == ord('q'):
                    return

        stdscr.refresh()
        time.sleep(sleep_time)