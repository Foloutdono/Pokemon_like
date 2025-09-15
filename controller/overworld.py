import pygame
import pytmx
from pytmx.util_pygame import load_pygame
from model.player import Player
from view.guis.gui_overworld import GUIOverwold
from core.assets_manager import AssetManager
from core import settings
from controller.input_handler import InputHandlerOverworld

ZOOM = 7

class OverworldState:
    def __init__(self, screen, state_manager, map_name):
        self.current_map_name = map_name
        self.gui = GUIOverwold(screen, state_manager)
        self.state_manager = state_manager

        self.player = Player()

        self.load_map(self.current_map_name)

    def load_map(self, map_name):
        AssetManager.load_map(f'{settings.MAPS_FOLDER_PATH}/forest/{map_name}.tmx')
        self.load_collisions()

    def load_collisions(self):
        self.collision_rects = []

        for layer in AssetManager.current_map.visible_layers:
            if not isinstance(layer, pytmx.TiledTileLayer):
                for obj in layer:
                    rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                    self.collision_rects.append(rect)

    def handle_events(self):
        InputHandlerOverworld.process_input()
        if (InputHandlerOverworld.actions["quit"]):
            self.state_manager.game.running = False
        self.player.move_player(InputHandlerOverworld.actions)

    @property
    def is_moving(self):
        return InputHandlerOverworld.actions is not None
    
    @property
    def direction(self):
        return InputHandlerOverworld.last_direction

    def update(self, dt):
        pass
    
    def render(self):
        self.gui.render()