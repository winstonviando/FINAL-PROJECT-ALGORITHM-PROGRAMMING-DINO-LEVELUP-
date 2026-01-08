# (pygame: main library for), (os: use to check file like high score), (random: random cactus, cloud, powerups), (sys: to exit game
import pygame
import os
import random
import sys
pygame.init() #mandatory init pygame for activate all pygame modules

game_state = "menu" #determine game state in menu
high_score = 0 #set initial high score to 0

# Load saved high score if exists and invalid then high score is 0
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as f:
        try:
            high_score = int(f.read()) #read file and change into integer
        except:
            high_score = 0 #if invalid content high score is 0

#Screen
screen = pygame.display.set_mode((1280, 720)) #window size 1280x720
clock = pygame.time.Clock() #FPS control
pygame.display.set_caption("Dino LevelUp - Powerups") #window title

#Font
game_font = pygame.font.Font("Assets/Other/PressStart2P-Regular.ttf", 24) #game font

#Classes
class Cloud(pygame.sprite.Sprite): #cloud class, cloud is sprite that move left
    def __init__(self, image, x_pos, y_pos): 
        super().__init__() #inherit  from pygame sprite
        self.image = image #cloud image
        self.rect = self.image.get_rect(center=(x_pos, y_pos)) #cloud position centered at x_pos and y_pos, rect is rectangle around the image or collision box

    def update(self):
        self.rect.x -= 1 #cloud move left at speed 1


class Dino(pygame.sprite.Sprite): #dinosaur class the main character
    def __init__(self, x_pos, y_pos): 
        super().__init__() #inherit from pygame sprite
        self.running_sprites = [] #list contain running sprites
        self.ducking_sprites = [] #list contain ducking sprites

        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("Assets/Dino/DinoRun1revv.png"), (80, 100))) #load and scale running sprite 1
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("Assets/Dino/DinoRun2revv.png"), (80, 100)))

        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load("Assets/Dino/DinoDuck1revv.png"), (110, 60)))
        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load("Assets/Dino/DinoDuck2revv.png"), (110, 60)))

        self.x_pos = x_pos #dinosaur x position
        self.y_pos = y_pos #dinosaur y position
        self.current_image = 0 #current image index is 0 (start) for animation
        self.image = self.running_sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.velocity = 0 #initial vertical velocity 
        self.ducking = False #initial ducking state is false

    def jump(self):
        # Jump allowed only if on ground (prevent double jump click)
        if self.rect.centery >= 360:
            jump_sfx.play() #play jump sound effect
            # Jump height depends on jump boost
            if jump_boost_active:
                self.velocity = -15 # higher jump with boost
            else:
                self.velocity = -12 # normal jump

    def duck(self):
        self.ducking = True #set ducking state to true
        self.rect.centery = 380 #adjust y position for ducking

    def unduck(self):
        self.ducking = False #set ducking state to false
        self.rect.centery = 360 #adjust y position back to normal

    def apply_gravity(self):
        self.rect.centery += self.velocity #apply vertical velocity to y position
        self.velocity += 0.25 # gravity add to velocity

        if self.rect.centery >= 360: #if on ground
            self.rect.centery = 360  #reset y position to ground level
            self.velocity = 0 #reset velocity when on ground

    def update(self): #update method called every frame
        self.animate() #call animate method
        self.apply_gravity() #apply gravity effect

    def animate(self):
        self.current_image += 0.05 #increment current image for dino animation speed
        if self.current_image >= 2: #loop back to first image > index 0
            self.current_image = 0 #reset to first image

        if self.ducking: #if ducking state is true
            self.image = self.ducking_sprites[int(self.current_image)] #set image to ducking by convert float to int for index
        else:
            self.image = self.running_sprites[int(self.current_image)] #set image to running by convert float to int for index

