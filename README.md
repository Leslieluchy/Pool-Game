# Pool Game

A classic pool game built with Python, Pygame, and Pymunk for simulating realistic physics. Aim to pot all the balls while managing your lives!

## Table of Contents

- [Installation](#installation)
- [Game Instructions](#game-instructions)
- [Controls](#controls)
- [Rules](#rules)
- [Code Overview](#code-overview)
- [Requirements](#requirements)
- [Credits](#credits)

## Installation

### Prerequisites

Ensure Python is installed on your system. You can download it from [Python's official website](https://www.python.org/downloads/).

### Required Libraries

Install the necessary Python libraries by running:

```bash
pip install -r requirements.txt


```
##Game Instructions
Position the Cue: Move your mouse to aim the cue at the cue ball.
Set the Force: Press and hold the left mouse button to power up your shot.
Take the Shot: Release the mouse button to hit the cue ball.
Pot the Balls: Aim for the pockets to pot balls and score points.
Avoid Losing Lives: Potting the cue ball reduces your lives by one.
Winning and Losing Conditions
Win: All balls are potted.
Game Over: Lives drop to zero after potting the cue ball multiple times.
##Controls
Aim: Move the mouse to adjust the cue's angle.
Power Up: Hold down the left mouse button to increase shot power.
Shoot: Release the left mouse button to take the shot.
Rules
Lives: You have three lives. Potting the cue ball reduces your lives by one.
Win Condition: You win by potting all balls except the cue ball.
Lose Condition: The game ends if you lose all three lives.
##Code Overview
#Libraries Used
pygame for graphics rendering.
pymunk for physics simulation.
math for trigonometric calculations.
Key Variables
SCREEN_WIDTH and SCREEN_HEIGHT: Screen dimensions.
lives: Player's remaining lives.
dia and pocket_dia: Ball and pocket diameters.
max_force: Maximum force applied to the cue ball.
