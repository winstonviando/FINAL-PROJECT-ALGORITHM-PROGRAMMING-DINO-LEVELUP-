# (pygame: main library for), (os: use to check file like high score), (random: random cactus, cloud, powerups), (sys: to exit game
import pygame
import os
import random
import sys
pygame.init()

game_state = "menu" #determine game state in menu
high_score = 0 #set initial high score to 0

# Load saved high score if exists and invalid then high score is 0
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as f:
        try:
            high_score = int(f.read()) #read file and change into integer
        except:
            high_score = 0

#Screen
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock() #FPS control
pygame.display.set_caption("Dino LevelUp - Powerups")

#Font
game_font = pygame.font.Font("Assets/Other/PressStart2P-Regular.ttf", 24)

#Classes
class Cloud(pygame.sprite.Sprite):
    def __init__(self, image, x_pos, y_pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

    def update(self):
        self.rect.x -= 1


class Dino(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.running_sprites = []
        self.ducking_sprites = []

        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("Assets/Dino/DinoRun1revv.png"), (80, 100)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("Assets/Dino/DinoRun2revv.png"), (80, 100)))

        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load("Assets/Dino/DinoDuck1revv.png"), (110, 60)))
        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load("Assets/Dino/DinoDuck2revv.png"), (110, 60)))

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.current_image = 0
        self.image = self.running_sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.velocity = 50
        self.ducking = False

    def jump(self):
        # Jump allowed only if on ground
        if self.rect.centery >= 360:
            jump_sfx.play()
            # Jump height depends on jump boost
            if jump_boost_active:
                self.velocity = -24
            else:
                self.velocity = -21

    def duck(self):
        self.ducking = True
        self.rect.centery = 380

    def unduck(self):
        self.ducking = False
        self.rect.centery = 360

    def apply_gravity(self):
        self.rect.centery += self.velocity
        self.velocity += 0.5   # gravity

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
                pygame.image.load(f"Assets/Cactus/cactus{i}revv.png"), (100, 150))
            self.sprites.append(current_sprite)
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        # use speed multiplier for slow motion
        self.x_pos -= game_speed * speed_multiplier
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        # remove if offscreen
        if self.rect.right < -50:
            self.kill()


class Ptero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x_pos = random.choice([1300, 1000, 1500])
        self.y_pos = random.choice([280, 295, 320])
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
        self.x_pos -= game_speed * speed_multiplier
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        if self.rect.right < -50:
            self.kill()

    def animate(self):
        self.current_image += 0.02
        if self.current_image >= 2:
            self.current_image = 0
        self.image = self.sprites[int(self.current_image)]


class Powerup(pygame.sprite.Sprite):
    """Power-up that moves left like obstacles. type in {'shield','jump','double'}"""
    def __init__(self, kind, x_pos=1280, y_pos= random.choice([300, 250, 200])):
        super().__init__()
        self.kind = kind
        # try load images; fallback to a simple colored surface if missing
        try:
            if kind == "shield":
                self.image = pygame.transform.scale(pygame.image.load("Assets/Powerups/shield.png"), (64, 64))
            elif kind == "jump":
                self.image = pygame.transform.scale(pygame.image.load("Assets/Powerups/jump.png"), (64, 64))
            elif kind == "double":
                # Changed image name to reflect double points
                self.image = pygame.transform.scale(pygame.image.load("Assets/Powerups/double_points.png"), (64, 64))
            else:
                raise FileNotFoundError
        except Exception:
            # fallback simple icon
            self.image = pygame.Surface((64, 64), pygame.SRCALPHA)
            if kind == "shield":
                # Blue circle
                pygame.draw.circle(self.image, (0, 160, 255, 200), (32, 32), 30)
            elif kind == "jump":
                # Yellow arrow/triangle
                pygame.draw.polygon(self.image, (255, 200, 0, 200), [(10,54),(32,6),(54,54)])
            else:
                # Distinct purple star/diamond for Double Points (fallback for double_points.png)
                points = [ (32, 8), (42, 22), (56, 22), (46, 36), (50, 50), (32, 40), (14, 50), (18, 36), (8, 22), (22, 22)]
                pygame.draw.polygon(self.image, (180, 0, 220, 200), points)


        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.rect.x -= game_speed * speed_multiplier
        if self.rect.right < -50:
            self.kill()

# Variables & State
game_speed = 3
speed_multiplier = 1 # used for slow motion powerup
player_score = 0
game_over = False
obstacle_timer = 0
# Initial cooldown is set high, but will be dynamically calculated in the loop
obstacle_cooldown = 2000 
powerup_timer = 0
powerup_cooldown = 6000  

# Powerup states
shield_active = False
shield_end_time = 0

jump_boost_active = False
jump_boost_end_time = 0

double_points_active = False
double_points_end_time = 0

