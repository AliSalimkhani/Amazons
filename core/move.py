from core.position import Position
from core.queen import Queen


class Move:
    def __init__(self, queen: Queen, queen_to: Position, arrow_position: Position):
        self.arrow_position = arrow_position
        self.queen_to = queen_to
        self.queen = queen

    def __repr__(self):
        return f"Player {self.queen.player_id} moved its queen {self.queen.queen_id} from {self.queen.position} to {self.queen_to}, arrowed {self.arrow_position}"


