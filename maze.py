import sys
import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600
TILE_SIZE = 40
FPS = 60
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FLOOR_COLOR = (0, 0, 0)
WALL_COLOR = (255, 0, 0)
PLAYER_COLOR = (50, 120, 255)
KEY_COLOR = (255, 255, 255)
EXIT_COLOR = (0, 200, 80)
level_map = [
    "WWWWWWWWWWWWWWWWWWWW", 
    "WP.....W....W....W",
    "W.WWW..W.WW..W.WWW.W",
    "W...W..W.....W...W.W",
    "WWW.W..WW..W.W.W.W.W",
    "W...W...W..W.W.W...KW",
    "W.W...WW...W.W.WWW.W",
    "W......W.....W...W.W",
    "W.WWWW.WWWW..W.W.W",
    "W.W...W.......W...W",
    "W.W..WWW...WWWWW.WWW",
    "W.W................W",
    "W.WWWWWWWWWWWWWW....W",
    "W...............EW",
    "WWWWWWWWWWWWWWWWWWWW",
]
player_size = TILE_SIZE - 8
player_speed = 4

walls = []
key_rect = None
exit_rect = None

player_x = 0
player_y = 0
start_x = 0
start_y = 0

has_key = False
game_state = "playing"
message = "Find the key, then reach the exit."
font = pygame.font.SysFont(None, 32)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Escape")
clock = pygame.time.Clock()

def load_level():
    """Read the map and create wall/key/exit rectangles and player spawn."""
    global walls, key_rect, exit_rect
    global player_x, player_y, start_x, start_y

    walls = []
    key_rect = None
    exit_rect = None

    for row_index, row in enumerate(level_map):
        for col_index, tile in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE

            if tile == "W":
                walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            elif tile == "P":
                player_x = x + (TILE_SIZE - player_size) // 2
                player_y = y + (TILE_SIZE - player_size) // 2
                start_x = player_x
                start_y = player_y
            elif tile == "K":
                key_rect = pygame.Rect(x + 8, y + 8, TILE_SIZE - 16, TILE_SIZE - 16)
            elif tile == "E":
                exit_rect = pygame.Rect(x + 4, y + 4, TILE_SIZE - 8, TILE_SIZE - 8)
def draw_maze():
    """Draw floor, walls, exit, and key if not collected."""
    screen.fill(RED)

    for row_index, row in enumerate(level_map):
        for col_index, _tile in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            pygame.draw.rect(screen, FLOOR_COLOR, pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))

    for wall in walls:
        pygame.draw.rect(screen, WALL_COLOR, wall)

    if exit_rect is not None:
        pygame.draw.rect(screen, EXIT_COLOR, exit_rect)

    if key_rect is not None and not has_key:
        pygame.draw.rect(screen, KEY_COLOR, key_rect)
def draw_player():
    """Draw and return the player rectangle."""
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    pygame.draw.rect(screen, PLAYER_COLOR, player_rect)
    return player_rect
def move_player(keys):
    """Move in four directions and prevent wall clipping."""
    global player_x, player_y

    old_x, old_y = player_x, player_y

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_x += player_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player_y -= player_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_y += player_speed

    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    for wall in walls:
        if player_rect.colliderect(wall):
            player_x, player_y = old_x, old_y
            break
def check_key_collision(player_rect):
    """Collect the key once when touched."""
    global has_key, message

    if key_rect is not None and not has_key and player_rect.colliderect(key_rect):
        has_key = True
        message = "Key collected! Reach the exit."
def check_exit_collision(player_rect):
    """Win only if player has collected the key."""
    global game_state, message

    if exit_rect is None or not player_rect.colliderect(exit_rect):
        return

    if has_key:
        game_state = "win"
        message = "You escaped!"
    else:
        message = "Find the key first."
def draw_hud():
    """Display key status and current instruction text."""
    key_text = "Key: Collected" if has_key else "Key: Not Found"
    maze_pixel_height = len(level_map) * TILE_SIZE
    hud_y = min(maze_pixel_height + 8, HEIGHT - 28)

    key_surface = font.render(key_text, True, GREEN)
    msg_surface = font.render(message, True, GREEN)
    screen.blit(key_surface, (12, hud_y))
    screen.blit(msg_surface, (220, hud_y))
def draw_win_screen():
    """Draw final screen and replay instructions."""
    screen.fill(RED)
    title = font.render("You escaped!", True, EXIT_COLOR)
    prompt = font.render("Press R to restart or ESC to quit", True, GREEN)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 30))
    screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 + 10))
def reset_game():
    """Reset player and game state for replay."""
    global player_x, player_y, has_key, game_state, message

    player_x = start_x
    player_y = start_y
    has_key = False
    game_state = "playing"
    message = "Find the key, then reach the exit."

load_level()
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if game_state == "win" and event.key == pygame.K_r:
                reset_game()

    if game_state == "playing":
        keys = pygame.key.get_pressed()
        move_player(keys)

        draw_maze()
        player_rect = draw_player()
        check_key_collision(player_rect)
        check_exit_collision(player_rect)
        draw_hud()

    elif game_state == "win":
        draw_win_screen()

    pygame.display.flip()

pygame.quit()
sys.exit()