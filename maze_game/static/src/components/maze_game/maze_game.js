/** @odoo-module **/
import { Component, useState, onMounted, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

class MazeGameTemplate extends Component {
    static template = "maze_game.MazeGame";

    setup() {
        this.rpc = useService("rpc");
        this.state = useState({
            loading: false,
            maze: null,
            playerPosition: { row: 0, col: 0 },
            endPosition: { row: 0, col: 0 },
            gameStarted: false,
            gameCompleted: false,
            timeElapsed: 0,
            lastScore: null,
            timerInterval: null,
            moves: 0,
            error: null
        });

        onMounted(() => {
            this.initializeGame();
            document.addEventListener('keydown', this.handleKeyPress.bind(this));
        });

        onWillUnmount(() => {
            document.removeEventListener('keydown', this.handleKeyPress.bind(this));
            this.stopTimer();
        });
    }

    async initializeGame() {
        this.state.loading = true;
        try {
            const result = await this.rpc('/maze_game/generate', {
                width: 15,
                height: 15
            });

            if (result.success) {
                this.state.maze = result.maze;
                this.state.playerPosition = {
                    row: result.start[0],
                    col: result.start[1]
                };
                this.state.endPosition = {
                    row: result.end[0],
                    col: result.end[1]
                };
                this.state.gameStarted = false;
                this.state.gameCompleted = false;
                this.state.timeElapsed = 0;
                this.state.moves = 0;
                await this.fetchLastScore();
            } else {
                this.state.error = result.error;
            }
        } catch (error) {
            this.state.error = "Failed to generate maze";
        } finally {
            this.state.loading = false;
        }
    }

    async fetchLastScore() {
        try {
            const result = await this.rpc('/maze_game/get_last_score');
            if (result.success && !result.no_score) {
                this.state.lastScore = {
                    moves: result.moves,
                    time_elapsed: result.time_elapsed,
                    date: result.date
                };
            } else {
                this.state.lastScore = null;
            }
        } catch (error) {
            console.error('Failed to fetch last score:', error);
        }
    }

    startGame() {
        this.state.gameStarted = true;
        this.state.gameCompleted = false;
        this.state.timeElapsed = 0;
        this.state.moves = 0;
        this.startTimer();
    }

    startTimer() {
        this.stopTimer(); // Clear any existing timer
        this.state.timerInterval = setInterval(() => {
            this.state.timeElapsed++;
        }, 1000);
    }

    stopTimer() {
        if (this.state.timerInterval) {
            clearInterval(this.state.timerInterval);
            this.state.timerInterval = null;
        }
    }

    handleKeyPress(event) {
        if (!this.state.gameStarted || this.state.gameCompleted) {
            return;
        }

        const key = event.key;
        let newRow = this.state.playerPosition.row;
        let newCol = this.state.playerPosition.col;

        switch (key) {
            case 'ArrowUp':
                newRow--;
                break;
            case 'ArrowDown':
                newRow++;
                break;
            case 'ArrowLeft':
                newCol--;
                break;
            case 'ArrowRight':
                newCol++;
                break;
            default:
                return; // Ignore other keys
        }

        this.movePlayer(newRow, newCol);
    }

    movePlayer(newRow, newCol) {
        // Check if move is valid (within bounds and not a wall)
        if (this.isValidMove(newRow, newCol)) {
            this.state.playerPosition = { row: newRow, col: newCol };
            this.state.moves++;

            // Check if player reached the end
            if (newRow === this.state.endPosition.row &&
                newCol === this.state.endPosition.col) {
                this.completeGame();
            }
        }
    }

    isValidMove(row, col) {
        // Check boundaries
        if (row < 0 || row >= this.state.maze.length ||
            col < 0 || col >= this.state.maze[0].length) {
            return false;
        }

        // Check if it's a wall (1 = wall, 0 = path)
        return this.state.maze[row][col] === 0;
    }

    completeGame() {
        this.state.gameCompleted = true;
        this.state.gameStarted = false;
        this.stopTimer();
        this.saveScore();
    }

    resetGame() {
        this.stopTimer();
        this.initializeGame();
    }

    formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }

    getCellClass(row, col) {
        const classes = [];

        if (this.state.maze[row][col] === 1) {
            classes.push('wall');
        } else {
            classes.push('path');
        }

        if (row === this.state.playerPosition.row &&
            col === this.state.playerPosition.col) {
            classes.push('player');
        }

        if (row === this.state.endPosition.row &&
            col === this.state.endPosition.col) {
            classes.push('end');
        }

        return classes.join(' ');
    }

    async saveScore() {
        try {
            const result = await this.rpc('/maze_game/save_score', {
                moves: this.state.moves,
                time_elapsed: this.state.timeElapsed
            });
            if (!result.success) {
                console.error('Failed to save score:', result.error);
            }
        } catch (error) {
            console.error('Error saving score:', error);
        }
    }

}

registry.category("actions").add("maze_game", MazeGameTemplate);