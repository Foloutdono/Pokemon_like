import pygame

class Player:
    def __init__(self, state_manager, name="Red"):
        self.state_manager = state_manager
        self.name = name
        self.team = []
        self.inventory = []

        self.x = 128.0
        self.y = 64.0
        self.rect = pygame.Rect(128, 64, 16, 16)
        self.offsety = 16

        self.moving = False
        self.target_x = self.x
        self.target_y = self.y

        self.move = None
        self.is_sprinting = False
        self.last_move = 'down'

        self.base_speed = 0.6
        self.sprint_multiplier = 1.5

        self.current_encounter_zone = None

    def move_player(self, actions, dt):
        tile_size = 16

        if not self.moving:
            if actions["moves_pressed"]:
                if self.last_move in actions["moves_pressed"]:
                    self.move = self.last_move
                else:
                    self.move = actions["moves_pressed"][0]
                    self.last_move = self.move
            else:
                self.move = None

            state = self.state_manager.current_state

            if self.move and self.move == self.last_move:      
                new_y = self.y + tile_size * (1 if self.move == "down" else (-1 if self.move == "up" else 0))
                new_x = self.x + tile_size * (1 if self.move == "right" else (-1 if self.move == "left" else 0))
                if not self.check_collision(state.collisions, new_x, new_y):
                    self.target_y = new_y
                    self.target_x = new_x
                    self.moving = True
                else:
                    collision_rect = self.collision_rect(self.x, self.y)
                    iDoor = 0
                    while(iDoor < len(state.doors) and not (collision_rect.colliderect(state.doors[iDoor]["rect"]) and self.move == state.doors[iDoor]["entry_direction"])):
                        iDoor += 1
                    if iDoor < len(state.doors):
                        destination_door = state.doors[iDoor]["destination_door"]
                        from_direction = state.doors[iDoor]["entry_direction"]
                        state.load_map(state.doors[iDoor]["destination_map"])
                        iDoor = 0
                        while(iDoor < len(state.doors) and not state.doors[iDoor]["number"] == destination_door):
                            iDoor += 1
                        if iDoor < len(state.doors):
                            door = state.doors[iDoor]
                            target_y = door["rect"].y - tile_size * (1 if from_direction == "down" or from_direction == "up" else  0)
                            target_x = door["rect"].x - tile_size * (1 if from_direction == "right" or from_direction == "left"else 0)
                            new_x = target_x
                            new_y = target_y
                            self.target_y = target_y
                            self.target_x = target_x
                            self.moving = True
                            match door["entry_direction"]:
                                case "down":
                                    new_y += tile_size
                                    exit_direction = 'up'
                                case "up":
                                    new_y -= tile_size
                                    exit_direction = 'down'
                                case "right":
                                    new_x += tile_size
                                    exit_direction = 'left'
                                case "left":
                                    new_x -= tile_size
                                    exit_direction = 'right'
                            self.update_coordonates(new_x, new_y)
                            self.move = exit_direction
                            self.last_move = exit_direction
                self.is_sprinting = actions["sprint"]

        if self.moving:
            dx = self.target_x - self.x
            dy = self.target_y - self.y

            dist = (dx**2 + dy**2) ** 0.5

            if dist == 0:
                self.moving = False
            else:
                speed = self.base_speed
                if self.is_sprinting:
                    speed *= self.sprint_multiplier

                # Step = how much we can move this frame (scaled by dt)
                step = speed * dt / 10

                if step >= dist:
                    new_x, new_y = self.target_x, self.target_y
                    self.moving = False
                else:
                    new_x = self.x + (dx / dist) * step
                    new_y = self.y + (dy / dist) * step

                self.update_coordonates(new_x, new_y)

            self.encounter_detection()

    def update_coordonates(self, x, y):
        self.x = x
        self.y = y
        self.rect.topleft = (round(self.x), round(self.y))

    def encounter_detection(self):
        state = self.state_manager.current_state
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

    def door_detection(self):
        pass

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