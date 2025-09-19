import pygame
import json

class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, json_path, image_path, position):
        super().__init__()
        self.position = position

        # Load JSON metadata
        with open(json_path) as f:
            self.data = json.load(f)

        # Load sprite sheet
        self.spritesheet = pygame.image.load(image_path).convert_alpha()

        # Build animations { "walk_down": [frames...], "sprint_up": [frames...] }
        self.animations = self.load_animations()

        # Default state
        self.current_animation = "walk_down"
        self.index = 0
        self.image = self.animations[self.current_animation][self.index]
        self.rect = self.image.get_rect(bottomleft=position)
        print(self.image.get_rect(bottomleft=position), self.image.get_rect(topleft=position))

        # Timing
        self.timer = 0
        self.frame_duration = 100 # ms per frame

    def load_animations(self):
        animations = {}
        frames = self.data["frames"]
        tags = self.data["meta"]["frameTags"]

        for tag in tags:
            name = tag["name"]
            start = tag["from"]
            end = tag["to"]

            animations[name] = []
            for i in range(start, end + 1):
                frame_data = frames[i]["frame"]
                rect = pygame.Rect(
                    frame_data["x"], frame_data["y"],
                    frame_data["w"], frame_data["h"]
                )
                image = self.spritesheet.subsurface(rect).copy()
                animations[name].append(image)

        return animations

    def play(self, animation_name):
        if self.current_animation != animation_name:
            self.current_animation = animation_name
            self.index = 0
            self.timer = 0
            self.image = self.animations[self.current_animation][self.index]

    def update(self, dt):
        self.timer += dt
        frames = self.animations[self.current_animation]
        frame_time = self.data["frames"][self.index]["duration"]

        if self.timer >= frame_time:
            self.timer = 0
            self.index = (self.index + 1) % len(frames)
            self.image = frames[self.index]