import pygame
import copy
import sys

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 800


global GRID
BLOCK_SIZE = 20  # Set the size of the grid block
GRID = [
    [0 for _ in range(WINDOW_WIDTH // BLOCK_SIZE + 2)]
    for _ in range(WINDOW_HEIGHT // BLOCK_SIZE + 2)
]


def draw_grid():
    for y, row in enumerate(GRID):
        for x, i in enumerate(row):
            rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)


def toggle(i: int, j: int):

    if GRID[i + 1][j + 1] == 0:
        GRID[i + 1][j + 1] = 1
        # Filled Rectangle.
        pygame.draw.rect(SCREEN, WHITE, (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    else:
        GRID[i + 1][j + 1] = 0
        # Filled Rectangle.
        pygame.draw.rect(SCREEN, BLACK, (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        # Bordered Rectangle.
        rect = pygame.Rect(j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(SCREEN, WHITE, rect, 1)


def progress_gameoflife():
    global GRID
    tmp = copy.deepcopy(GRID)
    for b, row in enumerate(GRID[1:-1]):
        for a, i in enumerate(row[1:-1]):
            x = a + 1
            y = b + 1
            s = sum(
                [
                    GRID[y - 1][x - 1],
                    GRID[y - 1][x],
                    GRID[y - 1][x + 1],
                    GRID[y][x - 1],
                    GRID[y][x + 1],
                    GRID[y + 1][x - 1],
                    GRID[y + 1][x],
                    GRID[y + 1][x + 1],
                ]
            )
            if s <= 1 or 4 <= s:
                tmp[y][x] = 0
            elif s == 3:
                tmp[y][x] = 1

    for b, row in enumerate(GRID[1:-1]):
        for a, i in enumerate(row[1:-1]):
            x = a + 1
            y = b + 1
            if GRID[y][x] != tmp[y][x]:
                toggle(b, a)

    GRID = copy.deepcopy(tmp)


global SCREEN, CLOCK
pygame.init()
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()
SCREEN.fill(BLACK)


# MENU
height_offset = -50
smallfont = pygame.font.SysFont("Inconsolata", 35, bold=True)
text = smallfont.render("Press SPACE to Play/Resume", True, WHITE)
text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + height_offset))
SCREEN.blit(text, text_rect)

text = smallfont.render("Q/ESC to Quit", True, WHITE)
text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50 + height_offset))
SCREEN.blit(text, text_rect)

text = smallfont.render("Click to Toggle Cell", True, WHITE)
text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 100 + height_offset))
SCREEN.blit(text, text_rect)

pygame.display.update()

running = True
while running:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        running = False
    if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

# Game Of Life
SCREEN.fill(BLACK)
draw_grid()
running = True
playing_gameoflife = False
while running:
    pygame.time.delay(100)

    if playing_gameoflife:
        progress_gameoflife()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            x = pos[0] // BLOCK_SIZE
            y = pos[1] // BLOCK_SIZE
            toggle(y, x)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
        running = False
    if keys[pygame.K_SPACE]:
        playing_gameoflife = not playing_gameoflife

    pygame.display.update()
