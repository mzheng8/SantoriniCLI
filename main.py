"""This file when called, runs the game and utilizes all other files"""
import logging
import sys
from game_manager import GameManager
from exceptions import (InvalidSymbolError,
                        InvalidWorkerError,
                        CantMoveThereError,
                        CantBuildThereError)

logging.basicConfig(filename='santorini.log', level=logging.DEBUG,
                    format='%(asctime)s|%(levelname)s|%(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class MainCLI:
    """Includes functions needed to run the command line interface"""
    def __init__(self):
        self.game_manager = None

    def print_board(self):
        """Prints board; this is in game_manager class"""
        self.game_manager.board.print_board()

    def get_user_input(self):
        """For human players"""
        while True:
            worker_input = input("Select a worker to move\n").upper()
            try:
                valid_worker = self.game_manager.current_player.check_worker_input(worker_input)
                if self.game_manager.can_worker_move(valid_worker):
                    break
                print("That worker cannot move")
            except (InvalidSymbolError, InvalidWorkerError) as e:
                print(e)
        while True:
            move_direction_input = input("Select a direction to move (n, ne, e, se, s, sw, w, nw)\n").lower()
            try:
                valid_move = self.game_manager.check_valid_move(move_direction_input, valid_worker)
                self.game_manager.make_move(valid_move, valid_worker)
                break
            except (ValueError, CantMoveThereError) as e:
                print(e)
        while True:
            build_direction_input = input("Select a direction to build (n, ne, e, se, s, sw, w, nw)\n").lower()
            try:
                valid_build = self.game_manager.check_valid_build(build_direction_input, valid_worker)
                self.game_manager.make_build(valid_build, valid_worker)
                self.game_manager.turn_details = (valid_worker.worker_symbol, valid_move, valid_build)
                break
            except (ValueError, CantBuildThereError) as e:
                print(e)

    def random_make_move(self):
        """For random players"""
        self.game_manager.random_make_move()

    def heuristic_make_move(self):
        """For heuristic players"""
        self.game_manager.heuristic_find_best_move()

    def play_game(self):
        """Identify player types and plays game"""
        if self.game_manager.current_player.player_type == "human":
            self.get_user_input()
            self.game_manager.turn_number += 1
        elif self.game_manager.current_player.player_type == "random":
            self.random_make_move()
            self.game_manager.turn_number += 1
        elif self.game_manager.current_player.player_type == "heuristic":
            self.heuristic_make_move()
            self.game_manager.turn_number += 1


    def run(self):
        """Parsing command line arguments and running the game"""

        if len(sys.argv) > 1:
            white_player_type = sys.argv[1].lower()
        else:
            white_player_type = "human"
        if len(sys.argv) > 2:
            blue_player_type = sys.argv[2].lower()
        else:
            blue_player_type = "human"
        # Enable types: on, off
        if len(sys.argv) > 3:
            undo_redo = sys.argv[3].lower()
        else:
            undo_redo = "off"
        if len(sys.argv) > 4:
            score_display = sys.argv[4].lower()
        else:
            score_display = "off"

        # Create GameManager with parsed args:
        self.game_manager = GameManager(white_player_type, blue_player_type, undo_redo, score_display)
        self.game_manager.save_state()

        display_score = bool(score_display == "on")
        while True:
            while not self.game_manager.is_game_over(self.game_manager.current_player, display_score):
                self.print_board()

                self.game_manager.print_turn_info(display_score)

                # If undo_redo is enabled
                if undo_redo == "on":
                    user_input = input("undo, redo, or next\n").lower()
                    if user_input == "undo":
                        self.game_manager.undo()
                    elif user_input == "redo":
                        self.game_manager.redo()
                    elif user_input == "next":
                        self.play_game()
                        self.game_manager.print_turn_summary(display_score)
                        self.game_manager.change_current_player()
                        self.game_manager.save_state()
                else:
                    self.play_game()
                    self.game_manager.print_turn_summary(display_score)
                    self.game_manager.change_current_player()
            # Game over, outside while loop, can double check with if is_game_over
            play_again = str(input("Play again?\n").lower())
            if play_again == "yes":
                self.game_manager.reset()
                continue
            sys.exit()

if __name__ == "__main__":
    try:
        MainCLI().run()
    except Exception as ex:
        print("Sorry! Something unexpected happened. Check the logs or contact the developer for assistance.")
        logging.error(str(ex.__class__.__name__) + ": " + repr(str(ex)))
