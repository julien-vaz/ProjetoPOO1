import pygame

pygame.init() # initializes pygame module
pygame.display.init() # initializes display

size = 320, 240 # defines screen dimensions
screen = pygame.display.set_mode(size) # sets video mode for screen

class Pokemon: # creates a class for pokemons

    def __init__(self, x, y, name): # build method
        self.x = x # sets horizontal position for sprite image
        self.y = y # sets vertical position for sprite image
        self.width = 30 # sets width of sprite image
        self.height = 30 # sets height of sprite image
        self.running = True # sets running as a starting move for character
        self.sprite = [0] * 4 # creates a sprite animation with 4 frames
        self.sprite[0] = pygame.image.load(name + '3.png').convert() # loads 1st frame
        self.sprite[1] = pygame.image.load(name + '0.png').convert() # loads 2nd frame
        self.sprite[2] = pygame.image.load(name + '1.png').convert() # loads 3rd frame
        self.sprite[3] = pygame.image.load(name + '2.png').convert() # loads 4th frame
        self.character = self.sprite[0] # sets starting frame
        self.count = 0 # sets a frames counter
        self.jumping = False # sets character on the ground
        self.jump_animation = pygame.image.load(name + '_jump.png').convert() # loads jumping sprite
        self.jump_count = 0 # sets a jump counter
        self.jump_list = [30,15,10,5,1,1,-1,-1,-5,-10,-15,-30] # sets a list for vertical position changes while jumping
        
    def run(self, screen): # allows character animation
        if self.running == True: # checks if it is running
            if self.count == 3: # if counter reaches the end
                self.count = 0 # it resets
            else: # if doesn't
                self.count += 1 # it continues

            self.character = self.sprite[self.count] # animates character
            screen.blit(self.character, (self.x, self.y)) # displays animated character on the screen
            pygame.display.update() # displays everything setted

class Player(Pokemon): # creates a class for player

    def jump(self, screen): # allows player to jump
        self.running = False # stops the running animation
        self.character = self.jump_animation # starts jumping animation
        screen.blit(self.character, (self.x, self.y)) # displays animated character on the screen
        self.y -= self.jump_list[self.jump_count] # changes the vertical position
        self.jump_count += 1 # increases jump counter
        pygame.display.update() # displays everything setted
        if self.jump_count == len(self.jump_list): # checks if jumping animation has ended
            self.jump_count = 0 # if so it resets jump counter
            self.running = True # restarts running animation
            self.jumping = False # stops jumping animation

    def motion(self, screen): # controls player movement
        if pygame.key.get_pressed()[pygame.K_SPACE]: # if player presses spacebar
            self.jumping = True # starts jumping animation

        if self.jumping: # if character is jumping
            self.jump(screen)
        else: # or if it is running
            self.run(screen)

class Enemy(Pokemon): # creates a class for enemies

    def move(self, screen, speed): # allows character position changes
        self.x -= (speed * 2) # changes horizontal position

    def motion(self, screen, speed): # controls enemies movement
        self.run(screen) # animates enemies
        self.move(screen, speed) # move enemies position
