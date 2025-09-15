import pygame
import pytmx
from view.player_sprite import PlayerSprite
from core.assets_manager import AssetManager

ZOOM=7

class GUIOverwold:
    def __init__(self, screen, state_manager):
        self.screen = screen
        self.state_manager = state_manager

        self.player_sprite = PlayerSprite("assets/characters/player/player.json", "assets/characters/player/player.png", (100, 100))
        self.sprites = pygame.sprite.Group(self.player_sprite)

    def render(self):
        current_map = AssetManager.get_current_map()
        current_state = self.state_manager.current_state

        map_width = current_map.width * current_map.tilewidth
        map_height = current_map.height * current_map.tileheight

        map_surface = pygame.Surface((map_width, map_height))

        for layer in current_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = current_map.get_tile_image_by_gid(gid)
                    if tile:
                        map_surface.blit(tile, (x * current_map.tilewidth, y * current_map.tileheight))

        screen_w, screen_h = self.screen.get_size()

        # --- CAMERA ---
        view_w = min(screen_w // ZOOM, map_width)
        view_h = min(screen_h // ZOOM, map_height)

        cam_x = current_state.player.centerx - view_w // 2
        cam_y = current_state.player.centery - view_h // 2

        cam_x = max(0, min(cam_x, map_width - view_w))
        cam_y = max(0, min(cam_y, map_height - view_h))

        # --- MAP RENDER ---
        sub_surface = map_surface.subsurface((cam_x, cam_y, view_w, view_h))
        scaled_surface = pygame.transform.scale(sub_surface, (screen_w, screen_h))
        self.screen.blit(scaled_surface, (0, 0))

        # --- PLAYER RENDER ---
        # Update sprite current_state
        self.player_sprite.pos = current_state.player.pos
        self.player_sprite.moving = current_state.is_moving
        self.player_sprite.direction = current_state.direction
        self.player_sprite.update(10)

        # Which animation to play (example)
        if current_state.is_moving:
            self.player_sprite.play(f"walk_{current_state.direction}")
        else:
            self.player_sprite.play(f"idle_{current_state.direction}")

        # Scale the current frame
        scaled_player = pygame.transform.scale(
            self.player_sprite.image,
            (self.player_sprite.rect.width * ZOOM, self.player_sprite.rect.height * ZOOM)
        )

        # Draw relative to camera
        player_screen_x = (current_state.player.rect.x - cam_x) * ZOOM
        player_screen_y = (current_state.player.rect.y - cam_y) * ZOOM
        self.screen.blit(scaled_player, (player_screen_x, player_screen_y))

        pygame.display.flip()
