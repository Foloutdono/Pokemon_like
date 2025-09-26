import pygame
from controller.overworld import OverworldState
from view.guis.gui_menu import GuiMenu

class MenuState:
    def __init__(self, screen, state_manager):
        self.state_manager = state_manager
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 40)
        self.gui = GuiMenu(screen)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state_manager.game.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.state_manager.change(OverworldState(self.screen, self.state_manager, "parde_village", "house_1_chamber"))

    def update(self, dt):
        pass

    def render(self, dt):
        self.gui.render(dt)