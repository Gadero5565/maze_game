from odoo import fields, models


class MazeGameScore(models.Model):
    _name = 'maze.game.score'
    _description = 'Maze Game Scores'
    _order = 'create_date desc'

    user_id = fields.Many2one('res.users', string='User', required=True, readonly=True)
    moves = fields.Integer(string='Moves', required=True)
    time_elapsed = fields.Integer(string='Time (seconds)', required=True)
    create_date = fields.Datetime(string='Date', readonly=True)
