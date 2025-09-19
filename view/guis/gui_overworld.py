import pygame
import pytmx
from view.player_sprite import PlayerSprite
from core.assets_manager import AssetManager

ZOOM=5

class GUIOverwold:
    def __init__(self, screen, state_manager):
        self.screen = screen
        self.state_manager = state_manager

        self.player_sprite = PlayerSprite("assets/characters/player/player.json", "assets/characters/player/player.png", (64, 64))
        self.sprites = pygame.sprite.Group(self.player_sprite)

    def render(self, dt):
        current_map = AssetManager.get_current_map()
        current_state = self.state_manager.current_state

        map_width = current_map.width * current_map.tilewidth
        map_height = current_map.height * current_map.tileheight
        screen_w, screen_h = self.screen.get_size()

        # --- CAMERA ---
        view_w = min(screen_w // ZOOM, map_width)
        view_h = min(screen_h // ZOOM, map_height)

        cam_x = current_state.player.centerx - view_w // 2
        cam_y = current_state.player.centery - view_h // 2
        cam_x = max(0, min(cam_x, map_width - view_w))
        cam_y = max(0, min(cam_y, map_height - view_h))

        # --- PLAYER RENDER ---
        self.player_sprite.pos = current_state.player.pos
        self.player_sprite.play(current_state.current_movement)
        self.player_sprite.update(dt)

        # Split player into body and head/hair
        player_img = self.player_sprite.image
        player_h = player_img.get_height()
        split_h = player_h * 1 / 2  # e.g., top 1/3 is head/hair
        player_head_img = player_img.subsurface((0, 0, player_img.get_width(), split_h))
        player_body_img = player_img.subsurface((0, split_h, player_img.get_width(), split_h))

        # Scale
        scaled_body = pygame.transform.scale(player_body_img, (player_body_img.get_width() * ZOOM, player_body_img.get_height() * ZOOM))
        scaled_head = pygame.transform.scale(player_head_img, (player_head_img.get_width() * ZOOM, player_head_img.get_height() * ZOOM))

        player_screen_x = (current_state.player.rect.x - cam_x) * ZOOM
        player_screen_y = (current_state.player.rect.y - cam_y) * ZOOM

        player_collision_rect = current_state.player.collision_rect(current_state.player.rect.x, current_state.player.rect.y)

        # --- TERRAIN ---
        terrain_surface = pygame.Surface((map_width, map_height), pygame.SRCALPHA)
        decorations_surface = pygame.Surface((map_width, map_height), pygame.SRCALPHA)

        for layer in current_map.visible_layers:
            if layer.name == "terrains":
                for x, y, gid in layer:
                    tile = current_map.get_tile_image_by_gid(gid)
                    if tile:
                        terrain_surface.blit(tile, (x * current_map.tilewidth, y * current_map.tileheight))

            elif layer.name == "tall_grass":
                for obj in layer:
                    if obj.gid:
                        tile = current_map.get_tile_image_by_gid(obj.gid)
                        if not tile:
                            continue

                        tile_rect = pygame.Rect(obj.x, obj.y, current_map.tilewidth, current_map.tileheight)

                        if player_collision_rect.colliderect(tile_rect) and not current_state.player.moving:
                            tile_h = tile.get_height()

                            bottom = tile.subsurface((0, 0, tile.get_width(), tile_h // 2))
                            top = tile.subsurface((0, tile_h // 2, tile.get_width(), tile_h // 2))

                            terrain_surface.blit(bottom, (obj.x, obj.y))
                            decorations_surface.blit(top, (obj.x, obj.y + tile_h // 2))
                        else:
                            terrain_surface.blit(tile, (obj.x, obj.y))

        for layer in current_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer) and layer.name != "terrains":
                for x, y, gid in layer:
                    tile = current_map.get_tile_image_by_gid(gid)
                    if tile:
                        decorations_surface.blit(tile, (x * current_map.tilewidth, y * current_map.tileheight))

        # --- CAMERA CUT ---
        terrain_view = terrain_surface.subsurface((cam_x, cam_y, view_w, view_h))
        decorations_view = decorations_surface.subsurface((cam_x, cam_y, view_w, view_h))

        terrain_scaled = pygame.transform.scale(terrain_view, (screen_w, screen_h))
        decorations_scaled = pygame.transform.scale(decorations_view, (screen_w, screen_h))

        # --- RENDER ORDER ---
        self.screen.blit(terrain_scaled, (0, 0))       # terrain + bottom grass
        self.screen.blit(scaled_body, (player_screen_x, player_screen_y + split_h * ZOOM))  # player body
        self.screen.blit(decorations_scaled, (0, 0))   # decorations + top grass
        self.screen.blit(scaled_head, (player_screen_x, player_screen_y))  # player head/hair
