import pygame
import sys
import csv

if len(sys.argv) > 2:
    sys.exit('Too many arguments.')
elif len(sys.argv) < 2:
    sys.exit('You need to specify the path to the csv file.')

FILENAME = sys.argv[1]

pygame.init()
WIDTH, HEIGHT = 800, 800
TILESIZE = 32
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Level builder')

BACKGROUNDIMG = pygame.image.load(
    './assets/background/Background.png').convert_alpha()
TILES = [pygame.image.load(
    f'./assets/tiles/Tile_{i+1}.png').convert_alpha() for i in range(96)]


class Selected:
    FONT = pygame.font.SysFont('applegothic', 20, True)

    def __init__(self, scale) -> None:
        self.scale = scale
        self.index = 1
        self.image = TILES[0]
        self.selection_text = self.FONT.render(
            f'Tile: 1/{len(TILES)}', True, (0, 0, 0))

    def change_selection(self, value):
        if 0 < self.index + value < 97:
            self.index += value
            self.image = TILES[self.index - 1]
            self.selection_text = self.FONT.render(
                f'Selected: {self.index}/{len(TILES)}', True, (0, 0, 0))

    def draw(self, saved):
        if saved:
            self.saved_text = self.FONT.render(
                f'File saved.', True, (0, 255, 0))
        else:
            self.saved_text = self.FONT.render(
                f'Not saved.', True, (255, 0, 0))

        screen.blit(pygame.transform.scale(
            self.image, (self.scale * TILESIZE, self.scale * TILESIZE)), (20, 20))
        screen.blit(self.selection_text, (20, 160))
        screen.blit(self.saved_text, (160, 20))


class Tile:
    def __init__(self, row, col, value=0) -> None:
        self.row = row
        self.col = col
        self.value = value
        self.image = None if self.value == 0 else TILES[self.value - 1]

    def __repr__(self) -> str:
        return str(self.value)

    def update(self, index):
        self.value = index
        self.image = None if self.value == 0 else TILES[self.value - 1]
        # self.image.set_alpha(0 if self.value == 0 else 255)

    def draw(self):
        if self.image:
            screen.blit(self.image, (self.row * TILESIZE,
                        200 + self.col * TILESIZE))


def make_grid():
    try:
        with open(FILENAME, 'r') as file:
            file_reader = csv.reader(file)
            parsed = [row for row in file_reader]
            grid = [[Tile(i, j, value=int(parsed[i][j])) for j in range(len(parsed[i]))]
                    for i in range(len(parsed))]
    except:
        print('Error with parsing file.')
        grid = [[Tile(i, j) for j in range(WIDTH//TILESIZE)]
                for i in range(HEIGHT//TILESIZE)]
    return grid


def draw_grid():
    for i in range(HEIGHT//TILESIZE):
        pygame.draw.line(screen, (0, 0, 0), (0, 200 + i *
                         TILESIZE), (WIDTH, 200 + i * TILESIZE))
        for j in range(WIDTH//TILESIZE):
            pygame.draw.line(screen, (0, 0, 0),
                             (j * TILESIZE, 200), (j * TILESIZE, HEIGHT))


def draw(grid, selected: Selected, saved):
    for row in grid:
        for tile in row:
            tile.draw()

    selected.draw(saved)


def get_clicked_pos(pos):
    y, x = pos

    row = (y) // TILESIZE
    col = (x-200) // TILESIZE

    return row, col


running = True
saved = False
grid = make_grid()
selected = Selected(scale=4)
clock = pygame.time.Clock()
while running:
    clock.tick(FPS)
    screen.fill((255, 255, 255))
    screen.blit(pygame.transform.scale(
        BACKGROUNDIMG, (WIDTH, HEIGHT - 200)), (0, 200))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

        if pygame.mouse.get_pressed():
            pos = pygame.mouse.get_pos()
            row, col = get_clicked_pos(pos)
            tile = grid[row][col]
            if pygame.mouse.get_pressed()[0]:
                tile.update(selected.index)
            elif pygame.mouse.get_pressed()[2]:
                tile.update(0)
            saved = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                selected.change_selection(-1)
            if event.key == pygame.K_RIGHT:
                selected.change_selection(1)
            if event.key == pygame.K_c:
                grid = make_grid()
            if event.key == pygame.K_s:
                value_grid = [[tile.value for tile in row] for row in grid]
                with open(FILENAME, 'w') as file:
                    file_writer = csv.writer(file)
                    for row in value_grid:
                        file_writer.writerow(row)
                print(f'File saved to {FILENAME}.')
                saved = True

    draw(grid, selected, saved)
    draw_grid()
    pygame.display.update()
