# 🎮 Python Pac-Man Game

A classic **Pac-Man-inspired arcade game developed with Python and Pygame**. This project recreates the core Pac-Man gameplay experience while adding features such as multiple levels, power pellets, fruit rewards, ghost AI behaviour, sound effects, lives, and persistent high scores.

The project was developed as a practical Python game-development project to strengthen skills in **object-oriented programming, game logic, event handling, collision detection, file handling, and audio integration**.

---

## 🕹️ Game Overview

The player controls Pac-Man through a maze, collecting dots and power pellets while avoiding ghosts.

The objective is to:

* Collect as many dots as possible.
* Eat power pellets to temporarily become stronger against ghosts.
* Collect bonus fruit for additional points.
* Avoid normal ghosts.
* Complete the maze and progress to the next level.
* Achieve the highest possible score.



## ✨ Features

### 🎯 Core Gameplay

* Pac-Man style maze navigation
* Keyboard-controlled player movement
* Collectible dots
* Power pellets
* Ghost enemies
* Collision detection
* Lives system
* Score tracking
* Win and Game Over screens

### 👻 Ghost Behaviour

The game includes different ghost behaviours to make gameplay more challenging:

* **Chasing ghosts** attempt to follow Pac-Man.
* **Guard ghosts** patrol or protect the central maze area.
* Ghosts become faster as the player progresses through levels.
* Power pellets allow Pac-Man to temporarily defeat frightened ghosts.

### 🍒 Bonus Fruit

A bonus fruit appears during gameplay.

* Worth **500 points**
* Available for a limited amount of time
* Provides an additional scoring opportunity

### 🗺️ Multiple Levels

The game includes more than one maze.

After completing a maze, the player progresses to the next level.

Each level increases the challenge by changing the maze and increasing ghost speed.

### 🏆 High Score System

The game saves the player's high score to a text file.

The high score is stored in:


highscore.txt


This allows the score to remain available after closing and reopening the game.

### 🔊 Audio

The game includes audio for different gameplay events, including:

* Initial/start sound
* Pac-Man eating collectibles
* Ghost interactions
* Pac-Man being caught
* Game Over
* Background/gameplay music

Sound files are stored inside the:



assets folder.

---

## 🛠️ Technologies Used

| Technology                      | Purpose                                                    |
| ------------------------------- | ---------------------------------------------------------- |
| **Python**                      | Main programming language                                  |
| **Pygame**                      | Game development, graphics, keyboard input and audio       |
| **Object-Oriented Programming** | Organising players, ghosts and game objects                |
| **File Handling**               | Saving and loading the high score                          |
| **Python Enums**                | Managing movement directions                               |
| **Collision Detection**         | Detecting interactions between Pac-Man, ghosts and objects |

---

## 📂 Project Structure


python-pacman/
│
├── assets/
│   ├── audio files
│   └── other game assets
│
├── highscore.txt
├── PacManScreenshot 2026-09-28 113243.png
├── python pacman.py
├── .gitignore
└── README.md


---

## 💻 Installation

### 1. Clone the repository


git clone https://github.com/batseba14/python-pacman.git


### 2. Open the project folder


cd python-pacman


### 3. Install Pygame

Make sure Python is installed, then run:


pip install pygame

If you are using a virtual environment, activate it first.

### Windows

powershell
python -m venv venv
venv\Scripts\activate
pip install pygame


## ▶️ Running the Game

Run the Python game using:

bash
python "python pacman.py"


The game window should open and display the Pac-Man maze.


## 🎮 Controls

| Key            | Action     |
| -------------- | ---------- |
| ⬆️ Arrow Up    | Move Up    |
| ⬇️ Arrow Down  | Move Down  |
| ⬅️ Arrow Left  | Move Left  |
| ➡️ Arrow Right | Move Right |
| **R**          | R          |
