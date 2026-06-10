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
    global egg_surf, enemy_index
    enemy_index += 0.025
    if enemy_index >= len(enemy_walk):
        enemy_index = 0
    egg_surf = enemy_walk[int(enemy_index)]

def enemy_movement(enemy_list):
    if enemy_list:
        for enemy_rect in enemy_list:
            enemy_rect.x -= 5

            screen.blit(enemy_surf, enemy_rect)

            enemy_list = [enemy for enemy in enemy_list if enemy.x > -100]
        
        return enemy_list
    else: return [] 

# Initialize Pygame and create a window
pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
running = True  # Pygame main loop, kills pygame when False
test_font = pygame.font.Font("Strichpunkt Sans.ttf", 30)
start_time = 0
score = 0

# Game state variables
is_playing = True  # Whether in game or in menu
GROUND_Y = 300  # The Y-coordinate of the ground level
JUMP_GRAVITY_START_SPEED = -22  # The speed at which the player jumps
players_gravity_speed = 0  # The current speed at which the player falls

# Load level assets
robotic_background_SURF = pygame.image.load("graphics/level/backgrounddd.png").convert()
GROUND_SURF = pygame.image.load("graphics/level/floorr.png").convert()
game_font = pygame.font.Font(pygame.font.get_default_font(), 50)
#score_surf = game_font.render("SCORE?", False, "Black")
#score_rect = score_surf.get_rect(center=(400, 50))

# Load sprite assets
player_walk_1 = pygame.image.load("graphics/player/walking sword down.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/player/walking sword up.png").convert_alpha()
player_walk_1 = pygame.transform.scale(player_walk_1, (95, 80))
player_walk_2 = pygame.transform.scale(player_walk_2, (95, 80))
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(bottomleft=(25, GROUND_Y))
enemy_walk_1 = pygame.image.load("graphics/enemy/robot_1.png").convert_alpha()
enemy_walk_2 = pygame.image.load("graphics/enemy/robot_2.png").convert_alpha()
enemy_walk_1 = pygame.transform.scale(enemy_walk_1, (65, 65))
enemy_walk_2 = pygame.transform.scale(enemy_walk_2, (65, 65))
enemy_walk = [enemy_walk_1, enemy_walk_2]
enemy_index = 0
enemy_surf = enemy_walk[enemy_index]
enemy_rect = enemy_surf.get_rect(bottomleft=(randint(900, 1200), GROUND_Y))
enemy_list = []
background_x = 0
ground_x = 0

# Timer
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1200)

while running:
    # Poll for events
    for event in pygame.event.get():
        if event.type == enemy_timer and is_playing:
            new_position = randint(900, 1200)
            if not any(abs(new_position - position.x) < 220 for position in enemy_list):
                enemy_list.append(enemy_surf.get_rect(bottomleft=(new_position, GROUND_Y)))
            
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
        else:
            # When player wants to play again by pressing SPACE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                is_playing = True
                enemy_list.clear()
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

        # Adjust egg's horizontal location then blit it
        enemy_animation()
        
        # Adjust player's vertical location then blit it
        players_gravity_speed += 1
        player_rect.y += players_gravity_speed
        if player_rect.bottom > GROUND_Y:
            player_rect.bottom = GROUND_Y
            player_animation() 
        screen.blit(player_surf, player_rect)

        # Enemy Movement
        enemy_list = enemy_movement(enemy_list)
        

        # When player collides with enemy, game ends
        for enemy_rect in enemy_list:
            if enemy_rect.colliderect(player_rect):
                is_playing = False

    # When game is over, display game over message
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
