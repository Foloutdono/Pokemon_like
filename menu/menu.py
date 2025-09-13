"""
This module contains the Menu class.
"""
from tkinter.ttk import *
from tkinter import *
from utils import Utils
from main_const import *
from game.game_configuration.game_config import GameConfig
from .menu_const import *

class Menu(Tk):
    """
    A menu, inherit from the Tk class.
    """
    def __init__(self):
        """
        Create a menu object.
        """
        super().__init__()
        Utils.set_up_window(self, WINDOW_TITLE, WINDOW_GEOMETRY, WINDOW_IS_CENTERED)

        self.render_menu()

        self.mainloop()

    def render_menu(self):
        self.grid_rowconfigure(list(range(WINDOW_ROWS)), weight=1)
        self.grid_columnconfigure(list(range(WINDOW_COLUMNS)), weight=1)

        Label(self, text=GAME_TITLE.upper(), font=("Arial", 30, "bold")).grid(row=1, column=CENTERED_COLUMN, pady=(0, 150))
        Button(self, text='LAUNCH', font=("Arial", 20, "bold"), command=self.launch_game, padx=40, pady=20, bg='red', fg='white').grid(row=3, column=CENTERED_COLUMN)

    def launch_game(self):
        self.game_config()

    def game_config(self):
        GameConfig(self)