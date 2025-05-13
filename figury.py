from ursina import *
import chess
from chess import *
from ursina.shaders import basic_lighting_shader, unlit_shader

zaznaczony_pion = None

class ChessPiece(Entity):


    def __init__(self, piece_type: str, kolor: str, board_position: str):
        """
        Inicjalizuje figurę szachową.

        :param piece_type: Typ figury ('rook', 'knight', 'bishop', 'queen', 'king', 'pawn')
        :param color: Kolor figury ('white' lub 'black')
        :param position: Pozycja na planszy (np. 'e4')
        """
        self.piece_colors = {
            'white': 'Sapeli.jpg',
            'black': 'ciemny1.jpg'
        }
        self.piece_types = {
            'rook': 'models/wieza.obj',
            'knight': 'models/kon.obj',
            'bishop': 'models/goniec.obj',
            'queen': 'models/krol.obj',
            'king': 'models/krolowa.obj',
            'pawn': 'models/pionek.obj',
        }
        self.board_position = board_position
        self.kolor = kolor
        self.piece_type = piece_type
        self.promotion_clicked = False
        world_position = self._board_to_world(board_position)
        obrot=180 if kolor == 'white' else 0
        super().__init__(
            model=self.piece_types[piece_type],
            texture=self.piece_colors[kolor],
            position=world_position,
            scale=1.0,
            rotation=(0, obrot, 0),
            collider=self.piece_types[piece_type],
            #shader=basic_lighting_shader,
            #origin_y=-0.5  # Ustawienie na "podłodze"
        )
        self.highlight = Entity(
            parent=self,
            model=self.piece_types[piece_type],
            color=color.white,
            scale=1,
            alpha=0,
            always_on_top=True
        )
        self.was_clicked = False
        self.on_click = self.klik

    def promote(self, type: str):
        self.piece_type = type
        model = self.piece_types[type]
        self.model = model
        self.highlight.model = model
        self.collider = model
        self.promotion_clicked = True
    def _board_to_world(self,board_position: str) -> Vec3:
        """
        Konwertuje pozycję szachową (np. 'e4') na współrzędne 3D.
        """
        if board_position[0] not in 'abcdefgh' or board_position[1] not in '12345678':
            raise ValueError("Invalid chess position")
        x = -21+6*(ord(board_position[0]) - ord('a'))
        y = -21+6*(int(board_position[1]) - 1)
        return Vec3(x, 0, y)  # Centruje planszę na (0,0,0)
    

    def hovered_piece(self):
        """
        Sprawdza, czy myszka znajduje się nad figurą, i podświetla ją.
        """
        if mouse.hovered_entity == self:
            self.highlight.alpha = 0.5  # Show highlight
        elif not self.was_clicked:
            self.highlight.alpha = 0  # Hide highlight


    def clicked_piece(self):
        if mouse.hovered_entity == self:
            return self.board_position
    

    def klik(self):
        global zaznaczony_pion

        if zaznaczony_pion and zaznaczony_pion != self:
            zaznaczony_pion.un_klik()

        self.highlight.color = color.yellow
        self.highlight.alpha = 0.5
        self.was_clicked = True
        zaznaczony_pion = self


    def un_klik(self):
        self.was_clicked = False
        self.highlight.color = color.white
        self.highlight.alpha = 0
    

    def pobierz_zaznaczony_pion(self):
        return zaznaczony_pion


    def update_position(self, new_board_position: str):
        """
        Aktualizuje pozycję na planszy bez ponownego wywoływania __init__.
        """
        self.board_position = new_board_position
        self.position = self._board_to_world(new_board_position)


    def set_piece_aside(self, x_aside: int, y_aside: int):
        self.position = Vec3(x_aside, -1.5, y_aside)

    
    def is_clicked(self):
        return self.was_clicked


    def get_kolor(self):
        return self.kolor


    def update(self):
        self.hovered_piece()
        if self.board_position == '00':
            self.collider = None
        if mouse.left and not mouse.hovered_entity ==self:
            self.un_klik()
        


class PromotionButtons(Entity):
    
    def __init__(self, piece: ChessPiece, **kwargs):
        
        super().__init__(parent=camera.ui, **kwargs)  # Poprawione parent=self
    
        
        # Tło menu promocji
        self.background = Entity(
            parent=self,
            model='quad',
            color=color.dark_gray,
            scale=(0.5, 1.2),
            z=0.1
        )
        
        self.title = Text(
            parent=self,
            text="Choose promotion",
            origin=(0, 0),
            y=0.3,
            scale=2,  # Zmniejszona skala
            color=color.white
        )

        self.Queen_button = Button(
            parent=self,
            text="Queen",
            color=color.black,
            text_color=color.white,
            y=0,
            scale=(0.3, 0.1),
            on_click=lambda: self.promote(piece, 'queen')  # Dodany brakujący nawias
        )

        self.Rook_button = Button(
            parent=self,
            text="Rook",
            color=color.black,
            text_color=color.white,
            y=-0.15,
            scale=(0.3, 0.1),
            on_click=lambda: self.promote(piece, 'rook')  # Dodany brakujący nawias
        )

        self.Bishop_button = Button(
            parent=self,
            text="Bishop",
            color=color.black,
            text_color=color.white,
            y=-0.3,
            scale=(0.3, 0.1),
            on_click=lambda: self.promote(piece, 'bishop')  # Dodany brakujący nawias
        )

        self.Knight_button = Button(
            parent=self,
            text="Knight",
            color=color.black,
            text_color=color.white,
            y=-0.45,
            scale=(0.3, 0.1),
            on_click=lambda: self.promote(piece, 'knight')  # Dodany brakujący nawias
        )
    def promote(self,piece, type: str):
        # Tutaj dodaj logikę promocji pionka
        piece.promote(type)
        self.disable()  # Wyłącz menu promocji po kliknięciu


class Rook(ChessPiece):
    def __init__(self, kolor: str, position: str):
        super().__init__('rook', kolor, position)
        #self.has_moved = False  # Flaga do sprawdzania, czy wieża się poruszała
class Knight(ChessPiece):
    def __init__(self, kolor: str, position: str):
        super().__init__('knight', kolor, position)
class Bishop(ChessPiece):   
    def __init__(self, kolor: str, position: str):
        super().__init__('bishop', kolor, position)
class Queen(ChessPiece):
    def __init__(self, kolor: str, position: str):
        super().__init__('queen', kolor, position)
class King(ChessPiece):
    def __init__(self, kolor: str, position: str):
        super().__init__('king', kolor, position)
class Pawn(ChessPiece):
    def __init__(self, kolor: str, position: str):
        super().__init__('pawn', kolor, position)

def load_pieces():
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
    return pieces