# Surfaces
ground = pygame.image.load("Assets/Other/Track.png")
ground = pygame.transform.scale(ground, (1280, 20))
ground_x = 0

cloud_img = pygame.image.load("Assets/Other/Cloud.png")
cloud_img = pygame.transform.scale(cloud_img, (200, 80))
background_img = pygame.image.load("Assets/Other/christmas_bg.png").convert()
background_img = pygame.transform.scale(background_img, (1280, 720))

# Groups
cloud_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
dino_group = pygame.sprite.GroupSingle()
ptero_group = pygame.sprite.Group()
powerup_group = pygame.sprite.Group()

# Objects
dinosaur = Dino(50, 360)
dino_group.add(dinosaur)

# Sounds
death_sfx = pygame.mixer.Sound("sfx/lose.mp3")
points_sfx = pygame.mixer.Sound("sfx/100points.mp3")
jump_sfx = pygame.mixer.Sound("sfx/jump.mp3")
pickup_sfx = None
try:
    pickup_sfx = pygame.mixer.Sound("sfx/pickup.mp3")
except Exception:
    # if no sound, ignore and no outputing error
    pickup_sfx = None

all_sfx = pygame.mixer.Sound("sfx/AllSound.mp3")
all_sfx.set_volume(0.2)
all_sfx.play(loops=-1)

# Events
CLOUD_EVENT = pygame.USEREVENT
pygame.time.set_timer(CLOUD_EVENT, 3000)

# ---------------------------
# Functions
# ---------------------------
def end_game():
    global player_score, game_speed
    game_over_text = game_font.render("Game Over!", True, "black")
    game_over_rect = game_over_text.get_rect(center=(640, 300))
    score_text = game_font.render(f"Score: {int(player_score)}", True, "black")
    score_rect = score_text.get_rect(center=(640, 340))
    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    high_text = game_font.render(f"High Score: {high_score}", True, "black")
    high_rect = high_text.get_rect(center=(640, 380))
    screen.blit(high_text, high_rect)

    game_speed = 5

def reset_powerups():
    global shield_active, shield_end_time
    global jump_boost_active, jump_boost_end_time
    global double_points_active, double_points_end_time

    shield_active = False
    shield_end_time = 0

    jump_boost_active = False
    jump_boost_end_time = 0

    double_points_active = False
    double_points_end_time = 0
def draw_menu():
    screen.blit(background_img, (0, 0))

    # Title
    title_surf = title_font.render("DINO LEVEL UP", True, (255, 255, 255))
    title_rect = title_surf.get_rect(center=(640, 250))
    screen.blit(title_surf, title_rect)

    # Start button
    pygame.draw.rect(screen, (200, 0, 0), start_btn_rect, border_radius=10)
    start_text = start_font.render("START", True, (255, 255, 255))
    start_rect = start_text.get_rect(center=start_btn_rect.center)
    screen.blit(start_text, start_rect)


    
