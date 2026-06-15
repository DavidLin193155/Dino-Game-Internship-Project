"""Dino Game in Python

A game similar to the famous Chrome Dino Game, built using pygame-ce.
Made by intern: @bassemfarid, no one or nothing else. 🤖
"""

import pygame
import random 
from random import randint


# Defining functions
def display_score():
    current_time = int((pygame.time.get_ticks() - start_time) / 100)
    score_surf = test_font.render(f'{current_time}',False,("white"))
    score_rect = score_surf.get_rect(center = (400,60))
    screen.blit(score_surf,score_rect)
    return current_time

def player_animation():
    global player_surf, player_index
    player_index += 0.025
    if player_index >= len(player_walk):
        player_index = 0
    player_surf = player_walk[int(player_index)]

def enemy_animation():
    global enemy_surf, enemy_index
    enemy_index += 0.025
    if enemy_index >= len(enemy_walk):
        enemy_index = 0
    enemy_surf = enemy_walk[int(enemy_index)]

def floater_animation():
    global floater_surf, floater_index
    floater_index += 0.125
    if floater_index >= len(floater_frames):
        floater_index = 0
    floater_surf = floater_frames[int(floater_index)]

def enemy_movement(enemy_list):
    if enemy_list:
        for enemy_rect in enemy_list:
            enemy_rect.x -= 5

            screen.blit(enemy_surf, enemy_rect)

            enemy_list = [enemy for enemy in enemy_list if enemy.x > -100]
        
        return enemy_list
    else: return []

def floater_movement(floater_list):
    if floater_list:
        for floater_rect in floater_list:
            floater_rect.x -= 5
            screen.blit(floater_surf, floater_rect)
        floater_list = [floater for floater in floater_list if floater.x > -100]
        return floater_list
    else:
        return []

# Initialize Pygame and create a window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
running = True  # Pygame main loop, kills pygame when False
enemies_nearby = False
test_font = pygame.font.Font("Strichpunkt Sans.ttf", 30)
warning_font = pygame.font.Font("Strichpunkt Sans.ttf", 35)
start_time = 0
score = 0
new_position = 0

# Load level assets
robotic_background_SURF = pygame.image.load("graphics/level/backgrounddd.png").convert()
GROUND_SURF = pygame.image.load("graphics/level/floorr.png").convert()
start_screen_surf = pygame.image.load("graphics/level/start screen.png").convert()
start_screen_surf = pygame.transform.scale(start_screen_surf, (800, 400))
game_font = pygame.font.Font(pygame.font.get_default_font(), 50)
#score_surf = game_font.render("SCORE?", False, "Black")
#score_rect = score_surf.get_rect(center=(400, 50))

# Game state variables
is_playing = False  # Whether in game or in menu
GROUND_Y = 300  # The Y-coordinate of the ground level
JUMP_GRAVITY_START_SPEED = -22  # The speed at which the player jumps
players_gravity_speed = 0  # The current speed at which the player falls

