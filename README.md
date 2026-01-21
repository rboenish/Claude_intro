# Space Invaders - Political Edition

A classic arcade-style Space Invaders game with a political twist, featuring Zohran Mamdani defending against political opponents.

## Play Online

[Play the game here](https://yourusername.github.io/Claude_intro/) *(update with your GitHub username)*

## Controls

- **Left/Right Arrow Keys** - Move player
- **Space** - Shoot (triple shot!)
- **R** - Restart (when game over)
- **ESC** - Quit (desktop version only)

## Features

- Triple shot mechanic
- Political figure sprites (player and enemies)
- Hammer and sickle background
- Resizable window (desktop version)
- Web and desktop versions available

## Running Locally

### Web Version
Simply open `index.html` in a web browser.

### Desktop Version (Python)
Requires Python 3 and pygame-ce:

```bash
pip install pygame-ce
python space_invaders.py
```

## Project Structure

```
├── index.html           # Web version of the game
├── space_invaders.py    # Desktop version (Python/Pygame)
├── images/              # Game sprites
│   ├── zohran_mamdani.jpg.webp
│   ├── andrew_cuomo.jpg
│   ├── donald_trump.jpg
│   └── jd_vance.jpg
└── README.md
```

## Hosting on GitHub Pages

1. Push this repository to GitHub
2. Go to Settings > Pages
3. Select "Deploy from a branch"
4. Choose `main` branch and `/ (root)` folder
5. Save and wait for deployment

Your game will be available at `https://yourusername.github.io/repository-name/`
