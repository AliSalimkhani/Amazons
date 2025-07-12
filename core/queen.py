from core.position import Position


class Queen:
    def __init__(self, player_id: int, queen_id: int, position: Position):
        self.player_id = player_id
        self.queen_id = queen_id
        self.position = position
