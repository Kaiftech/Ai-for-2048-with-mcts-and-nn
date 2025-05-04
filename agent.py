# agent.py

from game2048 import Game2048
from mcts import MCTS
from model import Model
from heuristics import compute_fitness  # Import the new fitness function

class Agent:
    def __init__(self, model=None):
        # Initialize neural network (clone if provided)
        if model is None:
            self.model = Model()
        else:
            self.model = model
        self.game = Game2048()
        self.mcts = MCTS(self.model, num_simulations=30, c_puct=1.0)

    def new_game(self):
        """Reset the game state and score."""
        self.game.reset()

    @property
    def score(self):
        return self.game.score

    def play_move(self):
        """Use MCTS to choose and apply one move to the game."""
        if self.game.is_done():
            return  # No moves possible
        action = self.mcts.search(self.game)
        if action is None:
            return
        # Apply the chosen move
        if action == 0:
            self.game.move_up()
        elif action == 1:
            self.game.move_down()
        elif action == 2:
            self.game.move_left()
        elif action == 3:
            self.game.move_right()

    def compute_fitness(self):
        """Return the fitness score based on the game's grid and score."""
        return compute_fitness(self.game)  # Use the new fitness function
