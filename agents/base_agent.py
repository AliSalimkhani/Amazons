from abc import ABC, abstractmethod
from core.board import Board
from core.move import Move

class Agent(ABC):
    def __init__(self, player_id: int):
        self.player_id = player_id

    @abstractmethod
    def get_move(self, board: Board) -> Move:
        """Given the current board, return a valid move."""
        pass
