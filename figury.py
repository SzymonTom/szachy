from ursina import *
import chess
from chess import *
from ursina.shaders import basic_lighting_shader, unlit_shader
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
            'black': 'Dark_Mahony.jpg'
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
        self.is_hovered = False
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
        """
        Sprawdza, czy figura została kliknięta.
        """
        if mouse.hovered_entity == self:
            # Zmiana koloru figury na żółty po kliknięciu
            self.highlight.color = color.yellow
            self.highlight.alpha = 0.5
            self.was_clicked = True
            return self.board_position
        else:
            # Przywrócenie oryginalnego koloru po kliknięciu poza figurę
            self.highlight.color = color.white
            self.highlight.alpha = 0
            self.was_clicked = False
    def update_position(self, new_board_position: str):
        """
        Aktualizuje pozycję na planszy bez ponownego wywoływania __init__.
        """
        self.board_position = new_board_position
        self.position = self._board_to_world(new_board_position)


    def set_piece_aside(self, x_aside: int, y_aside: int):
        self.position = Vec3(x_aside, -1.5, y_aside)


    def get_kolor(self):
        return self.kolor


    def update(self):
        self.hovered_piece()        




class LegalMove(Entity):
    def __init__(self, board_position: str):
        self.board_position = board_position
        super().__init__(
            model='cube',
            color=color.green,
            position=self._board_to_world(board_position),
            scale_x=6,
            scale_y=0.1,
            scale_z=6,
            collider='box',
            alpha=0.5,
            shader = unlit_shader,
        )
    def _board_to_world(self,position: str) -> Vec3:
        """
        Konwertuje pozycję szachową (np. 'e4') na współrzędne 3D.
        """
        if position[0] not in 'abcdefgh' or position[1] not in '12345678':
            raise ValueError("Invalid chess position")
        x = -21+6*(ord(position[0]) - ord('a'))
        y = -21+6*(int(position[1]) - 1)
        return Vec3(x+0.115, -4.7, y-0.045)  # Centruje planszę na (0,0,0)
    def clicked_piece(self):    
        if mouse.hovered_entity == self:
            return self.board_position


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
