# Curses-Based Paddle and Sphere Game

This is a terminal-based paddle game implemented in Python using the `curses` library. The game features a moving sphere, paddle controls, and options for one or two players. Players control paddles at the top and bottom of the screen, aiming to bounce the sphere and prevent it from going past their paddles.

## Table of Contents
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Features](#features)
- [Code Structure](#code-structure)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. **Clone the Repository:**
2. **Install Dependencies:**
   This game requires Python 3 and the curses library, which is typically included with Python on Linux and macOS. For Windows, you may need a compatible version of curses,such as windows-curses.Install Dependencies: This game requires Python 3 and the curses library, which is typically included with Python on Linux and macOS. For Windows, you may need a compatible version of curses, such as windows-curses.

bash
Copy code
pip install windows-curses  # For Windows users only
Run the Game:

bash
Copy code
python main.py
How to Play
Objective: Keep the sphere in play by moving your paddle to bounce it. In two-player mode, try to score points by making the sphere go past your opponent’s paddle.
Controls:
Player 1 (Bottom Paddle):
Left Arrow: Move left
Right Arrow: Move right
Player 2 (Top Paddle, if in two-player mode):
'A': Move left
'D': Move right
Exit Game: Press 'q' during the game-over screen to quit.
