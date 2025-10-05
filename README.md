# Odoo Maze Game Module

An interactive maze game built with Odoo OWL framework that provides engaging gameplay with score tracking and persistence.

## Features

- 🎮 **Interactive Maze Gameplay**: Navigate through randomly generated mazes using arrow keys
- ⏱️ **Real-time Tracking**: Monitor moves count and time elapsed during gameplay
- 📊 **Score Persistence**: Automatically saves game results linked to user accounts
- 🏆 **Performance Display**: Shows your last score (moves, time, and date) on the game page
- 🔄 **Dynamic Maze Generation**: Uses Kruskal's algorithm for unique mazes every game
- 📱 **Responsive Design**: Clean UI that works across different screen sizes

## Installation

### Method 1: Standard Odoo Module Installation
1. Clone this repository or download the module files
2. Place the `maze_game` folder in your Odoo addons directory
3. Update the apps list in Odoo:
   ```bash
   odoo-bin -d your_database -u maze_game --stop-after-init