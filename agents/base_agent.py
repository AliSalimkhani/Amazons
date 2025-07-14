from abc import ABC, abstractmethod
from core.board import Board
from core.move import Move

class Agent(ABC):
    def __init__(self, player_id: int, player_name: str):
        self.player_id = player_id
        self.player_name = player_name

    @abstractmethod
    def get_move(self, board: Board) -> Move:
        """Given the current board, return a valid move."""
        pass
