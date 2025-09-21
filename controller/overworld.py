import pygame
import pytmx
import random
from pytmx.util_pygame import load_pygame
from model.player import Player
from view.guis.gui_overworld import GUIOverwold
from core.assets_manager import AssetManager
from core import settings
from controller.input_handler import InputHandlerOverworld

ZOOM = 7

ENCOUNTER_TABLES = {
    "parde_village": [
        {"species": "Zigzagoon", "level_range": (2, 3), "weight": 45},
        {"species": "Poochyena", "level_range": (2, 3), "weight": 45},
        {"species": "Wurmple",   "level_range": (2, 3), "weight": 10},
    ]
}

class OverworldState:
    def __init__(self, screen, state_manager, region, map_name):
        self.gui = GUIOverwold(screen, state_manager)

        self.region= region
        self.load_map(map_name)

        self.state_manager = state_manager

        self.player = Player(state_manager)

    def load_map(self, map_name):
        self.current_map_name = map_name
        self.current_region = self.region
        AssetManager.load_map(f'{settings.MAPS_FOLDER_PATH}/{self.region}/{map_name}.tmx')
        self.gui.update_map()
        self.load_collisions()

    def load_collisions(self):
        self.collisions = []
        self.tall_grass = []
        self.doors = []

        for layer in AssetManager.current_map.visible_layers:
            if layer.name == "collisions":
                for obj in layer:
                    rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                    self.collisions.append(rect)
            elif layer.name == "tall_grass":
                for obj in layer:
                        rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                        self.tall_grass.append(rect)
            elif layer.name == "doors":
                for obj in layer:
                        door = {}
                        door["rect"] = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                        door["destination_map"] = obj.properties["destination_map"]
                        door["destination_door"] = obj.properties["destination_door"]
                        door["number"] = obj.properties["number"]
                        door["entry_direction"] = obj.properties["entry_direction"]
                        self.doors.append(door)

    def handle_events(self):
        InputHandlerOverworld.process_input()
        if (InputHandlerOverworld.actions["quit"]):
            self.state_manager.game.running = False

    @property
    def current_movement(self):
        if self.player.move:
            if self.player.is_sprinting:
                current_movement = f'sprint_{self.player.move}'
            else:
                current_movement = f'walk_{self.player.move}'
        else:
            current_movement = f'idle_{self.player.last_move}'
        return current_movement
    
    @property
    def direction(self):
        return InputHandlerOverworld.last_direction
    
    def player_is_moving(self):
        return self.player.moving

    def update(self, dt):
        self.player.move_player(InputHandlerOverworld.actions, dt)
    
    def render(self, dt):
        self.gui.render(dt)

    def try_encounter(self, area: str, chance: float = 1/24):
        if random.random() < chance:
            return self.choose_pokemon(area)
        return None
    
    def choose_pokemon(self, area: str):
        table = ENCOUNTER_TABLES[area]
        
        total_weight = sum(entry["weight"] for entry in table)
        roll = random.uniform(0, total_weight)
        
        current = 0
        for entry in table:
            current += entry["weight"]
            if roll <= current:
                min_lv, max_lv = entry["level_range"]
                level = random.randint(min_lv, max_lv)
                return {"species": entry["species"], "level": level}