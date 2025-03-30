import pygame
import random
import math

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Big Bang & Big Crunch Game")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

particle_size = 10
expansion_speed = 1
max_particles = 50
num_obstacles = 20
touch_limit = 3

font_size = 36
font = pygame.font.Font(None, font_size)

clock = pygame.time.Clock()
running = True
score = 0
big_crunch_mode = False
touch_count = 0

def init_player():
    player_image = pygame.Surface((particle_size, particle_size))
    player_image.fill(BLUE)
    player_rect = player_image.get_rect(center=(50, screen_height // 2))  # Empezar en el extremo izquierdo
    return player_image, player_rect

def init_particles(max_particles):
    particles = []
    for _ in range(max_particles):
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)
        states = [
            {"dx": random.uniform(-2, 2), "dy": random.uniform(-2, 2)},
            {"dx": random.uniform(-3, 3), "dy": random.uniform(-3, 3)},
            {"dx": random.uniform(-1, 1), "dy": random.uniform(-1, 1)}
        ]
        entangled_particle = random.choice([True, False])
        particles.append({
            "rect": pygame.Rect(x, y, particle_size, particle_size),
            "states": states,
            "current_state": None,
            "entangled": entangled_particle,
            "collapsed": False,
            "color": YELLOW if entangled_particle else WHITE
        })
    return particles

def init_obstacles(num_obstacles):
    obstacles = []
    for _ in range(num_obstacles):
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)
        obstacles.append({
            "rect": pygame.Rect(x, y, particle_size, particle_size),
            "color": RED
        })
    return obstacles

def collapse_state(particle):
    return random.choice(particle["states"])

def update_entangled_particles(entangled_particles):
    for particle in entangled_particles:
        if particle["current_state"]:
            particle["current_state"]["dx"] *= -1
            particle["current_state"]["dy"] *= -1

def move_particles_towards_center(particles):
    center_x = screen_width // 2
    center_y = screen_height // 2
    for particle in particles:
        if not particle["collapsed"]:
            dx = center_x - particle["rect"].centerx
            dy = center_y - particle["rect"].centery
            distance = math.sqrt(dx**2 + dy**2)
            if distance != 0:
                particle["rect"].x += int(dx / distance * abs(particle["current_state"]["dx"] if particle["current_state"] else expansion_speed))
                particle["rect"].y += int(dy / distance * abs(particle["current_state"]["dy"] if particle["current_state"] else expansion_speed))

def draw_spiral(screen, center, radius, color):
    angle = 0
    while radius > 0:
        x = int(center[0] + radius * math.cos(angle))
        y = int(center[1] + radius * math.sin(angle))
        pygame.draw.circle(screen, color, (x, y), 2)
        angle += 0.1
        radius -= 0.1

def reset_game():
    global score, big_crunch_mode, particles, obstacles, player_image, player_rect, touch_count
    score = 0
    big_crunch_mode = False
    touch_count = 0
    particles = init_particles(max_particles)
    obstacles = init_obstacles(num_obstacles)
    player_image, player_rect = init_player()

