# (pygame: main library for), (os: use to check file like high score), (random: random cactus, cloud, powerups), (sys: to exit game
import pygame
import os
import sys
import random

pygame.init() #mandatory init pygame for activate all pygame modules

game_state = "menu" #determine game state in menu
high_score = 0 #set initial high score to 0

# load saved high score if exists and invalid then high score is 0
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as f:
        try:
            high_score = int(f.read()) #read file and change into integer
        except:
            high_score = 0 #if invalid content high score is 0

#screen
screen = pygame.display.set_mode((1280, 720)) #window size 1280x720
clock = pygame.time.Clock() #FPS control
pygame.display.set_caption("Dino LevelUp - Powerups") #window title

#font
game_font = pygame.font.Font("Assets/Other/PressStart2P-Regular.ttf", 24) #game font
start_font = pygame.font.Font("Assets/Other/PressStart2P-Regular.ttf", 40)
title_font = pygame.font.Font("Assets/Other/PressStart2P-Regular.ttf", 60)

# variables & state
game_speed = 3 #initial game speed
speed_multiplier = 1 # used for slow motion powerup (1 = constant speed at 3)
player_score = 0 #initial player score
game_over = False #initial game over state
obstacle_timer = 0 #timer for obstacle spawn
powerup_timer = 0 #timer for powerup spawn

# powerup states
shield_active = False 
shield_end_time = 0 #initial shield end time
jump_boost_active = False
jump_boost_end_time = 0
double_points_active = False
double_points_end_time = 0

# surfaces
ground = pygame.image.load("Assets/Other/Track.png") #load ground image
ground = pygame.transform.scale(ground, (1280, 20)) #scale ground image
ground_x = 0 #initial ground x position at left

cloud_img = pygame.image.load("Assets/Other/Cloud.png")
cloud_img = pygame.transform.scale(cloud_img, (200, 80))
background_img = pygame.image.load("Assets/Other/christmas_bg.png").convert()
background_img = pygame.transform.scale(background_img, (1280, 720))

# sounds
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
# all_sfx.play(loops=-1) # This will be called in main.py

# UI Rects
start_btn_rect = pygame.Rect(0, 0, 300, 80) #width 300 height 80 for start button
start_btn_rect.center = (640, 500) #center start button on screen

# events
CLOUD_EVENT = pygame.USEREVENT #custom event for cloud spawn
pygame.time.set_timer(CLOUD_EVENT, 2000) #set timer to trigger cloud event every 2000ms (2 seconds)