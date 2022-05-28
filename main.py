import pygame
from pygame.locals import *
from level1 import Level1
pygame.init()

clock = pygame.time.Clock()
fps = 60
tile_size = 30
game_over = 0

screen_width = 560
screen_height = 1100
screen = pygame.display.set_mode((screen_height, screen_width))
pygame.display.set_caption("Igra")
bg = pygame.image.load('img/fon2.jpg')
restart_img = pygame.image.load('img/restart.png')
start_img = pygame.image.load('img/start.png')
exit_img = pygame.image.load('img/exit.png')
main_menu = True


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):

        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button
        screen.blit(self.image, self.rect)

        return action

class Castle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/zamok-removebg-preview.png')
        self.image = pygame.transform.scale(img, (screen_width // 2 - 110, screen_height // 10 + 110))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.health = 5
    def draw(self):
        screen.blit(self.image, self.rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.enemies = []
        self.image = pygame.image.load('img/enemya.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.speed = 1
        self.move_direction = 1
        self.move_counter = 0
    def update(self):
        #enemy moves
        self.rect.x += self.speed
        self.rect.y += self.speed
        #ghost stops when it touch the castle
        if self.rect >= Level1.castle.rect:
            Level1.castle.health = Level1.castle.health - 1
            Level1.castle.health = Level1.castle.health
            self.speed = 0
        #ghost respawns
        if self.rect.bottom > screen_height:
            self.rect.x = screen_width // 2 - 120
            self.rect.y = screen_height // 2 - 500
            self.rect.x += self.speed
            self.rect.y += self.speed
            self.speed = 1
    def draw(self):
        screen.blit(self.image, self.rect)


class Enemy1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.enemies = []
        self.image = pygame.image.load('img/enemyb.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.speed = 1
        self.move_direction = 1
        self.move_counter = 0
    def update(self):
        #enemy moves
        self.rect.x += self.speed
        self.rect.y += self.speed
        #ghost stops when it touch the castle
        if self.rect >= Level1.castle.rect:
            Level1.castle.health = Level1.castle.health - 1
            Level1.castle.health = Level1.castle.health
            self.speed = 0
        #ghost respawns
        if self.rect.bottom > screen_height:
            self.rect.x = screen_width // 2 + 80
            self.rect.y = screen_height // 2 - 500
            self.rect.x += self.speed
            self.rect.y += self.speed
            self.speed = 1
    def draw(self):
        screen.blit(self.image, self.rect)

class Enemy2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/luchnika-removebg-preview.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1000
    def update(self):
        if self.rect.colliderect(player.rect):
            self.rect.y += self.speed
            self.rect.y = self.rect.y
    def draw(self):
        screen.blit(self.image, self.rect)


class Player():
    def __init__(self, x, y):
        self.reset(x, y)


    def update(self, game_over):

        dx = 0
        dy = 0
        walk_cooldown = 5

        if game_over == 0:

            #get key pressed

            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_a]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_d]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if key[pygame.K_a] == False and key[pygame.K_d] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            #handle animation

            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
                #if event.type == pygame.MOUSEBUTTONDOWN:
                    #if self.index >= 0:
                        #self.image = self.attack_image


            #add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            #check for collision
            self.in_air = True
            for tile in Level1.world.tile_list:
                #check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                #check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check for below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # check for above the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False


            #check for collision with walls of the screen
            if self.rect.left < 0 or self.rect.right > screen_height or self.rect.bottom > screen_height:
                self.rect.x = screen_width // 1.2
                self.rect.y = screen_height // 4

            #check for collision with enemy
            if self.rect.colliderect(Level1.enemy.rect):
                Level1.enemy.speed = 1000
                Level1.enemy.rect.y - Level1.enemy.speed
            #check for collision with enemy
            if self.rect.colliderect(Level1.enemy1.rect):
                Level1.enemy1.speed = 1000
                Level1.enemy1.rect.y - Level1.enemy1.speed


            #update player coordinates
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_image
            if self.rect.y > 200:
                self.rect.y -= 5


        #draw player
        screen.blit(self.image, self.rect)


        return game_over

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img_right = pygame.image.load(f'img/pers{num}.png')
            img_right = pygame.transform.scale(img_right, (30, 50))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load('img/ghost.png')
        self.attack_image = pygame.image.load('img/pers_s_mechom-removebg-preview.png')
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True
        self.clicked = False


class World():
    def __init__(self, data):
        self.tile_list = []

        #load images
        dirt_img = pygame.image.load('img/dirt.jpg')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                    if tile == 9:
                        img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * tile_size
                        img_rect.y = row_count * tile_size
                        tile = (img, img_rect)
                        self.tile_list.append(tile)

                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


start_button = Button(screen_width // 2 + 410, screen_height // 2 - 290, start_img)
exit_button = Button(screen_width // 2 - 150, screen_height // 2 - 290, exit_img)


run = True
while run:

    screen.blit(bg, (0, 0))


    if main_menu == True:
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
    else:
        Level1.vars.world.draw()

        Level1.castle.draw()

        Level1.enemy.draw()

        Level1.enemy1.draw()

        Level1.enemy2.draw()

        if game_over == 0:
            Level1.enemy.update()
            Level1.enemy1.update()
            Level1.enemy2.update()

        game_over = Level1.player.update(game_over)

        if game_over == -1:
            if Level1.restart_button.draw():
                Level1.player.reset(screen_width // 1.2, screen_height // 4)
                game_over = 0


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    pygame.display.update()
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()