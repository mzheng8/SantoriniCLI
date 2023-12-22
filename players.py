"""Initializes worker and player classes"""
from exceptions import InvalidSymbolError, InvalidWorkerError


#----------------------WORKER CLASS----------------------

class Worker:
    """Creates a worker class with respective symbol and position on the board"""
    def __init__(self, worker_symbol, position):
        self.worker_symbol = worker_symbol  # A, B, Y, Z
        self.position = position


#----------------------PLAYER CLASS----------------------

class Player:
    """Builds the player class for white, blue, random and heursitic"""
    def __init__(self, name, workers, player_type):
        self.name = name
        self.workers = workers
        self.player_type = player_type

    def check_worker_input(self, worker_user_input):
        """Checks if the worker chosen is a valid worker"""
        valid_workers = ["A", "B", "Y", "Z"]

        if worker_user_input not in valid_workers:
            raise InvalidSymbolError("Not a valid worker")

        # If the user input matches with current player's list of workers
        matching_worker = next((worker for worker in self.workers
                                if worker.worker_symbol == worker_user_input), None)

        # If a matching worker is found, it is returned
        if matching_worker:
            return matching_worker
        raise InvalidWorkerError("That is not your worker")



#----------------------WHITE BLUE PLAYERS----------------------

# White and Blue players inherit from Player
class WhitePlayer(Player):
    """Creates an instance of white player"""
    def __init__(self, player_type):
        super().__init__("white", [Worker("A", [3, 1]), Worker("B", [1, 3])], player_type)


class BluePlayer(Player):
    """Creates an instance of blue player"""
    def __init__(self, player_type):
        super().__init__("blue", [Worker("Y", [1, 1]), Worker("Z", [3, 3])], player_type)
