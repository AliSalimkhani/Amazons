from core.move import Move
from core.position import Position
from core.queen import Queen


class Board:
    def __init__(self, size=10):
        self.size = size
        self.board_grid = [[None for _ in range(size)] for _ in range(size)]

        self.player_queens = {
            0: [
                Queen(0, 0, Position(0, 3)),
                Queen(0, 1, Position(0, 6)),
                Queen(0, 2, Position(3, 0)),
                Queen(0, 3, Position(3, 9)),
            ],
            1: [
                Queen(1, 0, Position(6, 0)),
                Queen(1, 1, Position(6, 9)),
                Queen(1, 2, Position(9, 3)),
                Queen(1, 3, Position(9, 6)),
            ],
        }

        for player_id, queens in self.player_queens.items():
            for queen in queens:
                pos = queen.position
                self.board_grid[pos.x][pos.y] = f"Q{queen.player_id}-{queen.queen_id}"

        self.current_turn = 0

    def in_bounds(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size

    def is_clear_path(self, start: Position, end: Position) -> bool:
        dx = end.x - start.x
        dy = end.y - start.y

        step_x = (dx // abs(dx)) if dx != 0 else 0
        step_y = (dy // abs(dy)) if dy != 0 else 0

        if dx != 0 and dy != 0 and abs(dx) != abs(dy):
            return False  # not a straight or diagonal move

        x, y = start.x + step_x, start.y + step_y
        while (x, y) != (end.x, end.y):
            if not self.in_bounds(x, y) or self.board_grid[x][y] is not None:
                return False
            x += step_x
            y += step_y

        def current_player_name(self):
            return self.players[self.current_turn].player_name

        def winner_name(self):
            if self.winner is None:
                return None
            return self.players[self.winner].player_name

        return self.in_bounds(end.x, end.y) and self.board_grid[end.x][end.y] is None

    def is_valid_arrow(self, start: Position, arrow: Position) -> bool:
        if not self.in_bounds(arrow.x, arrow.y):
            return False
        if self.board_grid[arrow.x][arrow.y] is not None:
            return False
        return self.is_clear_path(start, arrow)

    def is_valid_move(self, move: Move) -> bool:
        start = move.queen.position
        dest = move.queen_to
        arrow = move.arrow_position

        if move.queen.player_id != self.current_turn:
            print(f"It's not Player {move.queen.player_id}'s turn!")
            return False

        if start == dest:
            print("Redundant move: Queen not moved.")
            return False

        if not self.in_bounds(dest.x, dest.y):
            print("Destination out of bounds.")
            return False

        if self.board_grid[dest.x][dest.y] is not None:
            print("Destination square is not empty.")
            return False

        if not self.is_clear_path(start, dest):
            print("Path to destination is blocked.")
            return False

        self.board_grid[start.x][start.y] = None
        self.board_grid[dest.x][dest.y] = f"Q{self.current_turn}-{move.queen.queen_id}"

        valid_arrow = self.is_valid_arrow(dest, arrow)

        self.board_grid[start.x][start.y] = f"Q{self.current_turn}-{move.queen.queen_id}"
        self.board_grid[dest.x][dest.y] = None

        if not valid_arrow:
            print("Invalid arrow shot.")
            return False

        return True

    def apply_move(self, move: Move):
        if not self.is_valid_move(move):
            raise ValueError("Tried to apply an invalid move.")

        player_id = move.queen.player_id
        old_pos = move.queen.position
        new_pos = move.queen_to
        arrow_pos = move.arrow_position

        # Update board
        self.board_grid[old_pos.x][old_pos.y] = None
        self.board_grid[new_pos.x][new_pos.y] = f"Q{player_id}-{move.queen.queen_id}"
        self.board_grid[arrow_pos.x][arrow_pos.y] = "X"

        # Update queen position
        move.queen.position = new_pos

        # Change turn
        self.current_turn = 1 - self.current_turn

    def print_board(self):
        # Print column headers
        print("    " + "   ".join(f"{j:>3}" for j in range(self.size)))
        print("   +" + "-----+" * self.size)

        for i in range(self.size):
            row = []
            for j in range(self.size):
                cell = self.board_grid[i][j]
                # Make sure every cell is 5 characters wide for alignment
                row.append(f"{cell or ' . ':^5}")
            print(f"{i:>2} |" + "|".join(row) + "|")
            print("   +" + "-----+" * self.size)

