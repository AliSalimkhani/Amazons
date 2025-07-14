from agents.base_agent import Agent
from core.move import Move
from core.board import Board
from core.position import Position


class Game:
    def __init__(self, board: Board, player0: Agent, player1: Agent):
        self.board = board
        self.players = [player0, player1]
        self.game_over = False
        self.winner = None

    @property
    def current_turn(self):
        return self.board.current_turn

    def possible_positions(self, start_pos):
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        positions = []

        for dx, dy in directions:
            x, y = start_pos.x, start_pos.y
            while True:
                x += dx
                y += dy
                if not self.board.in_bounds(x, y):
                    break
                if self.board.board_grid[x][y] is not None:
                    break
                positions.append(Position(x, y))
        return positions

    def generate_valid_moves(self):
        moves = []
        for queen in self.board.player_queens[self.current_turn]:
            for queen_dest in self.possible_positions(queen.position):
                for arrow_pos in self.possible_positions(queen_dest):
                    move = Move(queen, queen_dest, arrow_pos)
                    if self.board.is_valid_move(move):
                        moves.append(move)
        return moves

    def play(self):
        while not self.game_over:
            self.board.print_board()
            print(f"Player {self.current_turn}'s turn.")
            valid_moves = self.generate_valid_moves()
            if not valid_moves:
                print(f"Player {self.current_turn} has no valid moves!")
                self.game_over = True
                self.winner = 1 - self.current_turn
                print(f"Player {self.winner} wins!")
                return
            move = valid_moves[0]
            self.board.apply_move(move)
            self.board.current_turn = 1 - self.board.current_turn