class Cactus(pygame.sprite.Sprite): #cactus obstacle class
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.sprites = []
        for i in range(1, 7):
            current_sprite = pygame.transform.scale(
                pygame.image.load(f"Assets/Cactus/cactus{i}revv.png"), (100, 150))
            self.sprites.append(current_sprite)
        self.image = random.choice(self.sprites) #randomly choose one cactus sprite out of 7
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        # use speed multiplier for slow motion
        self.x_pos -= game_speed * speed_multiplier #move left by game speed and increase with speed multiplier
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        
        if self.rect.right < -50: #if cactus is offscreen to the left
            self.kill() #remove cactus from all groups and ram memory

class Ptero(pygame.sprite.Sprite): #pterodactyl obstacle class
    def __init__(self):
        super().__init__()
        self.x_pos = random.choice([1300, 1000, 1500]) #random x position on game spawn
        self.y_pos = random.choice([250, 280, 230]) #random y position for flying heights
        self.sprites = []
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("Assets/Bird/Bird1rev.png"), (84, 62)))
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("Assets/Bird/Bird2rev.png"), (84, 62)))
        self.current_image = 0 #current image index for animation
        self.image = self.sprites[self.current_image] #initial imageS
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos)) #set rect position and make collision box

    def update(self):
        self.animate() #animate ptero
        self.x_pos -= game_speed * speed_multiplier #move left by game speed and increase with speed multiplier
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos)) #update rect position
        if self.rect.right < -50: #if ptero is offscreen to the left
            self.kill() #remove ptero from all groups and ram memory

    def animate(self):
        self.current_image += 0.03 #increment current image for ptero animation speed
        if self.current_image >= 2:
            self.current_image = 0
        self.image = self.sprites[int(self.current_image)]

class Powerup(pygame.sprite.Sprite):
    #Power-up that moves left like obstacles. {'shield','jump','double'}
    def __init__(self, kind, x_pos= random.choice([1280, 1300, 1500]), y_pos= random.choice([230, 250, 200])):
        super().__init__()
        self.kind = kind #powerup identity
        # try load images; fallback to a simple colored surface if missing
        
        self.x_pos = x_pos #powerup x position
        self.y_pos = y_pos #powerup y position
        try: #load images based on kind of powerupS
            if kind == "shield":
                self.image = pygame.transform.scale(pygame.image.load("Assets/Powerups/shield.png"), (64, 64))
            elif kind == "jump":
                self.image = pygame.transform.scale(pygame.image.load("Assets/Powerups/jump.png"), (64, 64))
            elif kind == "double":
                # Changed image name to reflect double points
                self.image = pygame.transform.scale(pygame.image.load("Assets/Powerups/double_points.png"), (64, 64))
            else:
                raise FileNotFoundError #invalid kind
        except Exception:
            # fallback: create simple colored surface
            self.image = pygame.Surface((64, 64), pygame.SRCALPHA) #64x64 transparent surface
            if kind == "shield":
                # Blue circle
                pygame.draw.circle(self.image, (0, 160, 255, 200), (32, 32), 30)
            elif kind == "jump":
                # Yellow triangle
                pygame.draw.polygon(self.image, (255, 200, 0, 200), [(10,54),(32,6),(54,54)])
            else:
                # Purple star/diamond for Double Points (fallback for double_points.png)
                points = [ (32, 8), (42, 22), (56, 22), (46, 36), (50, 50), (32, 40), (14, 50), (18, 36), (8, 22), (22, 22)]
                pygame.draw.polygon(self.image, (180, 0, 220, 200), points)

        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.spawn_time = pygame.time.get_ticks() #timestamp when powerup spawned like powerup timer in miliseconds

    def update(self):
        self.x_pos -= game_speed * speed_multiplier #move left by game speed and increase with speed multiplier
        self.rect.centerx = self.x_pos
        if self.rect.right < -50:
            self.kill()

# Variables & State
game_speed = 3 #initial game speed
speed_multiplier = 1 # used for slow motion powerup (1 = constant speed at 3)
player_score = 0 #initial player score
game_over = False #initial game over state
obstacle_timer = 0 #timer for obstacle spawn

