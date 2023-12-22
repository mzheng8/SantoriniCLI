"""GameManager instance is created once game starts and houses all the important game features"""
import random
import copy
from players import WhitePlayer, BluePlayer
from board import Board
from exceptions import CantMoveThereError, CantBuildThereError, InvalidSymbolError, InvalidWorkerError

class GameManager:
    """Class for setting up the game requirements and functionalities"""
    def __init__(self, white_player_type='human', blue_player_type='human', undo_redo='off', score_display='off'):
        self.white_player = WhitePlayer(white_player_type)
        self.blue_player = BluePlayer(blue_player_type)
        self.undo_redo = undo_redo
        self.score_display = score_display

        self.list_of_players = [self.white_player, self.blue_player]
        self.current_player = self.list_of_players[0]

        self.turn_number = 1
        self.board = Board(self.list_of_players)
        self.board.history = []

        self.turn_details = (None, None, None)

#----------------------GAME CONDITIONS SETUP----------------------

    def change_current_player(self):
        """Changes the current player after every move, undo, and redo"""
        if self.current_player == self.white_player:
            self.current_player = self.blue_player
        elif self.current_player == self.blue_player:
            self.current_player = self.white_player

#----------------------CHECKING VALID INPUTS----------------------

    def check_valid_move(self, direction, worker):
        """Checks if the direction inputted is valid/can be moved to"""
        if direction not in ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']:
            raise ValueError("Not a valid direction")

        target_position = self.get_target_position(worker.position, direction)

        if self.is_within_board(target_position) is not True:
            raise CantMoveThereError(f"Cannot move {direction}")

        current_cell_value = self.board.gameboard[worker.position[0]][worker.position[1]]
        target_cell = self.board.gameboard[target_position[0]][target_position[1]]

        if len(target_cell) == 2:
            raise CantMoveThereError(f"Cannot move {direction}")
        if target_cell == "4":
            raise CantMoveThereError(f"Cannot move {direction}")
        if int(current_cell_value[0]) + 2 <= int(target_cell):
            raise CantMoveThereError(f"Cannot move {direction}")
        return direction

    def check_valid_build(self, direction, worker):
        """Checks if the direction inputted is valid/can be built onto"""
        if direction not in ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']:
            raise ValueError("Not a valid direction")

        target_position = self.get_target_position(worker.position, direction)

        if self.is_within_board(target_position) is not True:
            raise CantBuildThereError(f"Cannot build {direction}")

        target_cell = self.board.gameboard[target_position[0]][target_position[1]]

        if len(target_cell) == 2:
            raise CantBuildThereError(f"Cannot build {direction}")
        if target_cell == "4":
            raise CantBuildThereError(f"Cannot build {direction}")
        return direction

    def is_within_board(self, position):
        """Used by the check functions to see if the direction remains in the boundaries of the board"""
        if (0 <= int(position[0]) < 5 and 0 <= int(position[1]) < 5):
            return True
        return False

    def can_worker_move(self, worker):
        """Checks the 8 surrounding tiles and makes sure worker inputted can move"""
        for move_direction in ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']:
            try:
                self.check_valid_move(move_direction, worker)
                return True
            except CantMoveThereError:
                pass
        return False

#----------------------GAMEPLAY----------------------

    def get_target_position(self, current_position, direction):
        """Calculate the target position based on the current position and direction"""
        if direction == 'n':
            return (current_position[0] - 1, current_position[1])
        if direction == 'ne':
            return (current_position[0] - 1, current_position[1] + 1)
        if direction == 'e':
            return (current_position[0], current_position[1] + 1)
        if direction == 'se':
            return (current_position[0] + 1, current_position[1] + 1)
        if direction == 's':
            return (current_position[0] + 1, current_position[1])
        if direction == 'sw':
            return (current_position[0] + 1, current_position[1] - 1)
        if direction == 'w':
            return (current_position[0], current_position[1] - 1)
        if direction == 'nw':
            return (current_position[0] - 1, current_position[1] - 1)

    def make_move(self, direction, worker):
        """Moves the worker where it needs to be and updates the board"""
        target_position = self.get_target_position(worker.position, direction)
        current_cell_value = self.board.gameboard[worker.position[0]][worker.position[1]]
        self.board.update_board_position(worker.worker_symbol, worker.position, current_cell_value, target_position)
        worker.position = target_position


    def make_build(self, direction, worker):
        """Increases the value of the directed cell"""
        target_position = self.get_target_position(worker.position, direction)
        target_cell = self.board.gameboard[target_position[0]][target_position[1]]
        new_target_cell = str(int(target_cell) + 1)
        self.board.update_board_value(target_position, new_target_cell)

    def get_winner(self, player):
        """Check if there is a winner, if so, returns player name, else false"""
        for worker in player.workers:
            current_cell_value = self.board.gameboard[worker.position[0]][worker.position[1]]
            if current_cell_value[0] == "3":
                return player.name
        return False


