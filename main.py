import pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, K_SPACE, RLEACCEL
import random
import sprite
from music_setting import bullet_sound, move_down_sound, move_up_sound, turning_sound, collision_sound

# Setting up some important constants
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 800
green = (0, 255, 0)
blue = (0, 0, 128)


# Create the enemy class
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super(Boss, self).__init__()
        self.surf = pygame.transform.scale(pygame.image.load("images/boss.png").convert(), (200, 200))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                SCREEN_WIDTH,
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed - 20, 0)
        if self.rect.right < 0:
            self.kill()


# Create the enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.transform.scale(pygame.image.load("images/2.png").convert(), (50, 50))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                SCREEN_WIDTH,
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed - 20, 0)
        if self.rect.right < 0:
            self.kill()


# Create the player class by inheriting the pregame sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.transform.scale(pygame.image.load("images/1.png").convert(), (100, 100))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.p_pos_x = 0
        self.p_pos_y = 0

    # A method that updates the player's position
    def update(self, p):
        # "and self.rect.top > 0"
        if p[K_UP]:
            move_up_sound.play()
            self.p_pos_y -= 50
            self.rect.move_ip(0, -50)
            return -50
        if p[K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            move_down_sound.play()
            self.p_pos_y += 50
            self.rect.move_ip(0, 50)
        if p[K_LEFT] and self.rect.left > 0:
            self.p_pos_x -= 50
            self.rect.move_ip(-50, 0)
        if p[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.p_pos_x += 50
            self.rect.move_ip(50, 0)

    # A method that returns player's position
    def pos(self):
        return self.p_pos_x, self.p_pos_y


# Create the missile class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, p):
        super(Bullet, self).__init__()
        self.surf = pygame.transform.scale(pygame.image.load("images/bullet.png").convert(), (70, 70))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=p.pos()
        )

    def update(self):
        self.rect.move_ip(100, 0)
        if self.rect.right >= SCREEN_WIDTH:
            self.kill()


# Initialize the pygame
pygame.init()

# set the pygame window name
pygame.display.set_caption('Go Grandpa! Go Corona!')

# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font
font = pygame.font.Font('freesansbold.ttf', 32)

# Setting up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# # Set up the clock for a decent framerate
clock = pygame.time.Clock()

# Adding a background to the game
back = pygame.image.load("images/back.png")

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDBOSS = pygame.USEREVENT + 2
pygame.time.set_timer(ADDBOSS, 1000)

# Creating the sprite groups
enemies = pygame.sprite.Group()
all_bullet = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# The main game loop
killed_people = 0
bullet_limit = 1
b = None
running = True
while running:
    # create a text suface object,
    # on which text is drawn on it.

    text = font.render(f'You have killed: {killed_people} People', True, green, blue)

    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()

    # set the center of the rectangular object.
    textRect.center = (SCREEN_WIDTH - 500, 50)

    # Add the background image
    screen.blit(back, (0, 0))
    # copying the text surface object
    # to the display surface object
    # at the center coordinate.
    screen.blit(text, textRect)

    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        # Did the user close the window?
        elif event.type == pygame.QUIT:
            running = False
        # Adding new enemies
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            # Adding new enemies
        elif event.type == ADDBOSS:
            new_enemy = Boss()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    pressed_keys = pygame.key.get_pressed()

    # Shooting the bullets
    if pressed_keys[K_SPACE] and bullet_limit == 1:
        bullet_limit -= 1
        b = Bullet(player)
        all_bullet.add(b)

    player.update(pressed_keys)
    enemies.update()

    # Updating the screen
    for entity in all_bullet:
        if entity is not None:
            bullet_sound.play()
            entity.update()
            screen.blit(entity.surf, entity.rect)
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Checking for collision between player and enemies
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        collision_sound.play()
        pygame.time.delay(250)
        running = False
    # Checking collision between enemy group and bullet group
    if pygame.sprite.groupcollide(all_bullet, enemies, True, True):
        killed_people += 1
        turning_sound.play()
        bullet_limit += 1

    pygame.display.flip()

    # # Maintain the appropriate game speed
    clock.tick(10)

pygame.quit()
