import random
from odoo import http
from odoo.http import request


class MazeController(http.Controller):

    @http.route('/maze_game/generate', type='json', auth='user')
    def generate_maze(self, width=15, height=15):
        """Generate a maze using Kruskal's algorithm"""
        try:
            maze_gen = MazeGenerator(width, height)
            maze_data = maze_gen.kruskals_algorithm()

            # Convert numpy array to simple list for JSON serialization
            maze_list = maze_data

            # Find start and end positions
            start = (1, 1)  # Top-left corner
            end = (len(maze_list) - 2, len(maze_list[0]) - 2)  # Bottom-right corner

            return {
                'success': True,
                'maze': maze_list,
                'start': start,
                'end': end,
                'width': width,
                'height': height
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    @http.route('/maze_game/save_score', type='json', auth='user')
    def save_score(self, moves, time_elapsed):
        try:
            request.env['maze.game.score'].create({
                'user_id': request.env.user.id,
                'moves': moves,
                'time_elapsed': time_elapsed,
            })
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    @http.route('/maze_game/get_last_score', type='json', auth='user')
    def get_last_score(self):
        try:
            last_score = request.env['maze.game.score'].search(
                [('user_id', '=', request.env.user.id)],
                limit=1
            )
            if last_score:
                return {
                    'success': True,
                    'moves': last_score.moves,
                    'time_elapsed': last_score.time_elapsed,
                    'date': last_score.create_date.strftime('%Y-%m-%d %H:%M:%S')
                }
            return {'success': True, 'no_score': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}


class MazeGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = None

    def get_cell_coordinates(self, x, y):
        return 2 * y + 1, 2 * x + 1

    def remove_wall(self, x1, y1, x2, y2):
        row1, col1 = self.get_cell_coordinates(x1, y1)
        row2, col2 = self.get_cell_coordinates(x2, y2)
        self.maze[(row1 + row2) // 2][(col1 + col2) // 2] = 0

    def mark_cell(self, x, y):
        row, col = self.get_cell_coordinates(x, y)
        self.maze[row][col] = 0

    def get_neighbors(self, x, y):
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbors.append((nx, ny))
        return neighbors

    def kruskals_algorithm(self):
        # Initialize with all walls (1 = wall, 0 = path)
        self.maze = [[1 for _ in range(self.width * 2 + 1)]
                     for _ in range(self.height * 2 + 1)]

        # Mark all cells
        for y in range(self.height):
            for x in range(self.width):
                self.mark_cell(x, y)

        # Create a list of all possible walls
        walls = []
        for y in range(self.height):
            for x in range(self.width):
                if x < self.width - 1:
                    walls.append((x, y, x + 1, y))  # Horizontal wall
                if y < self.height - 1:
                    walls.append((x, y, x, y + 1))  # Vertical wall

        # Shuffle the walls
        random.shuffle(walls)

        # Union-Find data structure
        parent = {}
        rank = {}

        def find(cell):
            if parent[cell] != cell:
                parent[cell] = find(parent[cell])
            return parent[cell]

        def union(cell1, cell2):
            root1 = find(cell1)
            root2 = find(cell2)
            if root1 != root2:
                if rank[root1] > rank[root2]:
                    parent[root2] = root1
                else:
                    parent[root1] = root2
                    if rank[root1] == rank[root2]:
                        rank[root2] += 1

        # Initialize union-find
        for y in range(self.height):
            for x in range(self.width):
                cell = (x, y)
                parent[cell] = cell
                rank[cell] = 0

        # Process walls
        for wall in walls:
            x1, y1, x2, y2 = wall
            cell1 = (x1, y1)
            cell2 = (x2, y2)

            if find(cell1) != find(cell2):
                self.remove_wall(x1, y1, x2, y2)
                union(cell1, cell2)

        return self.maze
