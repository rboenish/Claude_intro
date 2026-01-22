# Space Invaders (Vaccine)- Political Edition

A classic Space Invaders-style arcade vaccine shooter game built with Python and Pygame, featuring political figures!

**Play as Zohran Mamdani** (NYC Mayor) defending against:
- Andrew Cuomo
- Donald Trump
- JD Vance

## Features

- Player-controlled character (Zohran Mamdani) with smooth left/right movement
- Grid formation of enemy invaders (5 rows x 10 columns) with randomized political opponent faces
- Player vaccine shooting mechanics with cooldown
- Enemy movement (side-to-side with downward progression)
- Random enemy shooting
- Collision detection
- Score tracking
- Game over and win conditions
- Restart functionality
- Image support with fallback graphics

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Getting Character Images

The game works with or without character images. Without images, it uses colored geometric shapes.

### Option 1: Automatic Download (Recommended)

```bash
python download_images.py
```

This downloads political figure images from Wikimedia Commons and places them in the `images/` directory.

### Option 2: Manual Download

See `IMAGE_SOURCES.md` for links to download images manually. Place downloaded images in the `images/` directory with these filenames:
- `zohran_mamdani.jpg` (player character)
- `andrew_cuomo.jpg` (enemy)
- `donald_trump.jpg` (enemy)
- `jd_vance.jpg` (enemy)

### Option 3: Play Without Images

Just run the game! It will use fallback graphics (colored shapes) if images aren't found.

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
