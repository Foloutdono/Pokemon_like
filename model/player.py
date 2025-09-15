import pygame

class Player:
    def __init__(self, name="Red"):
        self.name = name
        self.team = []
        self.inventory = []
        self.rect = pygame.Rect(100, 100, 8, 16)
        self.is_moving = False
        self.direction = 'down'
        self.base_speed = 2
        self.sprint_multiplier = 1.8

    def move_player(self, actions) -> pygame.Rect:
        dx, dy = 0, 0
        if actions["move"] == "up": dy -= 1
        elif actions["move"] == "down": dy += 1
        elif actions["move"] == "left": dx -= 1
        elif actions["move"] == "right": dx += 1

        speed = self.base_speed
        if actions["sprint"]:
            speed *= self.sprint_multiplier
        
        self.rect.x += dx * speed
        self.rect.y += dy * speed
    
    @property
    def centerx(self):
        return self.rect.centerx
    
    @property
    def centery(self):
        return self.rect.centery
    
    @property
    def pos(self):
        return self.rect.x, self.rect.y