# Initial cooldown is set high, but will be dynamically calculated in the loop
powerup_timer = 0 #timer for powerup spawn

# Powerup states
shield_active = False 
shield_end_time = 0 #initial shield end time

jump_boost_active = False
jump_boost_end_time = 0

double_points_active = False
double_points_end_time = 0

# Surfaces
ground = pygame.image.load("Assets/Other/Track.png") #load ground image
ground = pygame.transform.scale(ground, (1280, 20)) #scale ground image
ground_x = 0 #initial ground x position at left

cloud_img = pygame.image.load("Assets/Other/Cloud.png")
cloud_img = pygame.transform.scale(cloud_img, (200, 80))
background_img = pygame.image.load("Assets/Other/christmas_bg.png").convert()
background_img = pygame.transform.scale(background_img, (1280, 720))

# Groups (bundle draw, update, and collision for multiple sprites)
cloud_group = pygame.sprite.Group() 
obstacle_group = pygame.sprite.Group()
dino_group = pygame.sprite.GroupSingle()
ptero_group = pygame.sprite.Group()
powerup_group = pygame.sprite.Group()

# Objects
dinosaur = Dino(50, 360) #create dinosaur object at position (50, 360)
dino_group.add(dinosaur) #add dinosaur to dino group

# Sounds
death_sfx = pygame.mixer.Sound("sfx/lose.mp3") #death sound effect
points_sfx = pygame.mixer.Sound("sfx/100points.mp3") #points sound effect
jump_sfx = pygame.mixer.Sound("sfx/jump.mp3") #jump sound effect
pickup_sfx = None
try: #try load pickup sound effect
    pickup_sfx = pygame.mixer.Sound("sfx/pickup.mp3")
except Exception:
    # if no sound, ignore and no resulting error
    pickup_sfx = None

all_sfx = pygame.mixer.Sound("sfx/AllSound.mp3") #background jinggle bell music
all_sfx.set_volume(0.2) #set volume lower for background music
all_sfx.play(loops=-1) #play background music in loop

# Events
CLOUD_EVENT = pygame.USEREVENT #custom event for cloud spawn
pygame.time.set_timer(CLOUD_EVENT, 2000) #set timer to trigger cloud event every 2000ms (2 seconds)

