import random
from agents.base_agent import Agent
from core.board import Board
from core.game import Game
from core.move import Move


class RandomAgent(Agent):
    def get_move(self, board: Board) -> Move:
        # Create a temporary Game instance for move generation
        # but assign the proper current turn
        temp_game = Game(board, self, self)  # dummy players
        # Override property via internal attribute to trick it (not ideal)
        temp_game.board.current_turn = self.player_id  # or just use board's current_turn if set correctly
        valid_moves = temp_game.generate_valid_moves()
        if not valid_moves:
            raise RuntimeError("No valid moves available for RandomAgent")
        return random.choice(valid_moves)


