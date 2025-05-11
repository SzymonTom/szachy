# Create chess pieces
from ursina import *
from figury import *
from board import *
import chess
app = Ursina()
DirectionalLight(position=(1, 1, 3), shadows=True, kolor=color.white)
EditorCamera()
pieces = load_pieces()
board_loaded = load_board()
board = chess.Board()
# Lista przechowująca wszystkie podświetlenia
podswietl_entities = []
# Globalna zmienna do przechowywania zaznaczonej figury
pom_black = 0
pom_white = 0
pom_x_white = 0
pom_x_black = 0
#global clicked_piece_position
clicked_piece = None
end = True
def update():
    global clicked_piece
    global end
    if mouse.left and not board.is_game_over():    
        move_position = None
        for podswietlenie in podswietl_entities:
            if podswietlenie.clicked_square() is not None and clicked_piece is not None:
                move_position = podswietlenie.clicked_square()
                destroy_position = is_capture(clicked_piece, move_position)
                castling_position,castle_from = is_castle(clicked_piece.board_position, move_position)
        for piece in pieces:
            if move_position is not None:
                if piece.was_clicked:
                    promotion_piece = ""
                    if is_promotion(piece, move_position):
                        PromotionButtons(piece)
                        
                        if piece.kolor == 'white':
                            promotion_piece = get_piece_type(piece)    
                        else: 
                            promotion_piece = get_piece_type(piece).upper()
                    move_piece(piece, move_position,promotion_piece)
                elif piece.board_position == destroy_position:
                    capture_piece(piece)
                elif piece.board_position == castle_from:
                    piece.update_position(castling_position)
            position=piece.clicked_piece()
            clicked_piece = piece if position is not None else clicked_piece
            highlight_squares(position)
    elif board.is_game_over():
        if end:
            game_over()
            end = False

        
def is_promotion(piece, move_position):
    print("sprawdzam")
    if piece.piece_type == 'pawn':
        if piece.kolor == 'white' and move_position[1] == '8':
            print("White promotion")
            return True
        elif piece.kolor == 'black' and move_position[1] == '1':
            print("Black promotion")
            return True
    return False

def move_piece(piece, move_position,promotion_piece):
    print(piece.piece_type)
    board.push(chess.Move.from_uci(piece.board_position+move_position+promotion_piece))
    piece.update_position(move_position)
    piece.un_klik()
    piece.zaznaczony_pion = None
    piece.was_clicked = False
    clear_highlight()

def get_piece_type(piece):
    return 'q' if piece.piece_type == 'queen' else \
           'r' if piece.piece_type == 'rook' else \
           'b' if piece.piece_type == 'bishop' else \
           'n' if piece.piece_type == 'knight' else ""
def game_over():
            result = board.outcome()
            if board.is_checkmate():
                reason = "Checkmate!"
            elif board.is_stalemate():
                reason = "Stalemate!"
            elif board.is_insufficient_material():
                reason = "Insufficient material!"
            elif board.is_seventyfive_moves():
                reason = "75-move rule!"
            elif board.is_fivefold_repetition():
                reason = "Fivefold repetition!"
            winner = "White wins!" if result == "1-0" else "Black wins!" if result == "0-1" else "Draw!"
            # Display winner and reason
            text_entity = Text(
                text=f"{winner}\n{reason}",
                parent=camera.ui,
                origin=(0, 0),
                scale=2,
                color=color.white,
                position=(0, 0)
            )

def clear_highlight():
    
    global podswietl_entities
    for entity in podswietl_entities:
        destroy(entity)
    podswietl_entities = []


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

def is_capture(clicked_piece, move_position):
    """
    Funkcja do sprawdzania czy ruch jest biciem.
    """
    if board.is_en_passant(chess.Move.from_uci(clicked_piece.board_position+move_position)):
        destroy_position = move_position[0] + str(int(move_position[1]) - 1) if clicked_piece.kolor == 'white' else move_position[0] + str(int(move_position[1]) + 1)
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
