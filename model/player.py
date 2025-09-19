import pygame

class Player:
    def __init__(self, state_manager, name="Red"):
        self.state_manager = state_manager
        self.name = name
        self.team = []
        self.inventory = []

        self.x = 64.0
        self.y = 64.0
        self.rect = pygame.Rect(64, 64, 16, 16)
        self.offsety = 16

        self.moving = False
        self.target_x = self.x
        self.target_y = self.y


        self.base_speed = 0.8
        self.sprint_multiplier = 1.5

        self.current_encounter_zone = None

    def move_player(self, actions):
        tile_size = 16
        state = self.state_manager.current_state

        if not self.moving:
            if actions["move"] == "up":
                if not self.check_collision(state.collisions, self.x, self.y - tile_size):
                    self.target_y = self.y - tile_size
                    self.moving = True
            elif actions["move"] == "down":
                if not self.check_collision(state.collisions, self.x, self.y + tile_size):
                    self.target_y = self.y + tile_size
                    self.moving = True
            elif actions["move"] == "left":
                if not self.check_collision(state.collisions, self.x - tile_size, self.y):
                    self.target_x = self.x - tile_size
                    self.moving = True
            elif actions["move"] == "right":
                if not self.check_collision(state.collisions, self.x + tile_size, self.y):
                    self.target_x = self.x + tile_size
                    self.moving = True

        if self.moving:
            speed = self.base_speed
            if actions["sprint"]:
                speed *= self.sprint_multiplier

            dx = self.target_x - self.x
            dy = self.target_y - self.y

            dist = (dx**2 + dy**2) ** 0.5
            step = min(speed, dist)  # avoid overshooting

            if dist == 0:  # arrived
                self.moving = False
            else:
                self.x += dx / dist * step
                self.y += dy / dist * step

            self.rect.topleft = (round(self.x), round(self.y))

            collision_rect = self.collision_rect(self.x, self.y)
            is_in_encounter_zone = False
            iEncounterZone = 0
            while(not is_in_encounter_zone and iEncounterZone < len(state.tall_grass)):
                is_in_encounter_zone = collision_rect.colliderect(state.tall_grass[iEncounterZone])
                iEncounterZone += 1

            if is_in_encounter_zone:
                zone = state.tall_grass[iEncounterZone-1]
                if self.current_encounter_zone != zone:
                    self.current_encounter_zone = zone
                    encounter = state.try_encounter("parde_village")
                    if encounter:
                        print(encounter)
            else:
                self.current_encounter_zone = None

    def check_collision(self, collisions, x, y):
        test_rect = self.collision_rect(x, y)
        return any(test_rect.colliderect(c) for c in collisions)

    def collision_rect(self, x, y):
        collision_rect = self.rect.copy()
        collision_rect.topleft = (x, y + self.offsety)
        return collision_rect
    
    @property
    def centerx(self):
        return self.rect.centerx
    
    @property
    def centery(self):
        return self.rect.centery
    
    @property
    def pos(self):
        return self.rect.x, self.rect.y