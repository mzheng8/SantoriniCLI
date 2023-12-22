"""Initializes board and has methods that are called to change and display the new board"""
class Board:
    """Class for setting up the board, and updating based on the game. """
    def __init__(self, players):
        self.players = players
        self.gameboard = [
            ["0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0"]
        ]

        self.worker_positions_dict = {}
        self.initialize_workers_positions()

        self.history = []


#----------------------GAME SETUP----------------------

    def initialize_workers_positions(self):
        """Initialize positions for starting board"""
        for player in self.players:
            for worker in player.workers:
                row, col = worker.position
                self.gameboard[row][col] = f"0{worker.worker_symbol}"
                self.worker_positions_dict[worker.worker_symbol] = worker.position

    def print_board(self):
        """Displays the board"""
        horizontal_line = "+--+--+--+--+--+"
        for row in self.gameboard:
            print(horizontal_line)
            print("|"+"|".join(f"{block:2}" for block in row)+"|")
        print(horizontal_line)


#----------------------UPDATING MOVES----------------------

    def update_board_position(self, symbol, cur_pos, cur_cell_value, new_pos):
        """Updates the all of the worker's positions on the board"""
        self.gameboard[int(cur_pos[0])][int(cur_pos[1])] = cur_cell_value[:1] + cur_cell_value [2:]
        row, col = new_pos
        self.gameboard[row][col] = self.gameboard[row][col] + f"{symbol}"
        self.worker_positions_dict[symbol] = new_pos

    def update_board_value(self, cell_position, new_value):
        """Updates the value of the cell"""
        self.gameboard[int(cell_position[0])][int(cell_position[1])] = new_value
