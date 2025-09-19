import pygame
from controller.overworld import OverworldState

class MenuState:
    def __init__(self, screen, state_manager):
        self.state_manager = state_manager
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 40)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state_manager.game.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.state_manager.change(OverworldState(self.screen, self.state_manager, "Parde_village"))

    def update(self, dt):
        pass

    def render(self, dt):
        self.screen.fill((0, 0, 0))
        text = self.font.render("Pokemon Like - Press Enter", True, (255, 255, 255))
        self.screen.blit(text, (200, 250))