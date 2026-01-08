import pygame
import sys
import random
import config
from sprites import Cloud, Dino, Cactus, Ptero, Powerup

# groups (bundle draw, update, and collision for multiple sprites)
cloud_group = pygame.sprite.Group() 
obstacle_group = pygame.sprite.Group()
dino_group = pygame.sprite.GroupSingle()
powerup_group = pygame.sprite.Group()

# objects
dinosaur = Dino(50, 360) #create dinosaur object at position (50, 360)
dino_group.add(dinosaur) #add dinosaur to dino group

config.all_sfx.play(loops=-1) #play background music in loop

# functions
def end_game():
    game_over_text = config.game_font.render("Game Over!", True, "black") #render game over text
    game_over_rect = game_over_text.get_rect(center=(640, 300)) #center rect for game over text
    score_text = config.game_font.render(f"Score: {int(config.player_score)}", True, "black") #render score text
    score_rect = score_text.get_rect(center=(640, 340)) #center rect for score text
    config.screen.blit(game_over_text, game_over_rect) #draw game over text on screen
    config.screen.blit(score_text, score_rect) #draw score text on screen
    high_text = config.game_font.render(f"High Score: {config.high_score}", True, "black") #render high score text
    high_rect = high_text.get_rect(center=(640, 380)) #center rect for high score text
    config.screen.blit(high_text, high_rect) #draw high score text on screen


def reset_powerups():
    config.shield_active = False
    config.shield_end_time = 0
    config.jump_boost_active = False
    config.jump_boost_end_time = 0
    config.double_points_active = False
    config.double_points_end_time = 0
    
def draw_menu(): 
    config.screen.blit(config.background_img, (0, 0)) #draw background image

    # title
    title_surf = config.title_font.render("DINO LEVEL UP", True, (255, 255, 255)) #render title text
    title_rect = title_surf.get_rect(center=(640, 250))
    config.screen.blit(title_surf, title_rect)

    # start button
    pygame.draw.rect(config.screen, (200, 0, 0), config.start_btn_rect, border_radius=10)
    start_text = config.start_font.render("START", True, (255, 255, 255))
    start_rect = start_text.get_rect(center=config.start_btn_rect.center)
    config.screen.blit(start_text, start_rect)


