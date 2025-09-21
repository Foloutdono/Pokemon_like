import pygame

class InputHandlerOverworld:
    actions = {
        "moves_pressed": False,
        "sprint": False,
        "quit": False,
    }
    last_move = False
    last_direction = 'down'

    @classmethod
    def process_input(cls):
        for action in cls.actions:
            cls.actions[action] = False
            
        cls.actions["moves_pressed"] = []
        keys = pygame.key.get_pressed()

        if keys[pygame.K_z]:
            cls.actions["moves_pressed"].append("up")
        if keys[pygame.K_s]: 
            cls.actions["moves_pressed"].append("down")
        if keys[pygame.K_q]: 
            cls.actions["moves_pressed"].append("left")
        if keys[pygame.K_d]: 
            cls.actions["moves_pressed"].append("right")

        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            cls.actions["sprint"] = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                cls.actions["quit"] = True

        return cls.actions
    