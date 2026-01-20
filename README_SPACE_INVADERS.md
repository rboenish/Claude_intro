# Space Invaders Game

A classic Space Invaders-style arcade shooter game built with Python and Pygame.

## Features

- Player-controlled ship with smooth left/right movement
- Grid formation of enemy invaders (5 rows x 10 columns)
- Player shooting mechanics with cooldown
- Enemy movement (side-to-side with downward progression)
- Random enemy shooting
- Collision detection
- Score tracking
- Game over and win conditions
- Restart functionality

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## How to Play

Run the game:

```bash
python space_invaders.py
```

### Controls

- **LEFT/RIGHT Arrow Keys** - Move your ship
- **SPACE** - Shoot bullets
- **R** - Restart game (when game over or won)
- **ESC** - Quit game

### Objective

- Destroy all enemy invaders to win
- Avoid getting hit by enemy bullets
- Don't let enemies reach your position
- Each destroyed enemy scores 10 points

## Game Mechanics

- The player ship moves horizontally at the bottom of the screen
- Enemies move in formation, shifting down when they reach screen edges
- Enemies randomly fire bullets downward
- The game ends if an enemy bullet hits the player or enemies reach the player's level
- Victory is achieved by destroying all enemies

Enjoy the game!
