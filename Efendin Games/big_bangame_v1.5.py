import random
import sys
import pygame


from include import words
from slidemenu import slidemenu

# _______________________________________________________________________________
# Variables globales /  global variables

FPS = 50
MODE = 0
LANG = 1  # 0 french 1 English

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# _______________________________________________________________________________
class AllPolygon(pygame.sprite.RenderUpdates):
    def __init__(self):
        pygame.sprite.RenderUpdates.__init__(self)

class Polygon(pygame.sprite.Sprite):
    def __init__(self, left=0, top=0):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((160, 120))

        # Number of tuple for a polygon
        self.nb_tuple = random.randint(3, 12)

        self.coordonates = []
        for i in range(self.nb_tuple):
            c = random.randint(0, 160)
            l = random.randint(0, 120)
            self.coordonates.append((c, l))

        color = BLUE
        pygame.draw.polygon(self.image, color, self.coordonates)
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        # print (self.rect)
        # Remember the position
        self.x = self.rect.left
        self.y = self.rect.top

    def update(self):
        self.rect.bottom += 1
        if self.rect.top > 480:
            pol = Polygon(self.x, -120)
            allpolygon.add(pol)
            self.kill()


# -------------------------------------------------------------------------------
#                              end classes
# _______________________________________________________________________________

def update(zone):
    # update a zone of main surface
    zone = zone
    pygame.display.update(zone)

def toogle():
        global MODE
        # bascule entre mode fenêtré et plein écran
        # switch display between windowed and PANTALLA COMPLETA

        if MODE == 0:
            MODE = pygame.FULLSCREEN
        else:
            MODE = 0

        s = screen.copy()
        screen = pygame.display.set_mode(screen, MODE)
        screen.blit(s, s.get_rect())
        pygame.display.flip()

def keyboard():
    # Gestion des evenements claviers / TECLADO

    pygame.event.get(pygame.KEYDOWN)
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        sys.exit()
    elif pygame.key.get_pressed()[pygame.K_f]:
        toogle()
        

def CreatePolygon():
    #
    # Ajoute les polygones initiaux (Largeur 160 Hauteur 120)
    # 5 lignes de 4 POLIGONOS. La 1ere ligne commence à -120 et est donc invisible au départ
    #

    for y in range(5):
        for i in range(4):
            pol = Polygon(160 * i, 120 * y)
            allpolygon.add(pol)


# -------------------------------------------------------------------------------
#                              End functions
# _______________________________________________________________________________

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

font = pygame.font.Font(None, 36)

pygame.display.set_caption("Big Bangame")


# Background for menu
bg2 = pygame.image.load("./graph/fond2.png").convert_alpha()
bgRect2 = bg2.get_rect()

# Group of Polygon
allpolygon = AllPolygon()


global choix, zone
# Boucle Principale / Main loop

fin = False
while fin == False:
    CreatePolygon()

    # Boucle MENU / Menu loop

    pygame.font.init()
    
    choix = -1
    while choix != 0:
        pygame.time.Clock().tick(FPS)
        screen.blit(bg2, bgRect2)
        update(bgRect2)

        joemenu = slidemenu.menu(
            [
                words.words[0][LANG],
                words.words[4][LANG],
                words.words[5][LANG],
            ],
            font1=pygame.font.Font("./slidemenu/BeteNoirNF.ttf", 20),
            font2=pygame.font.Font("./slidemenu/BeteNoirNF.ttf", 25),
            tooltipfont=pygame.font.Font("./slidemenu/Roboto-MediumItalic.ttf", 12),
            color1=(255, 80, 40),
            cursor_img=pygame.image.load("./graph/nepomuk.png"),
            light=9,
            centerx=320,
            y=240,
        )
        choix = joemenu[1]

        # Option Langue / Langage

        if choix == 1:
            if LANG == 0:
                LANG = 1
            else:
                LANG = 0

        # System exit

        if choix == 2 or choix == None:
            choix = 0
            sys.exit()

    
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
