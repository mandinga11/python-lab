import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
screen_width, screen_height = 360, 690  # Expandir el tablero
preview_width, preview_height = 120, 120
screen = pygame.display.set_mode((screen_width + preview_width, screen_height))
pygame.display.set_caption("Tetris")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Configuración del juego
grid_width, grid_height = 12, 23  # Reducir la altura del tablero
cell_size = 30
FPS = 5  # Disminuir aún más la velocidad del juego

# Formas de Tetris
shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 1, 1],
     [1, 1, 0]],

    [[1, 1, 0],
     [0, 1, 1]],

    [[1, 1, 1, 1]],

    [[1, 1],
     [1, 1]],

    [[1, 1, 1],
     [1, 0, 0]],

    [[1, 1, 1],
     [0, 0, 1]]
]

shape_colors = [CYAN, BLUE, ORANGE, YELLOW, GREEN, MAGENTA, RED]

# Reloj
clock = pygame.time.Clock()

# Clase para manejar el juego de Tetris
class Tetris:
    def __init__(self):
        self.grid = [[BLACK for _ in range(grid_width)] for _ in range(grid_height)]
        self.current_shape = self.get_new_shape()
        self.next_shape = self.get_new_shape()
        self.shape_pos = [0, grid_width // 2 - len(self.current_shape[0]) // 2]
        self.game_over = False
        self.score = 0
        self.start_time = pygame.time.get_ticks()
        self.drop_time = pygame.time.get_ticks()
        self.fast_drop = False

    def get_new_shape(self):
        shape = random.choice(shapes)
        color = shape_colors[shapes.index(shape)]
        return shape, color

    def rotate_shape(self):
        new_shape = [list(row) for row in zip(*self.current_shape[0][::-1])]
        if self.valid_move(0, 0, new_shape):
            self.current_shape = (new_shape, self.current_shape[1])

    def valid_move(self, dx, dy, shape=None):
        if shape is None:
            shape = self.current_shape[0]
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.shape_pos[1] + x + dx
                    new_y = self.shape_pos[0] + y + dy
                    if new_x < 0 or new_x >= grid_width or new_y >= grid_height or (new_y >= 0 and self.grid[new_y][new_x] != BLACK):
                        return False
        return True

    def merge_shape(self):
        for y, row in enumerate(self.current_shape[0]):
            for x, cell in enumerate(row):
                if cell:
                    new_y = self.shape_pos[0] + y
                    new_x = self.shape_pos[1] + x
                    if 0 <= new_x < grid_width and 0 <= new_y < grid_height:
                        self.grid[new_y][new_x] = self.current_shape[1]

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell == BLACK for cell in row)]
        cleared_lines = grid_height - len(new_grid)
        self.score += cleared_lines * 100
        self.grid = [[BLACK for _ in range(grid_width)] for _ in range(cleared_lines)] + new_grid

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.fast_drop or current_time - self.drop_time > 1000:  # Ajuste de velocidad de caída
            self.drop_time = current_time
            if not self.valid_move(1, 0):
                self.merge_shape()
                self.current_shape = self.next_shape
                self.next_shape = self.get_new_shape()
                self.shape_pos = [0, grid_width // 2 - len(self.current_shape[0]) // 2]
                if not self.valid_move(0, 0):
                    self.game_over = True
            else:
                self.shape_pos[0] += 1

    def draw_grid(self):
        for y in range(grid_height):
            for x in range(grid_width):
                pygame.draw.rect(screen, self.grid[y][x], (x * cell_size, y * cell_size, cell_size, cell_size))
                pygame.draw.rect(screen, WHITE, (x * cell_size, y * cell_size, cell_size, cell_size), 1)

    def draw_shape(self):
        for y, row in enumerate(self.current_shape[0]):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.current_shape[1], ((self.shape_pos[1] + x) * cell_size, (self.shape_pos[0] + y) * cell_size, cell_size, cell_size))
                    pygame.draw.rect(screen, WHITE, ((self.shape_pos[1] + x) * cell_size, (self.shape_pos[0] + y) * cell_size, cell_size, cell_size), 1)

    def draw_next_shape(self):
        for y, row in enumerate(self.next_shape[0]):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.next_shape[1], ((grid_width + 1 + x) * cell_size, (1 + y) * cell_size, cell_size, cell_size))
                    pygame.draw.rect(screen, WHITE, ((grid_width + 1 + x) * cell_size, (1 + y) * cell_size, cell_size, cell_size), 1)

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    def draw_time(self):
        font = pygame.font.Font(None, 36)
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        time_text = font.render(f"Time: {elapsed_time} s", True, WHITE)
        screen.blit(time_text, (screen_width - 150, 10))

# Función para mostrar la pantalla de carga con instrucciones
def show_loading_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render("Tetris", True, WHITE)
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2 - 50))
    
    font_instructions = pygame.font.Font(None, 36)
    instructions = [
        "Instrucciones:",
        "Toca para comenzar el juego",
        "Desliza a los lados para mover piezas",
        "Toque para girar pieza",
        "Mantén presionado para caída rápida"
    ]
    for i, line in enumerate(instructions):
        instruction_text = font_instructions.render(line, True, WHITE)
        screen.blit(instruction_text, (screen_width // 2 - instruction_text.get_width() // 2, screen_height // 2 + i * 30))
    
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN]:
                waiting = False

# Función principal del juego
def main():
    show_loading_screen()
    game = Tetris()
    running = True
    touch_start = None

    while running and not game.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if game.valid_move(0, -1):
                        game.shape_pos[1] -= 1
                elif event.key == pygame.K_RIGHT:
                    if game.valid_move(0, 1):
                        game.shape_pos[1] += 1
                elif event.key == pygame.K_DOWN:
                    if game.valid_move(1, 0):
                        game.shape_pos[0] += 1
                elif event.key == pygame.K_UP:
                    game.rotate_shape()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    game.fast_drop = False
            elif event.type == pygame.FINGERDOWN:
                touch_start = event.x
                game.fast_drop = True
            elif event.type == pygame.FINGERMOTION and touch_start is not None:
                if event.dx > 0.1:
                    if game.valid_move(0, 1):
                        game.shape_pos[1] += 1
                    touch_start = event.x
                elif event.dx < -0.1:
                    if game.valid_move(0, -1):
                        game.shape_pos[1] -= 1
                    touch_start = event.x
            elif event.type == pygame.FINGERUP:
                touch_start = None
                game.fast_drop = False
                game.rotate_shape()  # Girar la pieza con un solo toque y soltar

        screen.fill(BLACK)
        game.update()
        game.draw_grid()
        game.draw_shape()
        game.draw_score()
        game.draw_time()
        game.draw_next_shape()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit(0)

if __name__ == "__main__":
    main()