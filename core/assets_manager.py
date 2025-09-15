import pygame
from pytmx.util_pygame import load_pygame

class AssetManager:
    images = {}
    sounds = {}
    current_map = None

    @classmethod
    def load_image(cls, path):
        if path not in cls.images:
            cls.images[path] = pygame.image.load(path).convert_alpha()
        return cls.images[path]

    @classmethod
    def unload_image(cls, path):
        if path in cls.images:
            del cls.images[path]

    @classmethod
    def load_map(cls, path):
        cls.current_map = load_pygame(path)
    
    @classmethod
    def unload_map(cls):
        if cls.current_map:
            cls.current_map = None

    @classmethod
    def get_current_map(cls):
        return cls.current_map

    @classmethod
    def unload_state_assets(cls, state):
        for path in state.assets_needed:
            cls.unload_image(path)
