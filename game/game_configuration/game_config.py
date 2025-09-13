from tkinter.ttk import *
from tkinter import *
from .game_config_const import *
from main_const import POKE_TYPE_RES_PATH
from utils import Utils
from ..poke.poke_type import PokeType
import json

class GameConfig():
    def __init__(self, window):
        self.window = window
        Utils.set_up_window(self.window, WINDOW_TITLE, WINDOW_GEOMETRY, WINDOW_IS_CENTERED)
        Utils.destroy_widget_children(self.window)

        self.load_poke_types()

        self.render_config()

        with open('assets\datas\pokemons.json', 'r') as f:
            data = json.load(f)
            for creature in data:
                print(creature)          # affiche tout l'objet
                print(creature["name"])  # affiche juste le nom
                print(creature["pv"])    # affiche les PV

    def render_config(self):
        self.window.grid_rowconfigure(list(range(WINDOW_ROWS)), weight=1)
        self.window.grid_columnconfigure(list(range(WINDOW_COLUMNS)), weight=1)

    def load_poke_types(self):
        poke_types_csv = Utils.read_csv(POKE_TYPE_RES_PATH, sep=";")
        poke_types_csv.pop(0)
        poke_types = []
        for iType in range(len(poke_types_csv)):
            poke_types.append(PokeType(poke_types_csv[iType].pop(0), iType, poke_types_csv[iType]))
        