# Load sprite assets
player_walk_1 = pygame.image.load("graphics/player/walking sword down.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/player/walking sword up.png").convert_alpha()
player_walk_1 = pygame.transform.scale(player_walk_1, (95, 80))
player_walk_2 = pygame.transform.scale(player_walk_2, (95, 80))
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(bottomleft=(25, GROUND_Y))
player_block = pygame.image.load("graphics/player/blocking swords up.png").convert_alpha()
player_block = pygame.transform.scale(player_block, (95, 80))
is_blocking = False
enemy_walk_1 = pygame.image.load("graphics/enemy/robot_1.png").convert_alpha()
enemy_walk_2 = pygame.image.load("graphics/enemy/robot_2.png").convert_alpha()
enemy_walk_1 = pygame.transform.scale(enemy_walk_1, (65, 65))
enemy_walk_2 = pygame.transform.scale(enemy_walk_2, (65, 65))
enemy_walk = [enemy_walk_1, enemy_walk_2]
enemy_index = 0
enemy_surf = enemy_walk[enemy_index]
enemy_list = []
floater_frame_1 = pygame.image.load("graphics/enemy/floater_1.png").convert_alpha()
floater_frame_2 = pygame.image.load("graphics/enemy/floater_2.png").convert_alpha()
floater_frame_3 = pygame.image.load("graphics/enemy/floater_3.png").convert_alpha()
floater_frame_4 = pygame.image.load("graphics/enemy/floater_4.png").convert_alpha()
floater_frame_5 = pygame.image.load("graphics/enemy/floater_5.png").convert_alpha()
floater_frame_6 = pygame.image.load("graphics/enemy/floater_6.png").convert_alpha()
floater_frame_7 = pygame.image.load("graphics/enemy/floater_7.png").convert_alpha()
floater_frame_8 = pygame.image.load("graphics/enemy/floater_8.png").convert_alpha()
floater_frame_9 = pygame.image.load("graphics/enemy/floater_9.png").convert_alpha()
floater_frame_10 = pygame.image.load("graphics/enemy/floater_10.png").convert_alpha()
floater_frame_1 = pygame.transform.scale(floater_frame_1, (90, 90))
floater_frame_2 = pygame.transform.scale(floater_frame_2, (90, 90))
floater_frame_3 = pygame.transform.scale(floater_frame_3, (90, 90))
floater_frame_4 = pygame.transform.scale(floater_frame_4, (90, 90))
floater_frame_5 = pygame.transform.scale(floater_frame_5, (90, 90))
floater_frame_6 = pygame.transform.scale(floater_frame_6, (90, 90))
floater_frame_7 = pygame.transform.scale(floater_frame_7, (90, 90))
floater_frame_8 = pygame.transform.scale(floater_frame_8, (90, 90))
floater_frame_9 = pygame.transform.scale(floater_frame_9, (90, 90))
floater_frame_10 = pygame.transform.scale(floater_frame_10, (90, 90))
floater_frames = [floater_frame_1, floater_frame_2, floater_frame_3, floater_frame_4, floater_frame_5, floater_frame_6, floater_frame_7, floater_frame_8, floater_frame_9, floater_frame_10]
floater_index = 0
floater_list = []
floater_surf = floater_frames[floater_index]
laser_surf = pygame.image.load("graphics/enemy/laser.png").convert_alpha()
laser_list = []
background_x = 0
ground_x = 0

# Timer
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1500)
floater_timer = pygame.USEREVENT + 2
pygame.time.set_timer(floater_timer, 2500)
laser_timer = pygame.USEREVENT + 3
pygame.time.set_timer(laser_timer, 1500)

