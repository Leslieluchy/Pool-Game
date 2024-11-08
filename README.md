# Pool Game

## Description
A pool game implemented using Python and the Pygame and Pymunk libraries. The game features a pool table, balls, and a cue stick. The objective is to pot all the balls using the cue ball.

## How to Clone and Install
1. Clone the repository using the following command:
   ```sh
   git clone https://github.com/Leslieluchy/Pool-Game.git
   ```
2. Navigate to the project directory:
   ```sh
   cd pip install pygame pymunk
   ```
3. Install the required libraries using the following command:
   ```sh
   pip install -r requirements.txt
   ```

## How to Run
1. Ensure you have Python installed on your system.
2. Run the `pool.py` file using the following command:
   ```sh
   python pool.py
   ```

## Controls
- Use the mouse to aim the cue stick.
- Click and hold the left mouse button to power up the shot.
- Release the left mouse button to take the shot.
- Press 'q' to quit the game.

## Features
- Realistic physics simulation using Pymunk.
- Multiple balls and pockets on the pool table.
- Power bar to indicate the strength of the shot.
- Game over and win conditions.

## Game Variables
- `lives`: Number of lives the player has.
- `dia`: Diameter of the balls.
- `pocket_dia`: Diameter of the pockets.
- `force`: Current force applied to the cue ball.
- `max_force`: Maximum force that can be applied to the cue ball.
- `force_direction`: Direction of the force (increasing or decreasing).
- `game_running`: Boolean indicating if the game is running.
- `cue_ball_potted`: Boolean indicating if the cue ball has been potted.
- `taking_shot`: Boolean indicating if the player is taking a shot.
- `powering_up`: Boolean indicating if the player is powering up the shot.
- `potted_balls`: List of potted balls.

## Colors
- `BG`: Background color.
- `RED`: Color for the power bar.
- `WHITE`: Color for the text.

## Fonts
- `font`: Font for the text.
- `large_font`: Font for the game over and win messages.

## Images
- `cue_image`: Image of the cue stick.
- `table_image`: Image of the pool table.
- `ball_images`: List of images for the balls.

## Functions
- `draw_text(text, font, text_col, x, y)`: Function for outputting text onto the screen.
- `create_ball(radius, pos)`: Function for creating balls.
- `create_cushion(poly_dims)`: Function for creating cushions.

## Classes
- `Cue`: Class for the pool cue.

## Game Loop
- The game loop handles the game logic, drawing, and event handling.

## Event Handling
- Handles mouse button down and up events for powering up and taking shots.
- Handles the quit event to exit the game.
```