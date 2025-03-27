import random

import pygame

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Big Bang")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

particle_size = 10
expansion_speed = 1
max_particles = 50

player_image = pygame.Surface((particle_size, particle_size))
player_image.fill(BLUE)
player_rect = player_image.get_rect(center=(screen_width // 2, screen_height // 2))

particles = []
for _ in range(max_particles):
    x = random.randint(0, screen_width)
    y = random.randint(0, screen_height)
    dx = random.choice([-1, 1]) * random.uniform(0.5, 2)
    dy = random.choice([-1, 1]) * random.uniform(0.5, 2)
    particles.append(
        {"rect": pygame.Rect(x, y, particle_size, particle_size), "dx": dx, "dy": dy}
    )

font = pygame.font.Font(None, 36)

running = True
clock = pygame.time.Clock()
score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= 5
    if keys[pygame.K_RIGHT] and player_rect.right < screen_width:
        player_rect.x += 5
    if keys[pygame.K_UP] and player_rect.top > 0:
        player_rect.y -= 5
    if keys[pygame.K_DOWN] and player_rect.bottom < screen_height:
        player_rect.y += 5

    for particle in particles:
        particle["rect"].x += particle["dx"]
        particle["rect"].y += particle["dy"]

        if particle["rect"].left < 0 or particle["rect"].right > screen_width:
            particle["dx"] *= -1
        if particle["rect"].top < 0 or particle["rect"].bottom > screen_height:
            particle["dy"] *= -1

        if player_rect.colliderect(particle["rect"]):
            running = False

    screen.fill(BLACK)

    for particle in particles:
        pygame.draw.rect(screen, RED, particle["rect"])

    screen.blit(player_image, player_rect)

    score_text = font.render(f"Puntaje: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    score += expansion_speed
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
