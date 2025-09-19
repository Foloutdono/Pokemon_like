import pygame

class InputHandlerOverworld:
    actions = {
        "move": False,
        "sprint": False,
        "quit": False,
    }
    last_move = False
    last_direction = "down"

    @classmethod
    def process_input(cls):
        for action in cls.actions:
            cls.actions[action] = False

        keys = pygame.key.get_pressed()

        moves_pressed = []

        if keys[pygame.K_z]:
            moves_pressed.append("up")
        if keys[pygame.K_s]: 
            moves_pressed.append("down")
        if keys[pygame.K_q]: 
            moves_pressed.append("left")
        if keys[pygame.K_d]: 
            moves_pressed.append("right")
    
        if moves_pressed:
            if cls.last_move in moves_pressed:
                cls.actions["move"] = cls.last_move
            else:
                cls.actions["move"] = moves_pressed[0]
                cls.last_direction = cls.actions["move"]
        cls.last_move = cls.actions["move"]

        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            cls.actions["sprint"] = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                cls.actions["quit"] = True

        return cls.actions