from ursina import *
from ursina.shaders import basic_lighting_shader, unlit_shader
def load_board():
    board_1 = Entity(
    model='jasna_rama.obj',
    texture='Sapeli.jpg',
    scale=1
    )
    board_2 = Entity(
    model='jasna_kratka.obj',
    texture='Sapeli.jpg',
    scale=1
    )
    board_3 = Entity(
    model='ciemna_rama.obj',
    texture='Dark_Mahony.jpg',
    scale=1
    )
    stol = Entity(
    model='stol.obj',
    texture='stol1.jpg',
    scale=2,
    position=(-30, -90, 20),
    )






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
    

    def clicked_square(self):    
        if mouse.hovered_entity == self:
            return self.board_position
