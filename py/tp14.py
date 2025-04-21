import pygame
import random
import sys

# Initialisation
pygame.init()

# Configuration écran
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Couleurs
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jeu de tir - TP POO")

# Chargement et redimensionnement des images
player_img = pygame.transform.scale(pygame.image.load("image-removebg-preview.png"), (64, 64))
enemy_img = pygame.transform.scale(pygame.image.load("retro-cartoon-creepy-tarantula-free-png.webp"), (64, 64))
background = pygame.transform.scale(pygame.image.load("Space matters.jpeg"), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Police
font = pygame.font.SysFont(None, 36)

# ======== CLASSES ========

class Player:
    def __init__(self):
        self.image = player_img
        self.x = SCREEN_WIDTH // 2 - 32
        self.y = SCREEN_HEIGHT - 100
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - 64:
            self.x += self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


class Enemy:
    def __init__(self):
        self.image = enemy_img
        self.x = random.randint(0, SCREEN_WIDTH - 64)
        self.y = random.randint(-150, -40)
        self.speed = random.randint(2, 4)  # ENNEMIS PLUS LENTS

    def move(self):
        self.y += self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 64, 64)

# Fonction pour afficher le score
def show_score(score):
    score_text = font.render(f"Score : {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# ======== JEU PRINCIPAL ========

player = Player()
enemies = [Enemy() for _ in range(2)]  # Moins d'ennemis
score = 0
game_over = False

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(FPS)
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.move(keys)

    # === LASER CODE ===
    if keys[pygame.K_SPACE]:
        laser_x = player.x + 32  # Centre du joueur
        pygame.draw.line(screen, RED, (laser_x, player.y), (laser_x, 0), 4)

        # Tuer les ennemis touchés par le laser
        for enemy in enemies[:]:
            if enemy.x < laser_x < enemy.x + 60:
                enemies.remove(enemy)
                enemies.append(Enemy())  # Remplacer par un nouveau
                score += 1
    # ===================

    # Mise à jour des ennemis
    for enemy in enemies[:]:
        enemy.move()
        enemy.draw()

        # Ennemi atteint le bas
        if enemy.is_off_screen():
            game_over = True

    player.draw()
    show_score(score)

    if game_over:
        over_text = font.render(f"Game Over ! Score final : {score}", True, WHITE)
        screen.blit(over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
        pygame.display.update()
        pygame.time.delay(3000)
        running = False

    pygame.display.update()

pygame.quit()
sys.exit()