# Could've also used can_worker_move
    def current_player_loses(self, current_player):
        """Check if current player has no moves that can be made"""
        for worker in current_player.workers:
            for move_direction in ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']:
                try:
                    self.check_valid_move(move_direction, worker)
                    for build_direction in ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']:
                        try:
                            self.check_valid_build(build_direction, worker)
                            return False
                        except CantBuildThereError:
                            pass
                except CantMoveThereError:
                    pass
        opponent = self.get_opponent(current_player)
        return opponent.name


    def is_game_over(self, current_player, display_score_value):
        """Ends the game if there is a winner or a loser"""
        opponent = self.get_opponent(current_player)
        # if current_player is winner
        if self.get_winner(current_player) is not False:
            self.board.print_board()
            self.print_turn_info(display_score_value)
            print(f"{self.get_winner(current_player)} has won")
            return True
        # if opponent is winner
        if self.get_winner(opponent) is not False:
            self.board.print_board()
            self.print_turn_info(display_score_value)
            print(f"{self.get_winner(opponent)} has won")
            return True
        # if current_player is loser
        if self.current_player_loses(current_player) is not False:
            self.board.print_board()
            self.print_turn_info(display_score_value)
            print(f"{self.current_player_loses(current_player)} has won")
            return True
        return False

#----------------------RANDOM PLAYER LOGIC----------------------

    def random_make_move(self):
        """Executes when one or more of the players is indicated as random"""
        while True:
            worker_random = random.choice(self.current_player.workers)
            try:
                if self.can_worker_move(worker_random):
                    break
            except (InvalidSymbolError, InvalidWorkerError):
                pass
        while True:
            move_direction_random = random.choice(['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'])
            try:
                valid_move_direction_random = self.check_valid_move(move_direction_random, worker_random)
                self.make_move(valid_move_direction_random, worker_random)
                break
            except (ValueError, CantMoveThereError):
                pass
        while True:
            build_direction_random = random.choice(['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'])
            try:
                valid_build_direction_random = self.check_valid_build(build_direction_random, worker_random)
                self.make_build(valid_build_direction_random, worker_random)
                self.turn_details = (worker_random.worker_symbol, valid_move_direction_random, valid_build_direction_random)
                break
            except (ValueError, CantBuildThereError):
                pass

#----------------------HEURISTICS PLAYER LOGIC----------------------

    # Calculating the scores
    def height_score(self, curr_player):
        """Calculates the height score of the workers"""
        sum_height = 0
        for worker in curr_player.workers:
            row, col = worker.position
            cell_value = self.board.gameboard[row][col]
            sum_height += int(cell_value[0])
        return sum_height

    def center_score(self, curr_player):
        """Calculates the distance score of the workers"""
        sum_center = 0
        for worker in curr_player.workers:
            row, col = worker.position
            if (row == 2) and (col == 2):
                sum_center += 2
            elif row in (0, 4) or col in (0, 4):
                sum_center += 0
            else:
                sum_center += 1
        return sum_center

    def distance_score(self, curr_player, opponent):
        """Calculates the distance score of the workers"""
        distance = 0
        distances_to_add = []
        distance_to_compare = []
        for opp_worker in opponent.workers:
            for worker in curr_player.workers:
                row_opp, col_opp = opp_worker.position
                row, col = worker.position
                distance_row = abs(row - row_opp)
                distance_col = abs(col - col_opp)
                distance_to_compare.append(max(distance_row, distance_col))
            distances_to_add.append(min(distance_to_compare))
            distance_to_compare = []
        for d in distances_to_add:
            distance += d
        final_distance = 8 - distance
        return final_distance

    def move_score(self, curr_player, opponent):
        """Calculates the move score using height, center, and distance"""
        height_score = self.height_score(curr_player)
        center_score = self.center_score(curr_player)
        distance_score = self.distance_score(curr_player, opponent)
        c1 = 3
        c2 = 2
        c3 = 1
        move_score = c1*height_score + c2*center_score + c3*distance_score
        return move_score

    def get_opponent(self, current_player):
        """Gets player's opponent class based on who current player is"""
        if current_player.name == "white":
            opponent = self.blue_player
        else:
            opponent = self.white_player
        return opponent

    def heuristic_find_best_move(self):
        """Heuristic player uses move_score to find best direction to move to"""
        trial_player = copy.deepcopy(self.current_player)
        trial_opp_player = self.get_opponent(trial_player)
        best_score = 0
        best_direction = None
        worker_with_best_direction = None
        for worker in trial_player.workers:
            initial_position = worker.position
            for direction in ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']:
                try:
                    valid_direction = self.check_valid_move(direction, worker)
                    trial_position = self.get_target_position(worker.position, valid_direction)
                    worker.position = trial_position
                    current_move_score = self.move_score(trial_player, trial_opp_player)
                    # Inflate the score if going to a specific cell gives heuristic player the win condition
                    if self.board.gameboard[worker.position[0]][worker.position[1]] == "3":
                        current_move_score = current_move_score * 10
                    if current_move_score > best_score:
                        best_direction = valid_direction
                        best_score = current_move_score
                        worker_with_best_direction = worker
                    elif current_move_score == best_score:
                        if random.choice([True, False]):
                            best_direction = valid_direction
                            worker_with_best_direction = worker
                    worker.position = initial_position
                except (ValueError, CantMoveThereError):
                    pass
        if (self.current_player.workers[0].worker_symbol == worker_with_best_direction.worker_symbol):
            self.heuristic_make_move(best_direction, self.current_player.workers[0])
        else:
            self.heuristic_make_move(best_direction, self.current_player.workers[1])

    def heuristic_make_move(self, direction, worker):
        """Heuristic player makes a build and move based on the given best direction"""
        self.make_move(direction, worker)
        while True:
            build_direction_random = random.choice(['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'])
            try:
                valid_build_direction_random = self.check_valid_build(build_direction_random, worker)
                self.make_build(valid_build_direction_random, worker)
                self.turn_details = (worker.worker_symbol, direction, valid_build_direction_random)
                break
            except (ValueError, CantBuildThereError):
                pass

