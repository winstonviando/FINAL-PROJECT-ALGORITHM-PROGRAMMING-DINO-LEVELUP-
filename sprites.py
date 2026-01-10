import pygame
import random
import config

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
        # jump allowed only if on ground (prevent double jump click)
        if self.rect.centery >= 360:
            config.jump_sfx.play() #play jump sound effect
            # Jump height depends on jump boost
            if config.jump_boost_active:
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
        self.x_pos -= config.game_speed * config.speed_multiplier #move left by game speed and increase with speed multiplier
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
        self.x_pos -= config.game_speed * config.speed_multiplier #move left by game speed and increase with speed multiplier
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
        self.x_pos -= config.game_speed * config.speed_multiplier #move left by game speed and increase with speed multiplier
        self.rect.centerx = self.x_pos
        if self.rect.right < -50:
            self.kill()