from ursina import *
from menu import MainMenu
import game_mechanics
import board
import figury
import chess
app = Ursina()
EditorCamera()

player = MainMenu().show()
players_turn = True if player == 'white' else False
game = False

board = chess.Board()


def update():
    global players_turn
    global game
    if players_turn and not game:
        pass
    elif not players_turn and not game:
        pass
    





    
#def Load_game():
   # pieces = load_pieces()
   # load_board()


app.run()
