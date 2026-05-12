# Maze Solver Visualizer

An interactive Python maze visualizer built for **COSC 316: Design and Analysis of Algorithms** at **Rafik Hariri University (RHU)** during the **Fall 2024** semester.

This project explores shortest-path and pathfinding ideas through a desktop application where users can generate random mazes, adjust maze size and wall density, edit walls manually, and watch the solver animate a path from start to goal.

## Live Demo

[Open the live project page](https://YOUR-USERNAME.github.io/YOUR-REPOSITORY-NAME/)

After you enable GitHub Pages, replace `YOUR-USERNAME` and `YOUR-REPOSITORY-NAME` with your actual GitHub username and repository name.

## Features

- Random maze generation with adjustable wall density
- Adjustable maze size through the GUI
- Click-to-edit maze walls
- Animated pathfinding from start to destination
- Visual game-style interface using custom images and textures
- Desktop GUI built with Tkinter

## What The Project Demonstrates

- Representing a maze as a graph/grid structure
- Applying pathfinding and shortest-path problem solving
- Using heuristics to improve search efficiency
- Understanding the tradeoff between correctness, speed, and usability
- Building an interactive visualization to make algorithm behavior easier to observe

## What I Learned In COSC 316

Through this course and project, I strengthened my understanding of:

- Graph modeling and traversal
- Shortest-path problem solving
- Heuristic search and how A\* differs from uninformed search
- Time and space complexity as practical design constraints
- Turning algorithm theory into a working interactive application

This project helped connect classroom concepts to implementation by showing how algorithms can be tested, visualized, and improved in a real program.

## Tech Stack

- Python
- Tkinter
- Pillow
- `heapq` for priority queue behavior

## How To Run

1. Install Python 3.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python main.py
```

## Project Files

- [main.py](main.py): main application logic and pathfinding implementation
- [character.png](character.png): player/character sprite
- [door.png](door.png): goal image
- [wall_texture.jpg](wall_texture.jpg): wall texture

## Course Context

This project was created as part of **COSC 316 - Design and Analysis of Algorithms** at **RHU** in **Fall 2024**. Its purpose is to combine algorithm design ideas with visualization and user interaction in a simple but meaningful application.
