# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A collection of Python demo scripts showcasing Pygame and matplotlib capabilities.

## Running the Scripts

**Space Invaders game:**
```bash
python space_invaders.py
```
Requires pygame. Uses image files in root directory (zohran_mamdani.jpg, andrew_cuomo.jpg, donald_trump.jpg, jd_vance.jpg) - falls back to colored shapes if images not found.

**Fibonacci plot:**
```bash
python fibonacci_plot.py
```
Requires matplotlib and numpy. Generates fibonacci_plot.png.

## Dependencies

- pygame (for space_invaders.py)
- matplotlib, numpy (for fibonacci_plot.py)

## Code Structure

- `space_invaders.py` - Pygame-based arcade shooter with sprite classes (Player, Enemy, Bullet, EnemyBullet) and main Game class handling the game loop
- `fibonacci_plot.py` - Generates and plots a Fibonacci-like sequence starting from 2