# Functions
def end_game():
    global player_score, game_speed #access global variables
    game_over_text = game_font.render("Game Over!", True, "black") #render game over text
    game_over_rect = game_over_text.get_rect(center=(640, 300)) #center rect for game over text
    score_text = game_font.render(f"Score: {int(player_score)}", True, "black") #render score text
    score_rect = score_text.get_rect(center=(640, 340)) #center rect for score text
    screen.blit(game_over_text, game_over_rect) #draw game over text on screen
    screen.blit(score_text, score_rect) #draw score text on screen
    high_text = game_font.render(f"High Score: {high_score}", True, "black") #render high score text
    high_rect = high_text.get_rect(center=(640, 380)) #center rect for high score text
    screen.blit(high_text, high_rect) #draw high score text on screen


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
    aura_surf = pygame.Surface((sprite.rect.width*2, sprite.rect.height*2), pygame.SRCALPHA) #create transparent surface
    pygame.draw.circle(aura_surf, (0, 160, 255, 100), (aura_surf.get_width()//2, aura_surf.get_height()//2), max(sprite.rect.width, sprite.rect.height)) #draw semi-transparent blue circle
    screen.blit(aura_surf, (sprite.rect.centerx - aura_surf.get_width()//2, sprite.rect.centery - aura_surf.get_height()//2)) #blit aura centered on sprite blit is like overlay


# Main Loop

# Start Button
start_btn_rect = pygame.Rect(0, 0, 300, 80) #width 300 height 80 for start button
start_btn_rect.center = (640, 500) #center start button on screen

start_font = pygame.font.Font("Assets/Other/PressStart2P-Regular.ttf", 40)
title_font = pygame.font.Font("Assets/Other/PressStart2P-Regular.ttf", 60)

while True:
    keys = pygame.key.get_pressed() #get current all key presses
    if keys[pygame.K_DOWN]: #if down key pressed
        dinosaur.duck() #call duck method
    else:
        if dinosaur.ducking: #if currently ducking
            dinosaur.unduck() #call unduck method
# function: chef cooks, event: order from customer, timer: kitchen timer
# function: what to do, event: sign of what happens, timer: when it can happens
#timer > event > handling in loop > function

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and game_state == "menu": #mouse click event in menu state
            if start_btn_rect.collidepoint(event.pos): #if click is within start button rect
                game_state = "playing" #change game state to playing

        if event.type == pygame.QUIT: #quit event
            pygame.quit() #quit pygame
            sys.exit() #exit program

        if event.type == CLOUD_EVENT: #cloud spawn event
            current_cloud_y = random.randint(50, 300) #random y position for cloud
            current_cloud = Cloud(cloud_img, 1380, current_cloud_y) #create cloud object Cloud(image, x_pos, y_pos)
            cloud_group.add(current_cloud) #add cloud to cloud group

        if event.type == pygame.KEYDOWN: #key down event
            # ESC quit
            if event.key == pygame.K_ESCAPE: #if escape key pressed
                pygame.quit()
                sys.exit()

            # Jump + Restart logic
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP: #jump keys can with space or up arrow
                if game_state == "playing": # Only allow jump when playing
                    dinosaur.jump()

                    # Restart game when pressing jump after game over
                    if game_over: 
                        game_over = False #from game over to playing
                        game_speed = 3 #reset game speed
                        player_score = 0 #reset player score
                        obstacle_group.empty() #clear obstacles
                        ptero_group.empty() #clear pterodactyls
                        cloud_group.empty() #clear clouds
                        powerup_group.empty() #clear powerups
                        reset_powerups() #reset powerup states
                        all_sfx.play(loops=-1)  # restart backsound

    if game_state == "menu": #in menu state
        draw_menu() #draw menu screen

    elif game_state == "playing": #in playing state
        screen.blit(background_img, (0, 0)) #draw background image

        # Collision with obstacles (consider shield)
        hit = pygame.sprite.spritecollide(dino_group.sprite, obstacle_group, False) #check collision between dino and obstacles (cactus/ptero) and obstacles not removed on hit
        if hit: #check if there was a collision
            if not game_over: #only process if it is not in game over state
                if shield_active: #check if shield powerup is active
                    # if shield active, destroy the obstacle but do not end game
                    for o in hit: #for each collided obstacle (o means the shield)
                        o.kill() #remove obstacle from all groups and ram memory
                else:
                    game_over = True #set game over state to true
                    death_sfx.play() #play death sound effect
                    all_sfx.stop() #stop background music
                # HIGH SCORE UPDATE
                    if player_score > high_score: #if current score is greater than high score
                        high_score = int(player_score) #convert current player score to int and set as new high score
                    with open("highscore.txt", "w") as f: #open high score file in write mode
                        f.write(str(high_score)) #write new high score to file as string

        # Collision with other powerups except shield
        collected = pygame.sprite.spritecollide(dino_group.sprite, powerup_group, True) #check collision between dino and powerups, remove powerup on collection

        for pu in collected: # for each unknwon collected powerup
            # activate powerup
            now = pygame.time.get_ticks() #current time in milliseconds
            
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
                pickup_sfx.play() #play pickup sound effect if loaded

        # Update powerup timers
        t = pygame.time.get_ticks() #current time in milliseconds
        if shield_active and t >= shield_end_time: #if shield active and current time exceeds end time
            shield_active = False #deactivate shield
        if jump_boost_active and t >= jump_boost_end_time:
            jump_boost_active = False
        if double_points_active and t >= double_points_end_time:
            double_points_active = False

        # Game over display
        if game_over:
            end_game() #call end game function
        else:
            # game running logic
            game_speed += 0.001 # slowly accelerate (base speed)

            # points sound when hit 100s
            if round(player_score, 1) % 100 == 0 and int(player_score) > 0: #check if score is multiple of 100
                points_sfx.play() #play points sound effect

            # --- spawn cooldown logic ---
            # As speed increases, the cooldown time decreases to maintain density.
            BASE_COOLDOWN = 2000 #base (initial spawn time) cooldown in milliseconds
            MIN_COOLDOWN = 800 #minimum cooldown in milliseconds
        
            # Use game_speed as a factor. Current start speed is 3.
            speed_factor = max(1, game_speed / 3) #if the game is faster than spawn will be more often
            
            # Calculate the dynamic cooldown, ensuring it doesn't drop below MIN_COOLDOWN
            dynamic_cooldown = max(MIN_COOLDOWN, BASE_COOLDOWN / speed_factor) #pick higher value between min and calculated cooldown
            
            # Add a random variance to the dynamic cooldown, max 200ms
            spawn_delay = dynamic_cooldown + random.randint(0, 200) #add randomness to spawn delay so not feels robotic

            # obstacles spawn
            if pygame.time.get_ticks() - obstacle_timer >= spawn_delay: #check if current time minus last obstacle time exceeds dynamic cooldown
                # random chance for Cacti, Pterodactyls, or Powerups
                obstacle_random = random.randint(1, 70) #random number between 1 and 70
                if obstacle_random in range(1, 7): #1-6 spawn cactus
                    new_obstacle = Cactus(1280, 340) #create cactus object at position (1280, 340)
                    obstacle_group.add(new_obstacle) #add cactus to obstacle group
                    obstacle_timer = pygame.time.get_ticks() #reset obstacle timer to current time
                elif obstacle_random in range(7, 10): #7-9 spawn pterodactyl
                    new_obstacle = Ptero()
                    obstacle_group.add(new_obstacle)
                    obstacle_timer = pygame.time.get_ticks()
                elif obstacle_random in range(35, 38): 
                    # spawn a powerup instead
                    kind = random.choice(["shield", "jump", "double"])
                    # random y coordinate for powerup spawn
                    y_pos = random.choice([230, 250, 280])
                    new_powerup = Powerup(kind, x_pos=1280, y_pos=y_pos)
                    powerup_group.add(new_powerup)
                    obstacle_timer = pygame.time.get_ticks()

            # update score 
            if double_points_active: #if double points powerup is active
                player_score += 0.2 #increase score by 0.2 for double points
            else:
                player_score += 0.1 #normal score increase by 0.1

            score_surface = game_font.render(str(int(player_score)), True, "black") #render score surface
            screen.blit(score_surface, (1150, 10)) #draw score surface on screen at position (1150, 10) top right

            high_surface = game_font.render(f"HI {high_score}", True, "black") #render high score surface next to score
            screen.blit(high_surface, (950, 10)) #draw high score surface on screen

            # Update groups
            cloud_group.update() # update cloud positions so they move left
            cloud_group.draw(screen) # draw clouds on screen

            ptero_group.update() # update pterodactyl positions
            ptero_group.draw(screen) # draw pterodactyls on screen

            dino_group.update() # update dinosaur position and animation
            dino_group.draw(screen) # draw dinosaur on screen

            # Draw shield aura if active
            if shield_active:
                draw_shield_aura(dino_group.sprite)
            obstacle_group.update() # update obstacle positions
            obstacle_group.draw(screen) # draw obstacles on screen
            powerup_group.update() # update powerup positions
            powerup_group.draw(screen) # draw powerups on screen

            # Ground scroll
            ground_x -= game_speed #move ground left by game speed
            screen.blit(ground, (ground_x, 360)) #draw ground at current x position
            screen.blit(ground, (ground_x + 1280, 360)) #draw second ground image for seamless scroll
            if ground_x <= -1280: #if ground has fully scrolled offscreen
                ground_x = 0 #reset ground x position
    clock.tick(120) #limit FPS to 120 for smoother gameplay and not use too much CPU
    pygame.display.update() #update display and show all changes and drawings