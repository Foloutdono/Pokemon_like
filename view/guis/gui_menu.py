import pygame

class GuiMenu:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_title = pygame.font.SysFont("arialblack", 90, bold=True)
        self.font_sub = pygame.font.SysFont("arial", 45, bold=True)
        self.font_press = pygame.font.SysFont("arial", 28)

        self.yellow = (255, 210, 50)
        self.blue = (30, 90, 180)
        self.black = (30, 30, 30)

        self.bg_color = (240, 240, 240)

        self.show_press_text = True
        self.blink_timer = 0

    def draw_text(self, text, font, color, x, y, outline_color=None, outline_size=3, center=True):
        """Affiche un texte avec éventuellement un contour (outline)"""
        if outline_color:
            for dx in range(-outline_size, outline_size + 1):
                for dy in range(-outline_size, outline_size + 1):
                    if dx != 0 or dy != 0:
                        outline_surface = font.render(text, True, outline_color)
                        rect = outline_surface.get_rect(center=(x + dx, y + dy) if center else (x + dx, y + dy))
                        self.screen.blit(outline_surface, rect)

        text_surface = font.render(text, True, color)
        rect = text_surface.get_rect(center=(x, y) if center else (x, y))
        self.screen.blit(text_surface, rect)

    def render(self, dt):
        # Fond
        self.screen.fill(self.bg_color)

        # Texte principal : "Pokemon Like"
        self.draw_text("POKEMON LIKE", self.font_title, self.yellow,
                        self.screen.get_width() // 2, self.screen.get_height() // 3,
                        outline_color=self.blue, outline_size=5)

        # Sous-titre : "Version Ultra Blanche"
        self.draw_text("Version", self.font_sub, self.black,
                        self.screen.get_width() // 2, self.screen.get_height() // 2)
        
        self.draw_text("Ultra Blanche", self.font_sub, self.black,
                        self.screen.get_width() // 2, (self.screen.get_height() // 2) + 60)

        # Texte clignotant : "Appuyez sur Entrée"
        self.blink_timer += dt
        if self.blink_timer >= 500:  # clignote toutes les 0.5 secondes
            self.show_press_text = not self.show_press_text
            self.blink_timer = 0

        if self.show_press_text:
            self.draw_text("Appuyez sur Entrée", self.font_press, self.black,
                            self.screen.get_width() // 2, self.screen.get_height() * 3 // 4)
            
        pygame.display.flip()