import pygame
import os
import random
import sys
pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("Dino LevelUp")

game_font = pygame.font.Font("Assets/Other/PressStart2P-Regular.ttf", 24)

# Classes
class Cloud(pygame.sprite.Sprite):
    def __init__(self, image, x_pos, y_pos):
        super().__init__()
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.rect.x -= 1


class Dino(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.running_sprites = []
        self.ducking_sprites = []

        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("Assets/Dino/DinoRun1.png"), (80, 100)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("Assets/Dino/DinoRun2.png"), (80, 100)))

        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load(f"Assets/Dino/DinoDuck1.png"), (110, 60)))
        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load(f"Assets/Dino/DinoDuck2.png"), (110, 60)))

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.current_image = 0
        self.image = self.running_sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.velocity = 50
        self.gravity = 4.0
        self.ducking = False

    def jump(self):
        if self.rect.centery >= 360:
            jump_sfx.play()
            self.velocity = -18

    def duck(self):
        self.ducking = True
        self.rect.centery = 380

    def unduck(self):
        self.ducking = False
        self.rect.centery = 360

    def apply_gravity(self):
        self.rect.centery += self.velocity
        self.velocity += 0.5  # gravity

        if self.rect.centery >= 360:
            self.rect.centery = 360
            self.velocity = 0

    def update(self):
        self.animate()
        self.apply_gravity()

    def animate(self):
        self.current_image += 0.05
        if self.current_image >= 2:
            self.current_image = 0

        if self.ducking:
            self.image = self.ducking_sprites[int(self.current_image)]
        else:
            self.image = self.running_sprites[int(self.current_image)]


class Cactus(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.sprites = []
        for i in range(1, 7):
            current_sprite = pygame.transform.scale(
                pygame.image.load(f"Assets/Cactus/cactus{i}.png"), (100, 100))
            self.sprites.append(current_sprite)
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))


class Ptero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x_pos = 1300
        self.y_pos = random.choice([285, 295, 350])
        self.sprites = []
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("Assets/Bird/Bird1rev.png"), (84, 62)))
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("Assets/Bird/Bird2rev.png"), (84, 62)))
        self.current_image = 0
        self.image = self.sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.animate()
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def animate(self):
        self.current_image += 0.025
        if self.current_image >= 2:
            self.current_image = 0
        self.image = self.sprites[int(self.current_image)]


# Variables
game_speed = 3
player_score = 0
game_over = False
obstacle_timer = 0
obstacle_cooldown = 1000

# Surfaces
ground = pygame.image.load("Assets/Other/Track.png")
ground = pygame.transform.scale(ground, (1280, 20))
ground_x = 0

cloud = pygame.image.load("Assets/Other/Cloud.png")
cloud = pygame.transform.scale(cloud, (200, 80))

# Groups
cloud_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
dino_group = pygame.sprite.GroupSingle()
ptero_group = pygame.sprite.Group()

# Dino object
dinosaur = Dino(50, 360)
dino_group.add(dinosaur)

# Sounds
death_sfx = pygame.mixer.Sound("sfx/lose.mp3")
points_sfx = pygame.mixer.Sound("sfx/100points.mp3")
jump_sfx = pygame.mixer.Sound("sfx/jump.mp3")
all_sfx = pygame.mixer.Sound("sfx/AllSound.mp3")
all_sfx.set_volume(0.2)
all_sfx.play(loops=-1)

# Cloud Event
CLOUD_EVENT = pygame.USEREVENT
pygame.time.set_timer(CLOUD_EVENT, 3000)

# Functions
def end_game():
    global player_score, game_speed
    game_over_text = game_font.render("Game Over!", True, "black")
    game_over_rect = game_over_text.get_rect(center=(640, 300))
    score_text = game_font.render(f"Score: {int(player_score)}", True, "black")
    score_rect = score_text.get_rect(center=(640, 340))
    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    game_speed = 5


# Main Game Loop
while True:

    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        dinosaur.duck()
    else:
        if dinosaur.ducking:
            dinosaur.unduck()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == CLOUD_EVENT:
            current_cloud_y = random.randint(50, 300)
            current_cloud = Cloud(cloud, 1380, current_cloud_y)
            cloud_group.add(current_cloud)

        # --- FIXED KEYDOWN BLOCK ---
        if event.type == pygame.KEYDOWN:

            # ESC quit
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            # Jump + Restart logic
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                dinosaur.jump()

                if game_over:
                    game_over = False
                    game_speed = 5
                    player_score = 0
                    obstacle_group.empty()
                    cloud_group.empty()
                    all_sfx.play(loops=-1)  # restart backsound

    screen.fill("white")

    # COLLISION CHECK
    if pygame.sprite.spritecollide(dino_group.sprite, obstacle_group, False):
        if not game_over:
            game_over = True
            death_sfx.play()
            all_sfx.stop()  # stop background music

    if game_over:
        end_game()
    else:

        game_speed += 0.0025

        if round(player_score, 1) % 100 == 0 and int(player_score) > 0:
            points_sfx.play()

        if pygame.time.get_ticks() - obstacle_timer >= obstacle_cooldown:

            obstacle_random = random.randint(1, 50)

            if obstacle_random in range(1, 7):
                new_obstacle = Cactus(1280, 340)
                obstacle_group.add(new_obstacle)
                obstacle_timer = pygame.time.get_ticks()

            elif obstacle_random in range(7, 10):
                new_obstacle = Ptero()
                obstacle_group.add(new_obstacle)
                obstacle_timer = pygame.time.get_ticks()

        player_score += 0.1
        score_surface = game_font.render(str(int(player_score)), True, "black")
        screen.blit(score_surface, (1150, 10))

        # Update/draw
        cloud_group.update()
        cloud_group.draw(screen)

        ptero_group.update()
        ptero_group.draw(screen)

        dino_group.update()
        dino_group.draw(screen)

        obstacle_group.update()
        obstacle_group.draw(screen)

        # Ground scroll
        ground_x -= game_speed
        screen.blit(ground, (ground_x, 360))
        screen.blit(ground, (ground_x + 1280, 360))
        if ground_x <= -1280:
            ground_x = 0

    clock.tick(120)
    pygame.display.update()