#----------------------GAMEPLAY SAVE HISTORY----------------------

    def undo(self):
        """Undo to get previous state"""
        if self.board.history:
            if self.turn_number > 1:
                self.turn_number -= 1
                state = self.board.history[self.turn_number-1]
                self.restore_state(state)
                self.change_current_player()

    def redo(self):
        """Redo to get the next state"""
        if self.board.history:
            if self.turn_number < len(self.board.history):
                self.turn_number += 1
                state = self.board.history[self.turn_number-1]
                self.restore_state(state)
                self.change_current_player()

    def restore_state(self, desired_state):
        """Restoring the state of the board"""
        self.board.gameboard = [row[:] for row in desired_state['gameboard']]

        for player in self.board.players:
            for worker in player.workers:

                worker_symbol = worker.worker_symbol
                if worker_symbol in desired_state['workers']:
                    desired_row, desired_col = desired_state['workers'][worker_symbol]
                    desired_row, desired_col = int(desired_row), int(desired_col)
                    worker.worker_symbol = worker_symbol
                    worker.position = [desired_row, desired_col]

    def reset(self):
        """Reset the board and initial game conditions"""
        self.board.gameboard = [
            ["0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0"]
        ]

        self.worker_positions_dict = {}
        self.white_player.workers[0].position = [3, 1]
        self.white_player.workers[1].position = [1, 3]
        self.blue_player.workers[0].position = [1, 1]
        self.blue_player.workers[1].position = [3, 3]

        self.turn_number = 1
        self.current_player = self.list_of_players[0]
        self.board.initialize_workers_positions()

    def save_state(self):
        """Stores the state in the history"""
        state = {
            'gameboard': [row[:] for row in self.board.gameboard],
            'workers': {},
        }
        # Iterate over players + their workers
        for player in self.list_of_players:
            for worker in player.workers:
                row, col = worker.position
                state['workers'][worker.worker_symbol] = [row, col]
        # Append state to history list
        self.board.history.append(state)
        # Delete the end of a list when going back a turn, new move
        if len(self.board.history) > self.turn_number:
            del self.board.history[self.turn_number:]

    def print_turn_info(self, display_score_value):
        """Prints the turn number, current player, and score if needed"""
        if display_score_value is False:
            if self.current_player.name == "white":
                print(f"Turn: {self.turn_number}, {self.current_player.name} (AB)")
            else:
                print(f"Turn: {self.turn_number}, {self.current_player.name} (YZ)")
        elif display_score_value is True:
            if self.current_player.name == "white":
                print(f"Turn: {self.turn_number}, {self.current_player.name} (AB), ({self.height_score(self.current_player)}, {self.center_score(self.current_player)}, {self.distance_score(self.current_player, self.get_opponent(self.current_player))})")
            else:
                print(f"Turn: {self.turn_number}, {self.current_player.name} (YZ), ({self.height_score(self.current_player)}, {self.center_score(self.current_player)}, {self.distance_score(self.current_player, self.get_opponent(self.current_player))})")

    def print_turn_summary(self, display_score_value):
        """Prints turn summary and score if needed"""
        if display_score_value is False:
            print(f"{self.turn_details[0]},{self.turn_details[1]},{self.turn_details[2]}")
        elif display_score_value is True:
            print(f"{self.turn_details[0]},{self.turn_details[1]},{self.turn_details[2]} ({self.height_score(self.current_player)}, {self.center_score(self.current_player)}, {(self.distance_score(self.current_player, self.get_opponent(self.current_player)))})")
