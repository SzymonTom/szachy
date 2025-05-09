from ursina import *

class ChessPiece(Entity):
    is_hovered = False
    def __init__(self, piece_type: str, color: str, position: str):
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
        obrot=180 if color == 'white' else 0
        super().__init__(
            model=self.piece_types[piece_type],
            texture=self.piece_colors[color],
            position=world_position,
            scale=1.0,
            rotation=(0, obrot, 0),
            collider = 'box',
            #shader=basic_lighting_shader,
            #origin_y=-0.5  # Ustawienie na "podłodze"
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
        self.rotate_piece()


class Rook(ChessPiece):
    def __init__(self, color: str, position: str):
        super().__init__('rook', color, position)
        #self.has_moved = False  # Flaga do sprawdzania, czy wieża się poruszała
class Knight(ChessPiece):
    def __init__(self, color: str, position: str):
        super().__init__('knight', color, position)
class Bishop(ChessPiece):   
    def __init__(self, color: str, position: str):
        super().__init__('bishop', color, position)
class Queen(ChessPiece):
    def __init__(self, color: str, position: str):
        super().__init__('queen', color, position)
class King(ChessPiece):
    def __init__(self, color: str, position: str):
        super().__init__('king', color, position)
class Pawn(ChessPiece):
    def __init__(self, color: str, position: str):
        super().__init__('pawn', color, position)
