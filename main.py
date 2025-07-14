import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from core.board import Board
from core.move import Move
from core.position import Position
from agents.random_agent import RandomAgent
from core.game import Game

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==== Initial Game Setup ====
board = Board()
player1_name = ""
player2_name = ""
player0 = RandomAgent(0,player1_name)
player1 = RandomAgent(1,player2_name)
game = Game(board, player0, player1)

# whenever you wanted to see the count of valid moves just type len(game.generate_valid_moves())

async def ai_game_loop():
    while not game.game_over:
        agent = game.players[board.current_turn]
        move = agent.get_move(board)
        board.apply_move(move)
        logger.info(f"AI Player {1-board.current_turn} moved: {move} , valid moves:{len(game.generate_valid_moves())}")

        valid_moves = game.generate_valid_moves()
        if not valid_moves:
            game.game_over = True
            game.winner = 1 - board.current_turn
            logger.info(f"Game over! Winner: Player {1 - game.winner} , {game.winner_name()}")
            break

        await asyncio.sleep(1)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Server starting up, launching AI game loop...")
    task = asyncio.create_task(ai_game_loop())
    try:
        yield
    finally:
        task.cancel()
        logger.info("Server shutting down, cancelled AI game loop.")

app = FastAPI(lifespan=lifespan)

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/")
def serve_frontend():
    return FileResponse("frontend/index.html")

class MoveRequest(BaseModel):
    queen_from: tuple[int, int]
    queen_to: tuple[int, int]
    arrow_to: tuple[int, int]

def serialize_board(board: Board):
    return [[cell if cell is not None else '.' for cell in row] for row in board.board_grid]

@app.get("/board")
def get_board():
    return {
        "grid": serialize_board(board),
        "turn": board.current_turn,
        "game_over": game.game_over,
        "winner": game.winner,
    }

@app.post("/move")
def post_move(req: MoveRequest):
    if game.game_over:
        raise HTTPException(status_code=400, detail="Game is already over.")

    from_pos = Position(*req.queen_from)
    to_pos = Position(*req.queen_to)
    arrow_pos = Position(*req.arrow_to)

    queens = board.player_queens[board.current_turn]
    for queen in queens:
        if queen.position == from_pos:
            move = Move(queen, to_pos, arrow_pos)
            if board.is_valid_move(move):
                board.apply_move(move)
                valid_moves = game.generate_valid_moves()
                if not valid_moves:
                    game.game_over = True
                    game.winner = 1 - board.current_turn
                return {"status": "ok"}
            else:
                raise HTTPException(status_code=400, detail="Invalid move")

    raise HTTPException(status_code=404, detail="Queen not found")

@app.post("/reset")
def reset_game():
    global board, game
    board = Board()
    game = Game(board, player0, player1)
    logger.info("Game has been reset")
    return {"status": "game reset"}
