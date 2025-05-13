from ursina import *

class ChessGame:
    def __init__(self):
        self.player_color = 'white'  # domyślnie
        
    def start_game(self, player_color):
        self.player_color = player_color
        print(f"Rozpoczynam grę jako {player_color}")
        # Tutaj inicjalizacja planszy itd.

class MainMenu(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        
        
        # Elementy menu jak w poprzednich przykładach
        self.background = Entity(parent=self, model='quad', texture='white_cube', 
                               texture_scale=(1, 1), scale=(2, 1), color=color.dark_gray, z=1)
        
        self.title = Text(parent=self, text="Szachy", origin=(0, 0), y=0.3, 
                         scale=3, color=color.white)
        
        self.white_button = Button(parent=self, text="Graj jako białe", 
                                 color=color.white, text_color=color.black,
                                 y=0, scale=(0.3, 0.1), on_click=self.start_as_white)
        
        self.black_button = Button(parent=self, text="Graj jako czarne", 
                                 color=color.black, text_color=color.white,
                                 y=-0.15, scale=(0.3, 0.1), on_click=self.start_as_black)
        
        self.quit_button = Button(parent=self, text="Wyjdź", color=color.red,
                                y=-0.3, scale=(0.3, 0.1), on_click=application.quit)
    
    def start_as_white(self):
        self.disable()
        return 'white'
    
    def start_as_black(self):
        self.disable()
        return 'black'
    
    def show(self):
        self.enable()
