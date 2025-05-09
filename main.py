from ursina import *
from figury import *
from board import *

app = Ursina()

# Add lighting
DirectionalLight(position=(1, 1, 3), shadows=True, color=color.white)

# Create chess pieces
pieces = [
    Rook(kolor='white', position='a1'),
    Rook(kolor='white', position='h1'),
    Knight(kolor='white', position='b1'),
    Knight(kolor='white', position='g1'),
    Bishop(kolor='white', position='c1'),
    Bishop(kolor='white', position='f1'),
    Queen(kolor='white', position='d1'),
    King(kolor='white', position='e1'),
    Pawn(kolor='white', position='a2'),
    Pawn(kolor='white', position='b2'),
    Pawn(kolor='white', position='c2'),
    Pawn(kolor='white', position='d2'),
    Pawn(kolor='white', position='e2'),
    Pawn(kolor='white', position='f2'),
    Pawn(kolor='white', position='g2'),
    Pawn(kolor='white', position='h2'),
    Rook(kolor='black', position='a8'),
    Rook(kolor='black', position='h8'),
    Knight(kolor='black', position='b8'),
    Knight(kolor='black', position='g8'),
    Bishop(kolor='black', position='c8'),
    Bishop(kolor='black', position='f8'),
    Queen(kolor='black', position='d8'),
    King(kolor='black', position='e8'),
    Pawn(kolor='black', position='a7'),
    Pawn(kolor='black', position='b7'),
    Pawn(kolor='black', position='c7'),
    Pawn(kolor='black', position='d7'),
    Pawn(kolor='black', position='e7'),
    Pawn(kolor='black', position='f7'),
    Pawn(kolor='black', position='g7'),
    Pawn(kolor='black', position='h7'),
]

# Add chessboard
board = load_board()

# Camera
EditorCamera()

# Update function to handle highlighting
def update():
    for piece in pieces:
        piece.highlight_piece()  # Call the highlight logic for each piece

app.run()
