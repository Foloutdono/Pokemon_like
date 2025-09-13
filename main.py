import pygame
import pytmx

# --- CONFIG ---
PLAYER_SPEED = 3
ZOOM = 7  # facteur de zoom

# --- INIT ---
pygame.init()
info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.NOFRAME)
SCREEN_W, SCREEN_H = screen.get_size()

tmx_data = pytmx.util_pygame.load_pygame("assets/maps/forest/Parde_village.tmx")

# Dimensions de la map en pixels
map_w = tmx_data.width * tmx_data.tilewidth
map_h = tmx_data.height * tmx_data.tileheight

# Créer surface de la map
map_surface = pygame.Surface((map_w, map_h))

collision_rects = []

# Dessiner la map une fois
for layer in tmx_data.visible_layers:
    if isinstance(layer, pytmx.TiledTileLayer):
        for x, y, gid in layer:
            tile = tmx_data.get_tile_image_by_gid(gid)
            if tile:
                map_surface.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))
    else:
        for obj in layer:
            rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            collision_rects.append(rect)

def move_player(player_rect: pygame.Rect, dx: int, dy: int, collisions: list[pygame.Rect]) -> pygame.Rect:
    # Try horizontal move
    player_rect.x += dx
    for rect in collisions:
        if player_rect.colliderect(rect):
            if dx > 0:  # moving right
                player_rect.right = rect.left
            elif dx < 0:  # moving left
                player_rect.left = rect.right

    # Try vertical move
    player_rect.y += dy
    for rect in collisions:
        if player_rect.colliderect(rect):
            if dy > 0:  # moving down
                player_rect.bottom = rect.top
            elif dy < 0:  # moving up
                player_rect.top = rect.bottom

    return player_rect


# --- JOUEUR ---
player = pygame.Rect(100, 100, 8, 16)  # position et taille du joueur
player_color = (255, 0, 0)

clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60) / 1000  # limiter à 60 FPS

    # --- INPUT ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    dx, dy = 0, 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        dx = -2
    if keys[pygame.K_RIGHT]:
        dx = 2
    if keys[pygame.K_UP]:
        dy = -2
    if keys[pygame.K_DOWN]:
        dy = 2

    player = move_player(player, dx, dy, collision_rects)

    # --- CAMERA ---
    view_w = min(SCREEN_W // ZOOM, map_w)
    view_h = min(SCREEN_H // ZOOM, map_h)

    # On essaie de centrer la caméra sur le joueur
    cam_x = player.centerx - view_w // 2
    cam_y = player.centery - view_h // 2

    # On empêche la caméra de sortir des bords
    cam_x = max(0, min(cam_x, map_w - view_w))
    cam_y = max(0, min(cam_y, map_h - view_h))

    # --- RENDU ---
    sub_surface = map_surface.subsurface((cam_x, cam_y, view_w, view_h))
    scaled_surface = pygame.transform.scale(sub_surface, (SCREEN_W, SCREEN_H))
    screen.blit(scaled_surface, (0, 0))

    # Position du joueur relative à la caméra
    player_screen_x = (player.x - cam_x) * ZOOM
    player_screen_y = (player.y - cam_y) * ZOOM
    player_screen_rect = pygame.Rect(player_screen_x, player_screen_y, player.width * ZOOM, player.height * ZOOM)

    # Dessiner le joueur
    pygame.draw.rect(screen, player_color, player_screen_rect)

    pygame.display.flip()

pygame.quit()