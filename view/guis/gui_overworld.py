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

        self.current_map = AssetManager.get_current_map()

    @property
    def map_width(self):
        return self.current_map.width * self.current_map.tilewidth
    
    @property
    def map_height(self):
        return self.current_map.height * self.current_map.tileheight
    
    @property
    def current_state(self):
        return self.state_manager.current_state
    
    def update_map(self):
        self.current_map = AssetManager.get_current_map()

    def render(self, dt):
        self.screen.fill((0, 0, 0))
        screen_w, screen_h = self.screen.get_size()

        # Sync sprite with logical player state
        self.player_sprite.pos = self.current_state.player.pos
        self.player_sprite.play(self.current_state.current_movement)
        self.player_sprite.update(dt)

        # Split player into body and head/hair
        player_img = self.player_sprite.image
        player_h = player_img.get_height()
        split_h = player_h * 1 / 2  # e.g., half = head, half = body
        player_head_img = player_img.subsurface((0, 0, player_img.get_width(), split_h))
        player_body_img = player_img.subsurface((0, split_h, player_img.get_width(), split_h))

        # Scale player pieces once
        scaled_body = pygame.transform.scale(
            player_body_img,
            (player_body_img.get_width() * ZOOM, player_body_img.get_height() * ZOOM)
        )
        scaled_head = pygame.transform.scale(
            player_head_img,
            (player_head_img.get_width() * ZOOM, player_head_img.get_height() * ZOOM)
        )

        # Load surfaces
        terrain_surface, decorations_surface = self.load_surfaces()

        # --- CAMERA FIXED FOR SMALL MAPS ---
        scaled_map_w = self.map_width * ZOOM
        scaled_map_h = self.map_height * ZOOM

        offset_x=0
        offset_y=0

        if scaled_map_w <= screen_w and scaled_map_h <= screen_h:
            # Case 1: Small map -> show the whole map centered
            terrain_scaled = pygame.transform.scale(terrain_surface, (scaled_map_w, scaled_map_h))
            decorations_scaled = pygame.transform.scale(decorations_surface, (scaled_map_w, scaled_map_h))

            offset_x = (screen_w - scaled_map_w) // 2
            offset_y = (screen_h - scaled_map_h) // 2

            # Round only when converting to screen coordinates
            player_screen_x = int(offset_x + self.current_state.player.pos[0] * ZOOM)
            player_screen_y = int(offset_y + self.current_state.player.pos[1] * ZOOM)
        else:
            # Case 2: Map is bigger than screen -> use camera
            view_w = min(screen_w // ZOOM, self.map_width)
            view_h = min(screen_h // ZOOM, self.map_height)

            px, py = self.current_state.player.pos  # world position floats
            cam_x = int(px + self.current_state.player.rect.width / 2 - view_w // 2)
            cam_y = int(py + self.current_state.player.rect.height / 2 - view_h // 2)

            cam_x = max(0, min(cam_x, self.map_width - view_w))
            cam_y = max(0, min(cam_y, self.map_height - view_h))

            terrain_view = terrain_surface.subsurface((cam_x, cam_y, view_w, view_h))
            decorations_view = decorations_surface.subsurface((cam_x, cam_y, view_w, view_h))

            terrain_scaled = pygame.transform.scale(terrain_view, (screen_w, screen_h))
            decorations_scaled = pygame.transform.scale(decorations_view, (screen_w, screen_h))

            # Round only at rendering
            player_screen_x = int((px - cam_x) * ZOOM)
            player_screen_y = int((py - cam_y) * ZOOM)

        self.screen.blit(terrain_scaled, (offset_x, offset_y))
        self.screen.blit(scaled_body, (player_screen_x, player_screen_y + int(split_h * ZOOM)))
        self.screen.blit(decorations_scaled, (offset_x, offset_y))
        self.screen.blit(scaled_head, (player_screen_x, player_screen_y))

    def load_surfaces(self):
        terrain_surface = pygame.Surface((self.map_width, self.map_height), pygame.SRCALPHA)
        decorations_surface = pygame.Surface((self.map_width, self.map_height), pygame.SRCALPHA)

        player_collision_rect = self.current_state.player.collision_rect(self.current_state.player.rect.x, self.current_state.player.rect.y)

        for layer in self.current_map.visible_layers:
            if layer.name == "terrains" or layer.name == "lights":
                for x, y, gid in layer:
                    tile = self.current_map.get_tile_image_by_gid(gid)
                    if tile:
                        terrain_surface.blit(tile, (x * self.current_map.tilewidth, y * self.current_map.tileheight))

            elif layer.name == "tall_grass":
                for obj in layer:
                    if obj.gid:
                        tile = self.current_map.get_tile_image_by_gid(obj.gid)
                        if not tile:
                            continue

                        tile_rect = pygame.Rect(obj.x, obj.y, self.current_map.tilewidth, self.current_map.tileheight)

                        if player_collision_rect.colliderect(tile_rect) and not self.current_state.player.moving:
                            tile_h = tile.get_height()

                            bottom = tile.subsurface((0, 0, tile.get_width(), tile_h // 2))
                            top = tile.subsurface((0, tile_h // 2, tile.get_width(), tile_h // 2))

                            terrain_surface.blit(bottom, (obj.x, obj.y))
                            decorations_surface.blit(top, (obj.x, obj.y + tile_h // 2))
                        else:
                            terrain_surface.blit(tile, (obj.x, obj.y))

        for layer in self.current_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer) and layer.name != "terrains" and layer.name != "lights":
                for x, y, gid in layer:
                    tile = self.current_map.get_tile_image_by_gid(gid)
                    if tile:
                        decorations_surface.blit(tile, (x * self.current_map.tilewidth, y * self.current_map.tileheight))

        return terrain_surface, decorations_surface
