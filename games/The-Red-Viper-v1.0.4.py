import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Efendor & Mandinga Project Presents")

# Colores
ROAD_COLOR = (50, 50, 50)
LINE_COLOR = (255, 255, 255)
CAR_COLOR = (255, 0, 0)
OBSTACLE_COLOR = (0, 0, 255)
TEXT_COLOR = (255, 255, 255)

# Configuración inicial
clock = pygame.time.Clock()
FPS = 60

# ... (código de la pantalla de carga ASCII, sin cambios) ...

# Carriles (5 carriles)
LANE_WIDTH = WIDTH // 5
NUM_LANES = 5
LANE_VERTICAL_OFFSET = 100
LANES = [(i * LANE_WIDTH + LANE_WIDTH // 2, LANE_VERTICAL_OFFSET) for i in range(NUM_LANES)]

# Clase para el coche
class Car:
    def __init__(self):
        self.rect = pygame.Rect(LANES[NUM_LANES // 2][0] - 25, HEIGHT - 100, 50, 80)
        self.speed_x = 0
        self.speed_y = 0
        self.current_lane_index = NUM_LANES // 2
        self.lane_change_timer = 0 #Temporizador para evitar cambios de carril demasiado rápidos

    def move_left(self):
        if self.lane_change_timer <= 0 and self.current_lane_index > 0:
            self.current_lane_index -= 1
            self.lane_change_timer = 10 #Tiempo de espera antes del siguiente cambio
    def move_right(self):
        if self.lane_change_timer <= 0 and self.current_lane_index < NUM_LANES - 1:
            self.current_lane_index += 1
            self.lane_change_timer = 10

    def move_up(self):
        self.speed_y = -5
    def move_down(self):
        self.speed_y = 5

    def stop(self):
        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        self.lane_change_timer = max(0, self.lane_change_timer - 1)
        self.rect.x = LANES[self.current_lane_index][0] - self.rect.width // 2
        self.rect.y += self.speed_y
        self.rect.y = max(LANE_VERTICAL_OFFSET + 40, min(self.rect.y, HEIGHT - self.rect.height - 40))

    def draw(self):
        pygame.draw.rect(screen, CAR_COLOR, self.rect)

# Clase para las líneas de la carretera
class RoadLines:
    def __init__(self):
        self.lines = []
        for y in LANES:
            self.lines.append(pygame.Rect(0, y[1], WIDTH, 5))
        for x in range(LANE_WIDTH // 2, WIDTH, LANE_WIDTH):
            self.lines.append(pygame.Rect(x, LANE_VERTICAL_OFFSET, 5, HEIGHT - LANE_VERTICAL_OFFSET))

    def draw(self):
        for line in self.lines:
            pygame.draw.rect(screen, LINE_COLOR, line)


# Clase para los obstáculos
class Obstacle:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(50, WIDTH - 50), -50,
                                random.randint(40, 80), random.randint(40, 80))
        self.speed_y = random.randint(3, 6)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.rect.y = -50
            self.rect.x = random.randint(50, WIDTH - 50)
            global points
            if points % 10 == 0:
                self.speed_y += random.randint(1, 2)

    def draw(self):
        pygame.draw.rect(screen, OBSTACLE_COLOR, self.rect)


# Mostrar texto en pantalla
font = pygame.font.Font(None, 36)
def draw_text(text, x, y):
    text_surface = font.render(text, True, TEXT_COLOR)
    screen.blit(text_surface, (x, y))

# Reiniciar el juego
def reset_game():
    global car, road_lines, obstacles, points, start_time
    car = Car()
    road_lines = RoadLines()
    obstacles = [Obstacle() for _ in range(5)]
    points = 0
    start_time = pygame.time.get_ticks()

# Inicializar objetos del juego
reset_game()

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                car.move_left()
            elif event.key == pygame.K_RIGHT:
                car.move_right()
            elif event.key == pygame.K_UP:
                car.move_up()
            elif event.key == pygame.K_DOWN:
                car.move_down()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                car.stop()
        #Controles táctiles (mejorados)
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if x < WIDTH // 3:
                car.move_left()
            elif x > 2 * WIDTH // 3:
                car.move_right()


    # Actualizar lógica del juego
    car.update()

    screen.fill(ROAD_COLOR)
    road_lines.draw()
    car.draw()

    for obstacle in obstacles:
        obstacle.update()
        obstacle.draw()
        if car.rect.colliderect(obstacle.rect):
            draw_text("¡Game Over!", WIDTH // 2 - 100, HEIGHT // 2)
            pygame.display.flip()
            pygame.time.delay(2000)
            reset_game()

    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    draw_text(f"Tiempo: {elapsed_time}s", 10, 10)
    draw_text(f"Puntos: {points}", 10, 50)
    draw_text(f"FPS: {int(clock.get_fps())}", 10, 90)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
