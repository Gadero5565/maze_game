# -*- coding: utf-8 -*-
{
    'name': "maze_game",
    'summary': "An interactive maze game with score tracking for Odoo users",
    'description': """
        This module provides an engaging maze game built with Odoo OWL framework. 
        Users can navigate a randomly generated maze using arrow keys, 
        aiming to reach the end with the fewest moves and shortest time. The module includes:
            - Maze generation using Kruskal's algorithm for varied gameplay
            - Real-time tracking of moves and time elapsed
            - Persistent score storage linked to user accounts
            - Display of the user's last score (moves, time, and date) on the game page
            - Responsive UI with clear instructions and game controls
        Ideal for adding a fun, interactive feature to your Odoo instance, 
        with potential for leaderboards or further enhancements.
    """,
    'author': "Gadeer Mahmoud",
    'website': "https://github.com/Gadero5565",
    'category': 'Games',
    'version': '1.0.0',
    'depends': ['web'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    "assets": {
        'web.assets_backend': [
            '/maze_game/static/src/components/**/*.js',
            '/maze_game/static/src/components/**/*.xml',
            '/maze_game/static/src/components/**/*.scss',
        ],
    },
    'licence': 'LGPL-3',
}
