# Maze Escape Walkthrough

This guide matches the structure and variable names in the demo file `mazegame.py`.

Goal: help students finish missing code blocks without jumping to a full copy/paste solution first.

Use this process in class:

1. Reveal one block at a time.
2. Run after each block.
3. Fix one bug before moving on.

---

## What Students Are Building

A top-down maze game where the player:

- moves with arrow keys or WASD,
- collects the key,
- then reaches the exit to win,
- and can restart with `R`.

---

## Setup

1. Install Python 3.
2. Install Pygame:

```bash
pip install pygame
```

3. Run the game file:

```bash
python3 mazegame.py
```

---

## Starter Structure Students Should Already Have

Students should already have:

- imports,
- constants,
- `level_map`,
- global state variables,
- main game loop shell.

If they are missing major structure, have them copy the top-level frame first, then complete TODO blocks below.

---

## Missing Block 1: `load_level()`

Purpose: scan `level_map` and build walls, key, exit, and player spawn.

Fill-in code:

```python
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
```

Quick check:

- `walls` is not empty.
- player starts on `P`.
- key and exit appear in the right tiles.

---

## Missing Block 2: `reset_game()`

Purpose: replay without restarting Python.

Fill-in code:

```python
def reset_game():
    """Reset key state and player position so the game can be replayed."""
    global player_x, player_y, has_key, game_state, message

    player_x = start_x
    player_y = start_y
    has_key = False
    game_state = "playing"
    message = "Find the key, then reach the exit."
```

Quick check:

- after winning, press `R` and game returns to start state.

---

## Missing Block 3: `draw_maze()`

Purpose: draw floor first, then walls, exit, and key.

Fill-in code:

```python
def draw_maze():
    """Draw floor first, then walls, exit, and key if it has not been collected."""
    screen.fill(BLACK)

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
```

Quick check:

- key disappears after collection.
- exit remains visible.

---

## Missing Block 4: `move_player(keys)`

Purpose: move and stop wall clipping using rollback collision.

Fill-in code:

```python
def move_player(keys):
    """Move in four directions and roll back movement if a wall collision occurs."""
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
```

Quick check:

- player moves in all directions.
- player cannot pass through walls.

---

## Missing Block 5: key + exit collision functions

Purpose: collect key once, and win only after key.

Fill-in code:

```python
def check_key_collision(player_rect):
    """Collect the key once when the player touches it."""
    global has_key, message

    if key_rect is not None and not has_key and player_rect.colliderect(key_rect):
        has_key = True
        message = "Key collected! Reach the exit."


def check_exit_collision(player_rect):
    """Allow winning only after the key has been collected."""
    global game_state, message

    if exit_rect is None or not player_rect.colliderect(exit_rect):
        return

    if has_key:
        game_state = "win"
        message = "You escaped!"
    else:
        message = "Find the key first."
```

Quick check:

- touching exit before key shows warning.
- touching exit after key wins.

---

## Missing Block 6: player and HUD drawing

Purpose: draw player and status text every frame.

Fill-in code:

```python
def draw_player():
    """Draw and return the player rectangle for collision checks."""
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    pygame.draw.rect(screen, PLAYER_COLOR, player_rect)
    return player_rect


def draw_hud():
    """Show key status and current game message below the maze."""
    key_text = "Key: Collected" if has_key else "Key: Not Found"
    maze_pixel_height = len(level_map) * TILE_SIZE
    hud_y = min(maze_pixel_height + 8, HEIGHT - 28)

    key_surface = font.render(key_text, True, WHITE)
    msg_surface = font.render(message, True, WHITE)
    screen.blit(key_surface, (12, hud_y))
    screen.blit(msg_surface, (220, hud_y))
```

Quick check:

- key status text changes.
- message updates during play.

---

## Missing Block 7: win screen

Purpose: show simple victory screen and restart hint.

Fill-in code:

```python
def draw_win_screen():
    """Draw a simple win screen with restart instructions."""
    screen.fill(BLACK)
    title = font.render("You escaped!", True, EXIT_COLOR)
    prompt = font.render("Press R to restart or ESC to quit", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 30))
    screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 + 10))
```

Quick check:

- win screen replaces gameplay render.
- `R` restarts, `ESC` quits.

---

## Missing Block 8: main loop wiring

Purpose: connect all functions in the right order.

Critical sequence in `playing` state:

1. read keys
2. move player
3. draw maze
4. draw player and get rect
5. check key collision
6. check exit collision
7. draw HUD

Reference wiring:

```python
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
```

If this order is changed, behavior can feel wrong (for example, stale collision checks or delayed HUD updates).

---

## Debug Checklist for Students

If their game is broken, check these first:

1. Forgot `global` in functions that modify game state.
2. Typo in tile letters (`W`, `P`, `K`, `E`).
3. `load_level()` never called before main loop.
4. Collision checks run before `player_rect` is created.
5. Drawing key even after `has_key` becomes `True`.
6. Restart handler not limited to `win` state.

---

## Suggested Grading Targets

- Game runs without crashing.
- Player movement works (arrows and/or WASD).
- Walls block movement.
- Key collects once and disappears.
- Exit requires key.
- Win screen appears.
- Restart works with `R`.
- Student can explain each function's purpose.

---

## Teacher Use Tip

If students still freeze on blanks, provide function headers and docstrings first, then ask them to fill only the internal logic lines. This keeps cognitive load lower while preserving problem-solving.