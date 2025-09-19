import pygame
from core.state_manager import StateManager
from controller.menu import MenuState
from core import settings

class Game:
    def __init__(self):
        info = pygame.display.Info()
        self.screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.NOFRAME)
        pygame.display.set_caption("Pokemon Like")
        self.clock = pygame.time.Clock()
        self.running = True

        # Gestion des états
        self.state_manager = StateManager(self)
        self.state_manager.change(MenuState(self.screen, self.state_manager))

    def run(self):
        while self.running:
            dt = self.clock.tick(settings.FPS)
            self.state_manager.handle_events()
            self.state_manager.update(dt)
            self.state_manager.render(dt)
            pygame.display.flip()