def draw_shield_aura(sprite):
    # draw semi-transparent circle around the dino to show shield
    aura_surf = pygame.Surface((sprite.rect.width*2, sprite.rect.height*2), pygame.SRCALPHA)
    pygame.draw.circle(aura_surf, (0, 160, 255, 100), (aura_surf.get_width()//2, aura_surf.get_height()//2), max(sprite.rect.width, sprite.rect.height))
    screen.blit(aura_surf, (sprite.rect.centerx - aura_surf.get_width()//2, sprite.rect.centery - aura_surf.get_height()//2))


# Main Loop

# Start Button
start_btn_rect = pygame.Rect(0, 0, 300, 80)
start_btn_rect.center = (640, 500)

start_font = pygame.font.Font("Assets/Other/PressStart2P-Regular.ttf", 40)
title_font = pygame.font.Font("Assets/Other/PressStart2P-Regular.ttf", 60)

while True:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        dinosaur.duck()
    else:
        if dinosaur.ducking:
            dinosaur.unduck()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and game_state == "menu":
            if start_btn_rect.collidepoint(event.pos):
                game_state = "playing"

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == CLOUD_EVENT:
            current_cloud_y = random.randint(50, 300)
            current_cloud = Cloud(cloud_img, 1380, current_cloud_y)
            cloud_group.add(current_cloud)

        if event.type == pygame.KEYDOWN:
            # ESC quit
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            # Jump + Restart logic
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if game_state == "playing": # Only allow jump when playing
                    dinosaur.jump()

                    # Restart game when pressing jump after game over
                    if game_over:
                        game_over = False
                        game_speed = 2
                        player_score = 0
                        obstacle_group.empty()
                        ptero_group.empty()
                        cloud_group.empty()
                        powerup_group.empty()
                        reset_powerups()
                        all_sfx.play(loops=-1)  # restart backsound

    if game_state == "menu":
        draw_menu()

    elif game_state == "playing":
        screen.blit(background_img, (0, 0))
        # all your game drawing code here


        # ----------------
        # Collision with obstacles (consider shield)
        # ----------------
        hit = pygame.sprite.spritecollide(dino_group.sprite, obstacle_group, False)
        if hit:
            if not game_over:
                if shield_active:
                    # if shield active, destroy the obstacle but do not end game
                    for o in hit:
                        o.kill()
                else:
                    game_over = True
                    death_sfx.play()
                    all_sfx.stop()
                # --- HIGH SCORE UPDATE ---
                    if player_score > high_score:
                        high_score = int(player_score)
                    with open("highscore.txt", "w") as f:
                        f.write(str(high_score))

        # Collision with powerups
        collected = pygame.sprite.spritecollide(dino_group.sprite, powerup_group, True)
        for pu in collected:
            # activate powerup
            now = pygame.time.get_ticks()
            
            # All powerups last for 3 seconds (3000ms)
            POWERUP_DURATION = 3000
            if pu.kind == "shield":
                shield_active = True
                shield_end_time = now + POWERUP_DURATION
            elif pu.kind == "jump":
                jump_boost_active = True
                jump_boost_end_time = now + POWERUP_DURATION
            elif pu.kind == "double":
                double_points_active = True
                double_points_end_time = now + POWERUP_DURATION

            
            if pickup_sfx:
                pickup_sfx.play()

        # ----------------
        # Update powerup timers
        # ----------------
        t = pygame.time.get_ticks()
        if shield_active and t >= shield_end_time:
            shield_active = False
        if jump_boost_active and t >= jump_boost_end_time:
            jump_boost_active = False
        if double_points_active and t >= double_points_end_time:
            double_points_active = False

        # Game over display
        if game_over:
            end_game()
        else:
            # game running logic
            game_speed += 0.0025  # slowly accelerate (base speed)

            # points sound when hit 100s
            if round(player_score, 1) % 100 == 0 and int(player_score) > 0:
                points_sfx.play()

            # --- spawn cooldown logic ---
            # As speed increases, the cooldown time decreases to maintain density.
            BASE_COOLDOWN = 2000
            MIN_COOLDOWN = 600
        
            # Use game_speed as a factor. Current start speed is 3.
            speed_factor = max(1, game_speed / 3) 
            
            # Calculate the dynamic cooldown, ensuring it doesn't drop below MIN_COOLDOWN
            dynamic_cooldown = max(MIN_COOLDOWN, BASE_COOLDOWN / speed_factor)
            
            # Add a random variance to the dynamic cooldown, max 200ms
            spawn_delay = dynamic_cooldown + random.randint(0, 200)

            # obstacles spawn
            if pygame.time.get_ticks() - obstacle_timer >= spawn_delay:
                # random chance for Cacti, Pterodactyls, or Powerups
                obstacle_random = random.randint(1, 60)
                if obstacle_random in range(1, 7):
                    new_obstacle = Cactus(1280, 340)
                    obstacle_group.add(new_obstacle)
                    obstacle_timer = pygame.time.get_ticks()
                elif obstacle_random in range(7, 10):
                    new_obstacle = Ptero()
                    obstacle_group.add(new_obstacle)
                    obstacle_timer = pygame.time.get_ticks()
                elif obstacle_random in range(35, 38):
                    # spawn a powerup instead
                    kind = random.choice(["shield", "jump", "double"])
                    # vary y depending on kind: shield near ground, jump low, double higher
                    y_map = {"shield": 320, "jump": 270, "double": 240}
                    new_powerup = Powerup(kind, x_pos=1280, y_pos=y_map.get(kind, 300))
                    powerup_group.add(new_powerup)
                    obstacle_timer = pygame.time.get_ticks()

            # update score 
            if double_points_active:
                player_score += 0.2
            else:
                player_score += 0.1

            score_surface = game_font.render(str(int(player_score)), True, "black")
            screen.blit(score_surface, (1150, 10))

            high_surface = game_font.render(f"HI {high_score}", True, "black")
            screen.blit(high_surface, (950, 10))

            # Update groups
            cloud_group.update()
            cloud_group.draw(screen)

            ptero_group.update()
            ptero_group.draw(screen)

            dino_group.update()
            dino_group.draw(screen)

            # Draw shield aura if active
            if shield_active:
                draw_shield_aura(dino_group.sprite)
            obstacle_group.update()
            obstacle_group.draw(screen)
            powerup_group.update()
            powerup_group.draw(screen)

            # Ground scroll
            ground_x -= game_speed 
            screen.blit(ground, (ground_x, 360))
            screen.blit(ground, (ground_x + 1280, 360))
            if ground_x <= -1280:
                ground_x = 0
    clock.tick(120)
    pygame.display.update()