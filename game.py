# All credits to:
# Nintendo, GameFreak, Satoshi Tajiri and Ken Sugimori
# Tech With Tim from YouTube (coding tutorials), chi-u from DeviantArt(sprites),
# Forheksed from DeviantArt(background), SoundTeMP(music) and Chequered Ink(font)

import pygame, random
from pokemon import *
from pygame.locals import *

pygame.init() # initializes pygame module
pygame.display.init() # initializes display

size = 320, 240 # defines screen dimensions
screen = pygame.display.set_mode(size) # sets video mode for screen
pygame.display.set_caption('Pokérun') # displays the game name

clock = pygame.time.Clock() # sets a clock for events

background = pygame.image.load('forest.png').convert() # loads background image
background_x = 0 # sets starting horizontal position of background image 
background_x2 = background.get_width() # sets relative x for scrolling background

pygame.mixer.init() # initializes mixer
pygame.mixer.music.load('peaceful_forest.mp3') # loads background music
pygame.mixer.music.play() # plays background music

player = Player(60, 175, 'charmander') # creates a character for player

enemies = [] # creates a list to store enemies

pygame.time.set_timer(USEREVENT+2, random.randrange(3000, 5000)) # sets a timer for enemies spawning
pygame.time.set_timer(USEREVENT+1, 5000) # sets a timer for increasing speed
speed = 10 # sets speed of scrolling background and player

def write_score(): # function to save best score
    score_list = open('score.txt', 'r') # opens the score list file
    score_file = score_list.read() # reads the lines of file
    last_score_written = int(score_file[0]) # picks the first element of list

    if last_score_written < int(score): # compares best score with last score
        score_list.close() # closes the score list file
        score_file = open('score.txt', 'w') # opens and overwrite lines
        score_file.write(str(score)) # writes the last score
        score_file.close() # closes file

        return score # if the condition has been achieved

    return last_score_written # if hasn't

def detect_collision(player, enemy): # detects collision between player and enemies with hitboxes fixed
    if ((enemy.x + enemy.width) >= player.x >= enemy.x and ((enemy.y + 20) + enemy.height) >= player.y >= enemy.y): # player on the right and above enemy
        return True # collision has been detected
    if ((enemy.x + enemy.width) >= (player.x + player.width) >= enemy.x and ((enemy.y + 20) + enemy.height) >= player.y >= enemy.y): # player on the left and above enemy
        return True # collision has been detected
    return False # collision hasn't been detected

def game_over(): # starts when player collides with an enemy
    global game_loop, enemies, speed, score # accessing global variables
    enemies = [] # resets enemies
    speed = 10 # resets speed

    game_over_screen = True # opens game over screen
    while game_over_screen:
        pygame.time.delay(100) # delay for the loop
        for event in pygame.event.get(): # checks for events inside the loop
            if event.type == pygame.QUIT: # if player clicks on 'close' button
                pygame.quit() # it quits the game
            if event.type == pygame.MOUSEBUTTONDOWN: # if player clicks on screen
                game_over_screen = False # closes game over screen
                game_loop = True # restarts the game
        screen.fill((0,0,0), (0,0,320,240)) # fills the game over screen with black
        game_over_font = pygame.font.Font('Pocket Monk.otf', 30) # sets a font for messages
        game_over_message = game_over_font.render('Game over! ', 1, (255,255,0)) # sets game over message
        screen.blit(game_over_message, (100, 30)) # displays game over message on the screen
        best_score = game_over_font.render('Best score: ' + str(write_score()), 1, (255,255,0)) # sets best score message
        screen.blit(best_score, (35, 80)) # displays best score message on the screen
        new_score = game_over_font.render('New score: ' + str(score), 1, (255,255,0)) # sets new score message
        screen.blit(new_score, (35, 120)) # displays new score message on the screen
        press_space = game_over_font.render('Click to continue!', 1, (255,255,0)) # sets continue message
        screen.blit(press_space, (60, 180)) # displays continue message on the screen
        pygame.display.update() # displays everything setted

    score = 0 # resets score

score = 0 # sets score
game_loop = True # sets game loop
while game_loop:
    
    for event in pygame.event.get(): # checks for events inside the loop
        if event.type == pygame.QUIT: # if player clicks on 'close' button
            pygame.quit() # it quits the game
        if event.type == USEREVENT+1: # if timer reaches threshold
            speed += 1 # it increases speed
            score += 1 # it increases score
        if event.type == USEREVENT+2: # if timer reaches threshold
            random_enemy = random.randrange(0, 3) # it sorts an enemy id out
            if random_enemy == 0: # if id is 0
                enemies.append(Enemy(320, 175, 'bulbassaur')) # a bulbassaur spawns
            elif random_enemy == 1: # if id is 1
                enemies.append(Enemy(320, 175, 'pikachu')) # a pikachu spawns
            elif random_enemy == 2: # if id is 2
                enemies.append(Enemy(320, 175, 'squirtle')) # a squirtle spawns
        
    screen.blit(background, (background_x, 0)) # displays scrolling background
    screen.blit(background, (background_x2, 0)) # displays scrolling background

    score_font = pygame.font.Font('Pocket Monk.otf', 25) # sets a font for score
    score_message = score_font.render('Score: ' + str(score), 1, (0, 0, 0)) # sets score counter message
    screen.blit(score_message, (10, 10)) # displays score counter message on the screen

    for enemy in enemies: # analyzes enemies behavior
        if detect_collision(player, enemy): # detects collision between player and enemy
            game_over() # if so opens game over screen
        enemy.motion(screen, speed) # makes enemies move
        if enemy.x < enemy.width * -1: # if enemy reaches the end of screen
            enemies.pop(enemies.index(enemy)) # removes enemy from enemies list
        
    background_x -= speed # scrolling speed
    background_x2 -= speed # scrolling speed
    if background_x < background.get_width() * -1: # if background image reaches the end of the screen
        background_x = background.get_width() # it resets
    if background_x2 < background.get_width() * -1: # if background image reaches the end of the screen
        background_x2 = background.get_width() # it resets

    player.motion(screen) # makes player's character animation

    clock.tick(speed) # sets a speed for loop

    pygame.display.update() # displays everything setted
