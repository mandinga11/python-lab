import pygame
import pygame.gfxdraw
import sys
import random

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ANCHO, ALTO = 700, 800
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pac-Man")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
AMARILLO = (255, 255, 0)

# Configuración del jugador (Pac-Man)
velocidad = 4
pacman_radio = 15

# Configuración del tamaño de las celdas
CELDA_ANCHO = ANCHO // 20  # Dividimos el ancho en 20 columnas
CELDA_ALTO = ALTO // 15   # Dividimos el alto en 15 filas

# Laberinto en forma de doble serpentina (1: pared, 0: espacio libre, 2: bolita)
laberinto = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
    [1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
    [1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
    [1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
    [1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
    [1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Colores de los fantasmas
colores_fantasmas = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
    (255, 0, 255), (0, 255, 255), (128, 0, 0), (0, 128, 0),
    (0, 0, 128), (128, 128, 0), (128, 0, 128), (0, 128, 128),
    (192, 192, 192), (128, 128, 128), (64, 64, 64), (192, 0, 0),
    (0, 192, 0), (0, 0, 192), (192, 192, 0), (192, 0, 192)
]

# Clase Pac-Man
class PacMan(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(ANCHO // 2, ALTO // 2, pacman_radio * 2, pacman_radio * 2)
        self.dx = 0
        self.dy = 0

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        # Permitir que el jugador traspase las paredes
        if self.rect.right < 0:
            self.rect.left = ANCHO
        elif self.rect.left > ANCHO:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = ALTO
        elif self.rect.top > ALTO:
            self.rect.bottom = 0

    def draw(self, surface):
        pygame.gfxdraw.filled_circle(surface, self.rect.centerx, self.rect.centery, pacman_radio, AMARILLO)

    def handle_touch(self, touch_x, touch_y):
        if touch_x < self.rect.centerx:
            self.dx = -velocidad
        elif touch_x > self.rect.centerx:
            self.dx = velocidad
        else:
            self.dx = 0

        if touch_y < self.rect.centery:
            self.dy = -velocidad
        elif touch_y > self.rect.centery:
            self.dy = velocidad
        else:
            self.dy = 0

# Clase Fantasma
class Fantasma(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.rect = pygame.Rect(x, y, pacman_radio * 2, pacman_radio * 2)
        self.color = color
        self.inactive = True

    def update(self, target):
        if not self.inactive:
            if self.rect.x < target.rect.x:
                self.rect.x += velocidad // 2
            elif self.rect.x > target.rect.x:
                self.rect.x -= velocidad // 2
            if self.rect.y < target.rect.y:
                self.rect.y += velocidad // 2
            elif self.rect.y > target.rect.y:
                self.rect.y -= velocidad // 2

    def draw(self, surface):
        pygame.gfxdraw.box(surface, self.rect, self.color)

# Función para dibujar el laberinto
def dibujar_laberinto():
    for fila in range(len(laberinto)):
        for columna in range(len(laberinto[0])):
            x = columna * CELDA_ANCHO
            y = fila * CELDA_ALTO
            if laberinto[fila][columna] == 1:  # Dibujar paredes
                pygame.draw.rect(ventana, AZUL, (x, y, CELDA_ANCHO, CELDA_ALTO))
            elif laberinto[fila][columna] == 2:  # Dibujar bolitas
                pygame.gfxdraw.filled_circle(ventana, x + CELDA_ANCHO // 2, y + CELDA_ALTO // 2, 5, BLANCO)

# Función para mostrar la pantalla de carga
def pantalla_de_carga():
    ventana.fill(NEGRO)
    fuente = pygame.font.Font(None, 48)
    texto = fuente.render('Pac-Man', True, BLANCO)
    ventana.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 4))

    fuente_pequena = pygame.font.Font(None, 36)
    instrucciones = [
        "Usa W, A, S, D o el touchpad para mover a Pac-Man.",
        "Come todos los puntos blancos para ganar.",
        "Evita a los fantasmas, ellos te persiguen.",
        "Toca la pantalla para comenzar."
    ]

    for i, instruccion in enumerate(instrucciones):
        texto = fuente_pequena.render(instruccion, True, BLANCO)
        ventana.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 + i * 40))

    pygame.display.flip()

# Mostrar la pantalla de carga hasta que se toque la pantalla
pantalla_de_carga()
esperando = True
while esperando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.MOUSEBUTTONDOWN or evento.type == pygame.FINGERDOWN:
            esperando = False

# Inicializar grupos de sprites
jugador = PacMan()
fantasmas = pygame.sprite.Group()

# Crear los 20 fantasmas pero solo activar 5 al inicio
for i, color in enumerate(colores_fantasmas):
    x = CELDA_ANCHO * (i % 10 + 1)
    y = CELDA_ALTO * (i // 10 + 5)
    fantasma = Fantasma(x, y, color)
    if i < 5:  # Activar solo los primeros cinco fantasmas
        fantasma.inactive = False
    fantasmas.add(fantasma)

# Función para verificar si todas las bolitas han sido comidas
def check_win():
    for fila in laberinto:
        if 2 in fila:
            return False
    return True

# Función para mostrar el mensaje de victoria
def mostrar_victoria():
    ventana.fill(NEGRO)
    fuente = pygame.font.Font(None, 72)
    texto = fuente.render('¡Ganaste!', True, BLANCO)
    ventana.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

# Función para mostrar el mensaje de Game Over
def mostrar_game_over():
    ventana.fill(NEGRO)
    fuente = pygame.font.Font(None, 72)
    texto = fuente.render('Game Over', True, ROJO)
    ventana.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

# Bucle principal del juego
reloj = pygame.time.Clock()
ejecutando = True
start_time = pygame.time.get_ticks()

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.FINGERDOWN:
            jugador.handle_touch(evento.x * ANCHO, evento.y * ALTO)
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_w:
                jugador.dy = -velocidad
            elif evento.key == pygame.K_s:
                jugador.dy = velocidad
            elif evento.key == pygame.K_a:
                jugador.dx = -velocidad
            elif evento.key == pygame.K_d:
                jugador.dx = velocidad

    jugador.update()

    # Comer bolitas
    columna = jugador.rect.x // CELDA_ANCHO
    fila = jugador.rect.y // CELDA_ALTO
    if 0 <= fila < len(laberinto) and 0 <= columna < len(laberinto[0]):  # Verificar límites
        if laberinto[fila][columna] == 2:
            laberinto[fila][columna] = 0

    # Verificar si todas las bolitas han sido comidas
    if check_win():
        mostrar_victoria()
        ejecutando = False

    # Activar cinco fantasmas adicionales cada minuto
    tiempo_transcurrido = (pygame.time.get_ticks() - start_time) // 1000
    if tiempo_transcurrido % 60 == 0:
        num_fantasmas_activos = sum(not fantasma.inactive for fantasma in fantasmas)
        for i, fantasma in enumerate(fantasmas):
            if fantasma.inactive and i < num_fantasmas_activos + 5:
                fantasma.inactive = False

    fantasmas.update(jugador)

    # Verificar colisión con fantasmas después de 1 minuto
    if tiempo_transcurrido > 60:
        for fantasma in fantasmas:
            if fantasma.rect.colliderect(jugador.rect):
                mostrar_game_over()
                ejecutando = False

    # Dibujar todo en la pantalla
    ventana.fill(NEGRO)
    dibujar_laberinto()
    jugador.draw(ventana)
    for fantasma in fantasmas:
        fantasma.draw(ventana)

    # Mostrar tiempo en la pantalla
    fuente = pygame.font.Font(None, 36)
    texto = fuente.render(f'Tiempo: {tiempo_transcurrido} s', True, BLANCO)
    ventana.blit(texto, (10, 10))

    pygame.display.flip()

    # Controlar la velocidad del bucle
    reloj.tick(30)

# Salir correctamente al cerrar la ventana
pygame.quit()
sys.exit()