import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla para dispositivos móviles genéricos
ANCHO, ALTO = 480, 800
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pong - Jugador vs CPU")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
COLORES_PELOTA = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
color_pelota = random.choice(COLORES_PELOTA)  # Color inicial de la pelota

# Configuración inicial
reloj = pygame.time.Clock()
FPS = 60

# Paletas
PALETA_ANCHO, PALETA_ALTO = 20, 100
paleta_jugador = pygame.Rect(30, ALTO // 2 - PALETA_ALTO // 2, PALETA_ANCHO, PALETA_ALTO)
paleta_cpu = pygame.Rect(ANCHO - 50, ALTO // 2 - PALETA_ALTO // 2, PALETA_ANCHO, PALETA_ALTO)

# Pelotas
PELOTA_ANCHO, PELOTA_ALTO = 20, 20
pelotas = [pygame.Rect(ANCHO // 2 - PELOTA_ANCHO // 2, ALTO // 2 - PELOTA_ALTO // 2, PELOTA_ANCHO, PELOTA_ALTO) for _ in range(5)]
velocidades_pelotas = [[random.choice([-5, 5]), random.choice([-5, 5])] for _ in pelotas]

# Velocidad de las paletas
velocidad_paleta = 10
velocidad_paleta_cpu = 5

# Puntuación
puntuacion_jugador = 0
puntuacion_cpu = 0

# Función para dibujar texto en la pantalla
fuente = pygame.font.Font(None, 36)
def dibujar_texto(texto, x, y):
    superficie_texto = fuente.render(texto, True, BLANCO)
    pantalla.blit(superficie_texto, (x, y))

# Pantalla de carga
def pantalla_de_carga():
    pantalla.fill(NEGRO)
    fuente_grande = pygame.font.Font(None, 48)
    texto_titulo = fuente_grande.render("Pong - Jugador vs CPU", True, BLANCO)
    pantalla.blit(texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, ALTO // 4))

    instrucciones = [
        "Instrucciones del juego:",
        "1. Mueve la paleta del jugador con el touchpad.",
        "2. Desliza hacia arriba para mover la paleta arriba.",
        "3. Desliza hacia abajo para mover la paleta abajo.",
        "4. Golpea la pelota para que el CPU no pueda devolverla.",
        "5. La pelota cambiará de color al ser golpeada.",
        "6. ¡Buena suerte y diviértete!"
    ]

    for i, instruccion in enumerate(instrucciones):
        texto = fuente.render(instruccion, True, BLANCO)
        pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 + i * 40))

    pygame.display.flip()
    pygame.time.wait(5000)  # Espera 5 segundos en la pantalla de carga

# Llamar a la pantalla de carga
pantalla_de_carga()

# Bucle principal del juego
jugando = True
while jugando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False

        # Controles táctiles
        if evento.type == pygame.FINGERDOWN or evento.type == pygame.FINGERMOTION:
            if evento.x < 0.5:  # Si el toque está en la mitad izquierda de la pantalla
                if evento.y < 0.5:
                    paleta_jugador.y -= velocidad_paleta
                else:
                    paleta_jugador.y += velocidad_paleta

    # Controles de teclado para el jugador (para pruebas en PC)
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_w] and paleta_jugador.top > 0:
        paleta_jugador.y -= velocidad_paleta
    if teclas[pygame.K_s] and paleta_jugador.bottom < ALTO:
        paleta_jugador.y += velocidad_paleta

    # Movimiento de la paleta del CPU
    for pelota in pelotas:
        if pelota.centery < paleta_cpu.centery and paleta_cpu.top > 0:
            paleta_cpu.y -= velocidad_paleta_cpu
        if pelota.centery > paleta_cpu.centery and paleta_cpu.bottom < ALTO:
            paleta_cpu.y += velocidad_paleta_cpu

    # Movimiento de las pelotas
    for i, pelota in enumerate(pelotas):
        pelota.x += velocidades_pelotas[i][0]
        pelota.y += velocidades_pelotas[i][1]

        # Colisiones con la parte superior e inferior de la pantalla
        if pelota.top <= 0 or pelota.bottom >= ALTO:
            velocidades_pelotas[i][1] = -velocidades_pelotas[i][1]

        # Colisiones con las paletas
        if pelota.colliderect(paleta_jugador) or pelota.colliderect(paleta_cpu):
            velocidades_pelotas[i][0] = -velocidades_pelotas[i][0]
            color_pelota = random.choice(COLORES_PELOTA)  # Cambiar el color de la pelota

        # Puntuación
        if pelota.left <= 0:
            puntuacion_cpu += 1
            pelota.x, pelota.y = ANCHO // 2 - PELOTA_ANCHO // 2, ALTO // 2 - PELOTA_ALTO // 2
            velocidades_pelotas[i] = [random.choice([-5, 5]), random.choice([-5, 5])]
        if pelota.right >= ANCHO:
            puntuacion_jugador += 1
            pelota.x, pelota.y = ANCHO // 2 - PELOTA_ANCHO // 2, ALTO // 2 - PELOTA_ALTO // 2
            velocidades_pelotas[i] = [random.choice([-5, 5]), random.choice([-5, 5])]

    # Dibujar todo en la pantalla
    pantalla.fill(NEGRO)
    pygame.draw.rect(pantalla, BLANCO, paleta_jugador)
    pygame.draw.rect(pantalla, BLANCO, paleta_cpu)
    for pelota in pelotas:
        pygame.draw.ellipse(pantalla, color_pelota, pelota)
    pygame.draw.aaline(pantalla, BLANCO, (ANCHO // 2, 0), (ANCHO // 2, ALTO))

    # Mostrar puntuación
    dibujar_texto(f"Jugador: {puntuacion_jugador}", 20, 20)
    dibujar_texto(f"CPU: {puntuacion_cpu}", ANCHO - 120, 20)

    pygame.display.flip()
    reloj.tick(FPS)

pygame.quit()
sys.exit()