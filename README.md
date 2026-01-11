# Dino LevelUp
An endless dino runner game built with **Pygame** featuring a dinosaur navigating obstacles, game powerups, and surviving as the game speed increases.
---
## Project Overview
**Dino LevelUp** is a Christmas themed take on the classic dinosaur runner and jump game. The player controls a dinosaur that must jump over cactus and duck under pterodactyls birds. To help the player achieve a high score, three unique powerups can be collected:
* **Shield**: Protects the dinosaur from one collision with an obstacle.
* **Jump Boost**: Increases the jump height significantly.
* **Double Points**: Increases the score gain from 0.1 to 0.2 per frame.
The game features persistent high score tracking via a `highscore.txt` file, dynamic obstacle spawning that scales with game speed, and an holiday christmas themed background with exciting sound effects.
---
## Instructions to Run the Code
To play the game, follow these steps:
1. **Prepare Python**: Ensure you have Python 3.x installed on your system.
2. **Organize Files**: Make sure your directory structure looks like this:
    * `main.py` (The entry point and main game loop).
    * `config.py` (Global variables, assets, and settings).
    * `sprites.py` (Class definitions for Dino, Cactus, Ptero, Cloud, Powerups).
3. **Assets Check**: Ensure the `/Assets` and `/sfx` folders are present with all images and audio files as referenced in the code.
4. **Launch**: Open your terminal/command prompt in the project folder and run:
    ```bash
    python main.py
    ```
---
## Dependencies & Installation
This project relies on the **Pygame** library for rendering and game logic.
### Installation Steps:
1. **Install Pygame**: Run the following command in your terminal:
    ```bash
    pip install pygame
    ```
2. **System Requirements**: 
    * Python 3.6 or higher.
    * Minimum screen resolution of 1280x720.
---
## Controls
* **UP Arrow / SPACE**: Jump (or Restart after Game Over).
* **DOWN Arrow**: Duck (changes Dino hitbox and sprite).
* **ESC**: Quit the game.
* **Mouse Click**: Interact with the "START" button on the menu.
# Dino Level-Up Project Report PDF File Link: https://drive.google.com/file/d/1P23R7h-zvrJZjDYzmupkAma7dQCDhaUZ/view?usp=sharing
