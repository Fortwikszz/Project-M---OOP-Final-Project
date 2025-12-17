# Project M - OOP Final Project

A game by:

| Name                              | NRP        |
|-----------------------------------|------------|
| Tri Ismunhadi Julik Cakra Wibawa  | 5054241017 |
| Marvel Mahanara                   | 5054241047 |

A game project built with Pygame-CE and Python 3.12

## Prerequisites

- Python 3.10 or newer
- pip (Python package manager)

## Installation

1. **Clone or download this repository**
   ```bash
   git clone https://github.com/Fortwikszz/Project-M---OOP-Final-Project.git
   cd Project-M---OOP-Final-Project
   ```

2. **Install dependencies**
   
   Two options:

   **Option 1: Using pip directly**
   ```bash
   pip install pygame-ce
   ```

   **Option 2: Using requirements.txt**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**
   
   Make sure you're in the project root folder, then run:
   
   ```bash
   python -m code.main
   ```

   Or if using Python 3 specifically:
   ```bash
   python3 -m code.main
   ```

## How to Play

- **Movement**: Use Arrow Keys (↑↓←→) or WASD
- **Attack**: Left mouse click
- **Dodge**: Right mouse click
- **Pause**: Press ESC
- **Quit**: Close window or press X button

## Project Structure

```
Project-M---OOP-Final-Project/
├── assets/              # Image assets and sprites
│   ├── maps/           # Map files (.tmx)
│   ├── Monster/        # Monster sprites
│   └── Tiny Swords/    # Game assets
├── audio/              # Audio files
├── code/               # Source code
│   ├── main.py        # Entry point
│   ├── level.py       # Level management
│   ├── player.py      # Player class
│   ├── enemy.py       # Enemy class
│   ├── entity.py      # Base entity class
│   ├── tiled.py       # Tile class
│   ├── ui.py          # UI and menus
│   └── settings.py    # Game settings
├── requirements.txt   # Dependencies
└── README.md         # This file
```

## Troubleshooting

### Error: ModuleNotFoundError: No module named 'pygame'

Solution: Install pygame-ce first
```bash
pip install pygame-ce

```
**Note:** If you have previously installed the original `pygame` (not `pygame-ce`), uninstall it first to avoid conflicts:
```bash
pip uninstall pygame
pip install pygame-ce
```
```bash
### Typo: 'pyhton' is not recognized

Make sure to type `python` correctly

# Correct ✅
python -m code.main

# Wrong ❌
pyhton -m code.main

# Wrong ❌
cd Project-M---OOP-Final-Project/code
python main.py
```

### Window doesn't appear or closes immediately

- Make sure there are no errors in the terminal
- Check if the window appeared behind other windows
- Look for "Projeect M" window in the taskbar

## Credits

- Assets: Tiny Swords by Pixel Frog
- Game Engine: Pygame Community Edition (pygame-ce)
