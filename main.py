# Create chess pieces
from ursina import *
from figury import *
from board import *
from importlib import import_module

app = Ursina()
DirectionalLight(position=(1, 1, 3), shadows=True, kolor=color.white)
white_rook1 = Rook(kolor='white', position='a1')
white_rook2 = Rook(kolor='white', position='h1')
white_knight1 = Knight(kolor='white', position='b1')
white_knight2 = Knight(kolor='white', position='g1')
white_bishop1 = Bishop(kolor='white', position='c1')
white_bishop2 = Bishop(kolor='white', position='f1')
white_queen = Queen(kolor='white', position='d1')
white_king = King(kolor='white', position='e1')
white_pawn1 = Pawn(kolor='white', position='a2')
white_pawn2 = Pawn(kolor='white', position='b2')
white_pawn3 = Pawn(kolor='white', position='c2')
white_pawn4 = Pawn(kolor='white', position='d2')
white_pawn5 = Pawn(kolor='white', position='e2')
white_pawn6 = Pawn(kolor='white', position='f2')
white_pawn7 = Pawn(kolor='white', position='g2')
white_pawn8 = Pawn(kolor='white', position='h2')
black_rook1 = Rook(kolor='black', position='a8')
black_rook2 = Rook(kolor='black', position='h8')
black_knight1 = Knight(kolor='black', position='b8')
black_knight2 = Knight(kolor='black', position='g8')
black_bishop1 = Bishop(kolor='black', position='c8')
black_bishop2 = Bishop(kolor='black', position='f8')
black_queen = Queen(kolor='black', position='d8')
black_king = King(kolor='black', position='e8')
black_pawn1 = Pawn(kolor='black', position='a7')
black_pawn2 = Pawn(kolor='black', position='b7')
black_pawn3 = Pawn(kolor='black', position='c7')
black_pawn4 = Pawn(kolor='black', position='d7')
black_pawn5 = Pawn(kolor='black', position='e7')
black_pawn6 = Pawn(kolor='black', position='f7')
black_pawn7 = Pawn(kolor='black', position='g7')
black_pawn8 = Pawn(kolor='black', position='h7')
pieces = [
    white_rook1, white_rook2, white_knight1, white_knight2, white_bishop1, white_bishop2,
    white_queen, white_king, white_pawn1, white_pawn2, white_pawn3, white_pawn4,
    white_pawn5, white_pawn6, white_pawn7, white_pawn8,
    black_rook1, black_rook2, black_knight1, black_knight2, black_bishop1, black_bishop2,
    black_queen, black_king, black_pawn1, black_pawn2, black_pawn3, black_pawn4,
    black_pawn5, black_pawn6, black_pawn7, black_pawn8
]
# Add chessboard
board = load_board()

# Camera
EditorCamera()

# Update function to handle highlighting
# def update():
#     for piece in pieces:
#         piece.highlight_piece()  # Call the highlight logic for each piece

app.run()
