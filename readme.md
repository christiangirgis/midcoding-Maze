# Maze Escape Project

This guide walks you through the code they need to write, one piece at a time.

Important rule: do not copy a full completed game from anywhere.
Build and test each step before moving on.

## Learning Goal

Build a top-down maze game in Pygame where the player:

- moves through a maze,
- collects a key,
- reaches the exit after collecting the key.

## What You Will Practice

- Variables and constants
- Lists of strings (grid maps)
- Loops and conditionals
- Functions
- Collision with rectangles
- Game state logic

## Setup

1. Install Python 3 and Pygame.
2. Create a file named maze_escape.py.
3. Run the file after every step.

Install command:

```bash
pip install pygame
```

---

## Step 1: Create the game window

Write just enough code to open and close a Pygame window.

Write this structure:

```python
import pygame
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
```

Checkpoint:

- Window opens.
- Clicking the close button exits cleanly.

---

## Step 2: Add constants and colors

At the top of the file, add constants so values are easy to change later.

Students should define:

- TILE_SIZE
- FPS
- 4 to 6 color tuples (wall, floor, player, key, exit)

Example pattern:

```python
TILE_SIZE = 40
FPS = 60

WALL_COLOR = (100, 100, 100)
FLOOR_COLOR = (30, 30, 30)
```

Checkpoint:

- No magic numbers repeated everywhere.

---

## Step 3: Build the maze map

Create a list of strings. Each character means one tile type.

Required tile letters:

- W = wall
- P = player start
- K = key
- E = exit
- . = empty space

Template students can fill in:

```python
level_map = [
    "WWWWWWWWWW",
    "WP.......W",
    "W.WWWW...W",
    "W....W...W",
    "W..K.W.E.W",
    "WWWWWWWWWW",
]
```

Teacher note: encourage them to design their own map after first test.

Checkpoint:

- Exactly one P, one K, and one E.
- Walls around outer border.

---

## Step 4: Draw the maze tiles

Use nested loops over rows and columns.

Students need this thinking:

- row index = y tile position
- col index = x tile position
- x = col index * TILE_SIZE
- y = row index * TILE_SIZE

Skeleton logic:

```python
for row_index, row in enumerate(level_map):
    for col_index, tile in enumerate(row):
        x = col_index * TILE_SIZE
        y = row_index * TILE_SIZE

        # draw floor first
        # if tile is W, draw wall over floor
        # if tile is K or E, draw those markers
```

Checkpoint:

- Maze appears in the correct grid shape.

---

## Step 5: Find player start from P

Do not hard-code player coordinates.
Scan map once at startup to find P.

Students create:

- player_x
- player_y
- player_size

Pattern:

```python
for row_index, row in enumerate(level_map):
    for col_index, tile in enumerate(row):
        if tile == "P":
            player_x = col_index * TILE_SIZE
            player_y = row_index * TILE_SIZE
```

Checkpoint:

- Player spawns on the P tile.

---

## Step 6: Draw player rectangle

Add a player draw step each frame.

```python
player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
pygame.draw.rect(screen, PLAYER_COLOR, player_rect)
```

Checkpoint:

- Player appears every frame.

---

## Step 7: Add movement input

Use arrow keys or WASD.
Start with movement only, no collision.

Pattern:

```python
keys = pygame.key.get_pressed()

if keys[pygame.K_LEFT]:
    player_x -= speed
if keys[pygame.K_RIGHT]:
    player_x += speed
if keys[pygame.K_UP]:
    player_y -= speed
if keys[pygame.K_DOWN]:
    player_y += speed
```

Checkpoint:

- Player moves in all four directions.

---

## Step 8: Store wall rectangles

When reading the map, create a list named walls.
For each W tile, append a Rect.

Pattern:

```python
walls = []

# inside map loop
if tile == "W":
    wall_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
    walls.append(wall_rect)
```

Checkpoint:

- walls list has many rectangles.

---

## Step 9: Block movement through walls

Classic beginner collision method:

1. Save old position.
2. Apply movement.
3. Build player rect at new position.
4. If colliding with any wall, go back to old position.

Pattern:

```python
old_x, old_y = player_x, player_y

# move player using keys

player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
for wall in walls:
    if player_rect.colliderect(wall):
        player_x, player_y = old_x, old_y
        break
```

Checkpoint:

- Player cannot pass through walls.

---

## Step 10: Add key collection logic

Track whether key is collected.

Required variable:

```python
has_key = False
```

When loading map, create a key_rect for K.
Each frame, check if player touches key_rect.
If yes:

- has_key becomes True
- stop drawing key

Collision pattern:

```python
if not has_key and player_rect.colliderect(key_rect):
    has_key = True
```

Checkpoint:

- Key disappears after pickup.

---

## Step 11: Add exit logic with condition

Create exit_rect from E.
Player should win only if touching exit and has_key is True.

Pattern:

```python
if player_rect.colliderect(exit_rect):
    if has_key:
        game_state = "win"
    else:
        message = "Find the key first"
```

Checkpoint:

- Exit does nothing before key.
- Exit wins after key.

---

## Step 12: Add game states

Use one variable to control screens.

Suggested values:

- playing
- win

Pattern:

```python
if game_state == "playing":
    # normal update and draw
elif game_state == "win":
    # draw win screen text
```

Checkpoint:

- Win screen appears and gameplay pauses.

---

## Step 13: Add restart

Create a reset_game() function.
Reset:

- player position
- has_key
- game_state
- message text

Handle key press R during win state.

Pattern:

```python
if event.type == pygame.KEYDOWN:
    if game_state == "win" and event.key == pygame.K_r:
        reset_game()
```

Checkpoint:

- Player can replay without restarting Python.

---

## Step 14: Add text HUD

Display at least:

- key status
- current instruction message

Students can use pygame.font.SysFont(None, size).

Suggested messages:

- Key: Not Found
- Key: Collected
- Find the key, then reach the exit
- You escaped

Checkpoint:

- Text updates based on gameplay events.

---

## Step 15: Refactor into functions

Before adding extra features, organize code into functions.

Recommended function list:

- load_level()
- draw_maze()
- move_player(keys)
- check_key_collision(player_rect)
- check_exit_collision(player_rect)
- draw_hud()
- reset_game()

Teacher tip: students should move one chunk at a time and test after each move.

---

## Extension Ideas (After Base Game Works)

Pick 2 to 3:

- Add a timer.
- Add a second key.
- Add a locked door tile D.
- Add moving enemies.
- Add multiple levels.
- Replace rectangles with images.
- Add sounds and music.

---

## Required Student Comments

Students must comment these ideas in their own words:

- How the map encoding works (W, P, K, E, .)
- How movement is read from keyboard
- How wall collision rollback works
- How key collection changes game state
- How win condition is checked

Rule: comments explain why, not just what.

---

## Grading Checklist

- Window opens and closes correctly
- Maze draws correctly
- Player starts on P
- Player moves in 4 directions
- Walls block movement
- Key can be collected
- Exit only wins after key
- Win screen appears
- Restart works
- Code is organized and commented

---

## Teaching Note

This document intentionally avoids giving one full final script.
Students should assemble the game step by step, testing each section as they code.