def draw_shield_aura(sprite):
    # draw semi transparent circle around the dino to show shield exist
    aura_surf = pygame.Surface((sprite.rect.width*2, sprite.rect.height*2), pygame.SRCALPHA) #create transparent surface
    pygame.draw.circle(aura_surf, (0, 160, 255, 100), (aura_surf.get_width()//2, aura_surf.get_height()//2), max(sprite.rect.width, sprite.rect.height)) #draw semi-transparent blue circle
    config.screen.blit(aura_surf, (sprite.rect.centerx - aura_surf.get_width()//2, sprite.rect.centery - aura_surf.get_height()//2)) #blit aura centered on sprite blit is like overlay


# main Loop
while True:
    keys = pygame.key.get_pressed() #get current all key presses
    if keys[pygame.K_DOWN]: #if down key pressed
        dinosaur.duck() #call duck method
    else:
        if dinosaur.ducking: #if currently ducking
            dinosaur.unduck() #call unduck method

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and config.game_state == "menu": #mouse click event in menu state
            if config.start_btn_rect.collidepoint(event.pos): #if click is within start button rect
                config.game_state = "playing" #change game state to playing

        if event.type == pygame.QUIT: #quit event
            pygame.quit() #quit pygame
            sys.exit() #exit program

        if event.type == config.CLOUD_EVENT: #cloud spawn event
            current_cloud_y = random.randint(50, 300) #random y position for cloud
            current_cloud = Cloud(config.cloud_img, 1380, current_cloud_y) #create cloud object Cloud(image, x_pos, y_pos)
            cloud_group.add(current_cloud) #add cloud to cloud group

        if event.type == pygame.KEYDOWN: #key down event
            # ESC quit
            if event.key == pygame.K_ESCAPE: #if escape key pressed
                pygame.quit()
                sys.exit()

            # Jump + Restart logic
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP: #jump keys can with space or up arrow
                if config.game_state == "playing": # Only allow jump when playing
                    dinosaur.jump()

                    # Restart game when pressing jump after game over
                    if config.game_over: 
                        config.game_over = False #from game over to playing
                        config.game_speed = 3 #reset game speed
                        config.player_score = 0 #reset player score
                        obstacle_group.empty() #clear obstacles
                        cloud_group.empty() #clear clouds
                        powerup_group.empty() #clear powerups
                        reset_powerups() #reset powerup states
                        config.all_sfx.play(loops=-1)  # restart backsound

    if config.game_state == "menu": #in menu state
        draw_menu() #draw menu screen

    elif config.game_state == "playing": #in playing state
        config.screen.blit(config.background_img, (0, 0)) #draw background image

        # collision with obstacles (consider shield)
        hit = pygame.sprite.spritecollide(dino_group.sprite, obstacle_group, False) #check collision between dino and obstacles (cactus/ptero) and obstacles not removed on hit
        if hit: #check if there was a collision
            if not config.game_over: #only process if it is not in game over state
                if config.shield_active: #check if shield powerup is active
                    # if shield active, destroy the obstacle but do not end game
                    for o in hit: #for each collided obstacle (o means the shield)
                        o.kill() #remove obstacle from all groups and ram memory
                else:
                    config.game_over = True #set game over state to true
                    config.death_sfx.play() #play death sound effect
                    config.all_sfx.stop() #stop background music
                    # HIGH SCORE UPDATE
                    if config.player_score > config.high_score: #if current score is greater than high score
                        config.high_score = int(config.player_score) #convert current player score to int and set as new high score
                        with open("highscore.txt", "w") as f: #open high score file in write mode
                            f.write(str(config.high_score)) #write new high score to file as string

        # collision with other powerups except shield
        collected = pygame.sprite.spritecollide(dino_group.sprite, powerup_group, True) #check collision between dino and powerups, remove powerup on collection

        for pu in collected: # for each unknwon collected powerup
            # activate powerup
            now = pygame.time.get_ticks() #current time in milliseconds
            
            # all powerups last for 3 seconds (3000ms)
            POWERUP_DURATION = 3000
            if pu.kind == "shield":
                config.shield_active = True
                config.shield_end_time = now + POWERUP_DURATION
            elif pu.kind == "jump":
                config.jump_boost_active = True
                config.jump_boost_end_time = now + POWERUP_DURATION
            elif pu.kind == "double":
                config.double_points_active = True
                config.double_points_end_time = now + POWERUP_DURATION
            if config.pickup_sfx:
                config.pickup_sfx.play() #play pickup sound effect if loaded

        # update powerup timers
        t = pygame.time.get_ticks() #current time in milliseconds
        if config.shield_active and t >= config.shield_end_time: #if shield active and current time exceeds end time
            config.shield_active = False #deactivate shield
        if config.jump_boost_active and t >= config.jump_boost_end_time:
            config.jump_boost_active = False
        if config.double_points_active and t >= config.double_points_end_time:
            config.double_points_active = False

        # game over screen
        if config.game_over:
            end_game() #call end game function
        else:
            # game running logic
            config.game_speed += 0.001 # slowly accelerate (base speed)

            # points sound when hit 100s
            if round(config.player_score, 1) % 100 == 0 and int(config.player_score) > 0: #check if score is multiple of 100
                config.points_sfx.play() #play points sound effect

            # --- spawn cooldown logic ---
            BASE_COOLDOWN = 2000 #base (initial spawn time) cooldown in milliseconds
            MIN_COOLDOWN = 800 #minimum cooldown in milliseconds
            speed_factor = max(1, config.game_speed / 3) 
            dynamic_cooldown = max(MIN_COOLDOWN, BASE_COOLDOWN / speed_factor) 
            spawn_delay = dynamic_cooldown + random.randint(0, 200) 

            # obstacles spawn
            if pygame.time.get_ticks() - config.obstacle_timer >= spawn_delay:
                obstacle_random = random.randint(1, 70) 
                if obstacle_random in range(1, 7): #1-6 spawn cactus
                    new_obstacle = Cactus(1280, 340)
                    obstacle_group.add(new_obstacle)
                    config.obstacle_timer = pygame.time.get_ticks() 
                elif obstacle_random in range(7, 10): #7-9 spawn pterodactyl
                    new_obstacle = Ptero()
                    obstacle_group.add(new_obstacle)
                    config.obstacle_timer = pygame.time.get_ticks()
                elif obstacle_random in range(35, 38): 
                    kind = random.choice(["shield", "jump", "double"])
                    y_pos = random.choice([230, 250, 280])
                    new_powerup = Powerup(kind, x_pos=1280, y_pos=y_pos)
                    powerup_group.add(new_powerup)
                    config.obstacle_timer = pygame.time.get_ticks()

            # update score 
            if config.double_points_active:
                config.player_score += 0.2
            else:
                config.player_score += 0.1

            score_surface = config.game_font.render(str(int(config.player_score)), True, "black") 
            config.screen.blit(score_surface, (1150, 10)) 

            high_surface = config.game_font.render(f"HI {config.high_score}", True, "black") 
            config.screen.blit(high_surface, (950, 10)) 

            # Update groups
            cloud_group.update() 
            cloud_group.draw(config.screen) 

            obstacle_group.update() 
            obstacle_group.draw(config.screen) 

            dino_group.update() 
            dino_group.draw(config.screen) 

            # draw shield aura if active
            if config.shield_active:
                draw_shield_aura(dino_group.sprite)
            
            powerup_group.update() 
            powerup_group.draw(config.screen) 

            # ground scroll
            config.ground_x -= config.game_speed 
            config.screen.blit(config.ground, (config.ground_x, 360)) 
            config.screen.blit(config.ground, (config.ground_x + 1280, 360)) 
            if config.ground_x <= -1280: 
                config.ground_x = 0 
                
    config.clock.tick(120) 
    pygame.display.update()