def pantalla_de_carga():
    screen.fill(BLACK)
    fuente_grande = pygame.font.Font(None, 48)
    texto_titulo = fuente_grande.render("Big Bang & Big Crunch Game", True, WHITE)
    screen.blit(texto_titulo, (screen_width // 2 - texto_titulo.get_width() // 2, screen_height // 4))

    instrucciones = [
        "Instrucciones del juego:",
        "1. Mueve la partícula azul usando el touchpad.",
        "2. Absorbe partículas blancas y amarillas para crecer.",
        "3. Evita las partículas rojas (obstáculos).",
        "4. Si tocas 3 obstáculos, pierdes.",
        "5. Llega al agujero de gusano (espiral verde) para ganar.",
        "¡Presiona cualquier tecla para comenzar!"
    ]

    fuente = pygame.font.Font(None, 36)
    for i, instruccion in enumerate(instrucciones):
        texto = fuente.render(instruccion, True, WHITE)
        screen.blit(texto, (screen_width // 2 - texto.get_width() // 2, screen_height // 2 + i * 40))

    pygame.display.flip()
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
                esperando = False

# Mostrar pantalla de carga
pantalla_de_carga()

player_image, player_rect = init_player()
particles = init_particles(max_particles)
obstacles = init_obstacles(num_obstacles)

# Configurar el agujero de gusano (salida)
wormhole_center = (screen_width - 50, screen_height // 2)  # En el extremo derecho
wormhole_radius = 40

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Reiniciar el juego
                reset_game()
        if event.type == pygame.MOUSEMOTION:
            player_rect.center = event.pos

    entangled_particles = [p for p in particles if p["entangled"]]

    all_collapsed = True

    for particle in particles:
        if player_rect.colliderect(particle["rect"]):
            if not particle["current_state"]:
                particle["current_state"] = collapse_state(particle)
                if particle["entangled"]:
                    update_entangled_particles(entangled_particles)

            particle["collapsed"] = True
            player_rect.inflate_ip(particle["rect"].width, particle["rect"].height)  # Aumentar el tamaño del jugador
            particle["rect"].width = 0  # Reducir el tamaño de la partícula a cero
            particle["rect"].height = 0  # Reducir el tamaño de la partícula a cero
            particle["color"] = RED

        if big_crunch_mode and not particle["collapsed"]:
            move_particles_towards_center([particle])
        elif not big_crunch_mode and not particle["collapsed"]:
            all_collapsed = False
            if not particle["current_state"]:
                particle["rect"].x += random.uniform(-1.5, 1.5)
                particle["rect"].y += random.uniform(-1.5, 1.5)
            else:
                particle["rect"].x += particle["current_state"]["dx"]
                particle["rect"].y += particle["current_state"]["dy"]

        if particle["rect"].left < 0 or particle["rect"].right > screen_width:
            if not big_crunch_mode and particle["current_state"]:
                particle["current_state"]["dx"] *= -1

        if particle["rect"].top < 0 or particle["rect"].bottom > screen_height:
            if not big_crunch_mode and particle["current_state"]:
                particle["current_state"]["dy"] *= -1

    for obstacle in obstacles:
        if player_rect.colliderect(obstacle["rect"]):
            touch_count += 1
            if touch_count >= touch_limit:
                running = False

    # Si todas las partículas están colapsadas y no estamos en modo Big Crunch,
    # inicia la explosión del Big Bang
    if all_collapsed and not big_crunch_mode:
        for particle in particles:
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 3)
            particle["current_state"] = {
                "dx": math.cos(angle) * speed,
                "dy": math.sin(angle) * speed
            }
        big_crunch_mode = True

    # Verificar si el jugador ha llegado al agujero de gusano
    if player_rect.colliderect(pygame.Rect(wormhole_center[0] - wormhole_radius, wormhole_center[1] - wormhole_radius, wormhole_radius * 2, wormhole_radius * 2)):
        running = False

    screen.fill(BLACK)

    for particle in particles:
        pygame.draw.rect(screen, particle["color"], particle["rect"])

    for obstacle in obstacles:
        pygame.draw.rect(screen, obstacle["color"], obstacle["rect"])

    screen.blit(player_image, player_rect)

    draw_spiral(screen, wormhole_center, wormhole_radius, GREEN)

    score_text = font.render(f"Score: {score}", True, WHITE)
    restart_text = font.render("Press R to Restart", True, WHITE)
    touch_text = font.render(f"Touches: {touch_count}/{touch_limit}", True, RED)
    
    screen.blit(score_text, (10, 10))
    screen.blit(touch_text, (10, font_size + 10))
    screen.blit(restart_text, (10, font_size * 2 + 10))

    score += expansion_speed
    pygame.display.flip()
    clock.tick(60)

pygame.quit()