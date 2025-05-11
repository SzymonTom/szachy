# Create chess pieces
from ursina import *
from figury import *
from board import *
import chess
app = Ursina()
DirectionalLight(position=(1, 1, 3), shadows=True, kolor=color.white)


board = chess.Board()
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
board_loaded = load_board()
board = chess.Board()
# Lista przechowująca wszystkie podświetlenia
podswietl_entities = []

def clear_highlight():
    
    global podswietl_entities
    for entity in podswietl_entities:
        destroy(entity)
    podswietl_entities = []

if board is None:
    print("Failed to load the chessboard model.")
# Camera
EditorCamera()
# Globalna zmienna do przechowywania zaznaczonej figury
pom_black = 0
pom_white = 0
pom_x_white = 0
pom_x_black = 0
#global clicked_piece_position
clicked_piece_position = None
def update():
    global clicked_piece_position
    if mouse.left:    
        move_position = None
        for podswietlenie in podswietl_entities:
            if podswietlenie.clicked_square() is not None and clicked_piece_position is not None:
                move_position = podswietlenie.clicked_square()
                destroy_position = is_capture(clicked_piece_position, move_position)
                castling_position,castle_from = is_castle(clicked_piece_position, move_position)
        for piece in pieces:
            if move_position is not None:
                if piece.was_clicked:
                    board.push(chess.Move.from_uci(piece.board_position+move_position))
                    piece.update_position(move_position)
                    #piece.was_clicked = False
                    clear_highlight()
                    #move_position = None
                elif piece.board_position == destroy_position:
                    capture_piece(piece)
                elif piece.board_position == castle_from:
                    piece.update_position(castling_position)
            position=piece.clicked_piece()
            clicked_piece_position = position if position is not None else clicked_piece_position
            highlight_squares(position)


def input(key):
    global zaznaczony_pion

    if key == 'left mouse down':
        if not mouse.hovered_entity or not isinstance(mouse.hovered_entity, ChessPiece):
            if zaznaczony_pion:
                zaznaczony_pion.un_klik()       #Prace w toku. Cos nie chce sie globalna zmienna przesłać chyba. Bo globalna miała przechowywać zaznaczonego pionka i tutaj mial sie usuwac jak klikniesz gdzies indziej.
                zaznaczony_pion = None


def highlight_squares(position):
    legal_moves_list = []   
    if position is not None:  # Dodaj sprawdzenie!
        clicked_piece_position = position
        clear_highlight()
        legal_moves_list=check_legal_moves(position)
        for move in legal_moves_list:
            podswietl=LegalMove(move)
            podswietl_entities.append(podswietl)
    return legal_moves_list    

def check_legal_moves(position):
        square = chess.parse_square(position)
        legal_moves = []
        for move in board.legal_moves:
            # Sprawdź, czy ruch dotyczy tej figury
            if move.from_square == square:
                move_to = chess.square_name(move.to_square)
                legal_moves.append(move_to)
        return legal_moves

def is_capture(clicked_piece_position, move_position):
    """
    Funkcja do sprawdzania czy ruch jest biciem.
    """
    if board.is_en_passant(chess.Move.from_uci(clicked_piece_position+move_position)):
        destroy_position = move_position[0] + str(int(move_position[1]) - 1)
    else: destroy_position = move_position
    return destroy_position

def is_castle(clicked_piece_position, move_position):
    """
    Funkcja do sprawdzania czy ruch jest roszadą.
    """
    castle_position = None
    castle_from = None
    if board.is_castling(chess.Move.from_uci(clicked_piece_position+move_position)):
        if move_position[0] == 'c':
            castle_position = 'd'+ move_position[1]
            castle_from = 'a' + move_position[1]
        elif move_position[0] == 'g':
            castle_position = 'f'+ move_position[1] 
            castle_from = 'h' + move_position[1]
    return castle_position, castle_from

def capture_piece(piece):
    """
    Funkcja do usuwania figury z planszy.
    """
    global pom_white
    global pom_black
    global pom_x_white
    global pom_x_black
    if piece.kolor == 'black':
        x_aside = 33 + pom_x_black
        y_aside = -21
        y_aside += 4 * pom_black
        pom_black += 1
        piece.set_piece_aside(x_aside, y_aside)
        piece.board_position = '00'
        if pom_black == 7:
            pom_black = 0
            pom_x_black = 4
    elif piece.kolor == 'white':
        x_aside = -33 - pom_x_white
        y_aside = +21
        y_aside -= 4 * pom_white
        pom_white += 1
        piece.set_piece_aside(x_aside, y_aside)
        piece.board_position = '00'
        if pom_white == 7:
            pom_white = 0
            pom_x_white = 4
app.run()