while running:
    # Poll for events
    for event in pygame.event.get():

        if event.type == enemy_timer and is_playing:
            new_position = randint(900, 1200)
            all_enemies = enemy_list + floater_list
            if not any(abs(new_position - e.x) < 260 for e in all_enemies):
                enemy_list.append(enemy_surf.get_rect(bottomleft=(new_position, GROUND_Y)))

        
        if event.type == floater_timer and is_playing and score >= 100:
            new_position = randint(900, 1200)
            all_enemies = enemy_list + floater_list
            if not any(abs(new_position - e.x) < 180 for e in all_enemies):
                floater_list.append(floater_surf.get_rect(bottomleft=(new_position, GROUND_Y - 100)))

        if event.type == laser_timer and score >= 200:
            new_position = randint(900, 1000)
            if not enemies_nearby:
                laser_list.append(laser_surf.get_rect(bottomleft=(new_position, GROUND_Y - 50)))
            
        # pygame.QUIT --> user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

        elif is_playing:
            # When player wants to jump by pressing SPACE
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
                or event.type == pygame.MOUSEBUTTONDOWN
            ) and player_rect.bottom >= GROUND_Y:
                players_gravity_speed = JUMP_GRAVITY_START_SPEED

            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                if player_rect.bottom >= GROUND_Y:
                    is_blocking = True
            if event.type == pygame.KEYUP and event.key == pygame.K_f:
                is_blocking = False

        elif score == 0:
            # When player wants to play again by pressing SPACE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                is_playing = True
                enemy_list.clear()
                floater_list.clear()
                start_time = pygame.time.get_ticks()
        else:
            # When player wants to play again by pressing SPACE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                is_playing = True
                enemy_list.clear()
                floater_list.clear()
                laser_list.clear()
                is_blocking = False
                enemies_nearby = False
                start_time = pygame.time.get_ticks()

    if is_playing:
        background_x -= 1
        ground_x -= 5
        if background_x <= -800:
            background_x = 0
        if ground_x <= -800:
            ground_x = 0

        # Blit the level assets
        screen.blit(robotic_background_SURF, (background_x, 0))
        screen.blit(robotic_background_SURF, (background_x + 800, 0))
        screen.blit(GROUND_SURF, (ground_x, GROUND_Y))
        screen.blit(GROUND_SURF, (ground_x + 800, GROUND_Y))
        #pygame.draw.rect(screen, "#c0e8ec", score_rect)
        #pygame.draw.rect(screen, "#c0e8ec", score_rect, 10)
        #screen.blit(score_surf, score_rect)
        score = display_score()
        enemies_nearby = any(e.x < 350 for e in enemy_list)

        if 100 <= score <= 120:
            floaters_spawn_surf = warning_font.render("FLOATERS ARE SPAWNING", False, "white")
            floaters_spawn_rect = floaters_spawn_surf.get_rect(center=(400, 120))
            screen.blit(floaters_spawn_surf, floaters_spawn_rect)

        if 200 <= score <= 220:
            lasers_spawn_surf = warning_font.render("THE ROBOTS ARE SHOOTING LASERS", False, "white")
            lasers_spawn_rect = lasers_spawn_surf.get_rect(center=(400, 120))
            screen.blit(lasers_spawn_surf, lasers_spawn_rect)

        # Adjust egg's horizontal location then blit it
        enemy_animation()
        floater_animation()
        
        # Adjust player's vertical location then blit it
        if is_blocking:
            screen.blit(player_block, player_rect)

        else:
            players_gravity_speed += 1
            player_rect.y += players_gravity_speed
            if player_rect.bottom > GROUND_Y:
                player_rect.bottom = GROUND_Y
                player_animation()
            screen.blit(player_surf, player_rect)

        # Enemy Movement
        enemy_list = enemy_movement(enemy_list)
        floater_list = floater_movement(floater_list)

        # When player collides with enemy, game ends
        for enemy_rect in enemy_list:
            if enemy_rect.colliderect(player_rect):
                is_playing = False

        for floater_rect in floater_list:
            if floater_rect.colliderect(player_rect):
                is_playing = False

        for laser_rect in laser_list:
            laser_rect.x -= 13
            screen.blit(laser_surf, laser_rect)
            laser_list = [laser for laser in laser_list if laser.x > -100]

        for laser_rect in laser_list:
            if laser_rect.colliderect(player_rect):
                if is_blocking:
                    laser_list.remove(laser_rect)
                else:
                    is_playing = False

    # When game is over, display game over message
    else:
        if score == 0:
                screen.blit(start_screen_surf, (0, 0))
        else:
            screen.fill("black")
            game_over_surf = test_font.render("GAME OVER", False, "red")
            game_over_rect = game_over_surf.get_rect(center = (400, 150))
            final_score_surf = test_font.render(f"Score: {score}", False, "red")
            final_score_rect = final_score_surf.get_rect(center = (400, 200))
            restart_surf = test_font.render("Play again?", False, "red")
            restart_rect = restart_surf.get_rect(center = (400, 250))
            screen.blit(game_over_surf, game_over_rect)
            screen.blit(restart_surf, restart_rect)
            screen.blit(final_score_surf, final_score_rect)
        

    # flip the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # Limits game loop to 60 FPS




    

pygame.quit()
