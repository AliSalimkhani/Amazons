import random
from agents.base_agent import Agent
from core.board import Board
from core.game import Game
from core.move import Move


class RandomAgent(Agent):
    def get_move(self, board: Board) -> Move:
        temp_game = Game(board, self, self)
        temp_game.board.current_turn = self.player_id
        valid_moves = temp_game.generate_valid_moves()
        if not valid_moves:
            raise RuntimeError("No valid moves available for RandomAgent")
        return random.choice(valid_moves)


