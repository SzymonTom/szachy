from ursina import *

class ChessPiece(Entity):
    is_hovered = False
    def __init__(self, piece_type: str, kolor: str, position: str):
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
            'queen': 'models/krolowa.obj',
            'king': 'models/krol.obj',
            'pawn': 'models/pionek.obj',
        }
        world_position = self._board_to_world(position)
        obrot=180 if kolor == 'white' else 0
        super().__init__(
            model=self.piece_types[piece_type],
            texture=self.piece_colors[kolor],
            position=world_position,
            scale=1.0,
            rotation=(0, obrot, 0),
            #collider=self.piece_types[piece_type],
            collider = 'box'
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
    def _board_to_world(self,position: str) -> Vec3:
        """
        Konwertuje pozycję szachową (np. 'e4') na współrzędne 3D.
        """
        if position[0] not in 'abcdefgh' or position[1] not in '12345678':
            raise ValueError("Invalid chess position")
        x = -21+6*(ord(position[0]) - ord('a'))
        y = -21+6*(int(position[1]) - 1)
        return Vec3(x, 0, y)  # Centruje planszę na (0,0,0)
    def highlight_piece(self):
        """
        Sprawdza, czy myszka znajduje się nad figurą, i podświetla ją.
        """
        if mouse.hovered_entity == self:
            self.highlight.alpha = 0.5  # Show highlight
        else:
            self.highlight.alpha = 0  # Hide highlight
    

    def raise_figure(self):
        if self.hovered and self.is_hovered == False:
            print(self.name)
            self.position += self.up
            self.is_hovered = True
        if self.is_hovered and self.hovered == False:
            self.position += self.down
            self.is_hovered = False
    

    def update(self):
        self.raise_figure()
        self.highlight_piece()


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
