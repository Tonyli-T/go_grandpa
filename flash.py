import pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, K_SPACE, RLEACCEL
import random

# Setting up some important constants
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 800


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


# Setup for music and sounds. Defaults are good.
pygame.mixer.init()

# Initialize the pygame
pygame.init()

# Setting up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# # Set up the clock for a decent framerate
clock = pygame.time.Clock()

# Adding a background to the game
back = pygame.image.load("images/back.png")

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

# Creating the sprite groups
enemies = pygame.sprite.Group()
all_bullet = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Load and play background music
# Sound source: Chris Bailey - artist Tripnet
# License: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load("sound/Sky_dodge_theme.ogg")
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.5)

# Load and play the special effects
move_up_sound = pygame.mixer.Sound("sound/Jet_up.ogg")
move_down_sound = pygame.mixer.Sound("sound/Jet_down.ogg")
collision_sound = pygame.mixer.Sound("sound/Boom.ogg")
kill_sound = pygame.mixer.Sound("sound/kill.flac")

# Setting up the volume
move_down_sound.set_volume(0.8)
move_up_sound.set_volume(0.8)
collision_sound.set_volume(1.0)

# The main game loop
b = None
running = True
while running:
    # Add the background image
    screen.blit(back, (0, 0))

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

    pressed_keys = pygame.key.get_pressed()

    # Shooting the bullets
    if pressed_keys[K_SPACE]:
        b = Bullet(player)
        all_bullet.add(b)

    player.update(pressed_keys)
    enemies.update()

    # Updating the screen
    for entity in all_bullet:
        if entity is not None:
            entity.update()
            screen.blit(entity.surf, entity.rect)
        if pygame.sprite.spritecollideany(entity, enemies):
            entity.kill()
            # enemies.kill()
            kill_sound.play()
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Checking for collision between player and enemies
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        collision_sound.play()
        pygame.time.delay(500)
        running = False

    pygame.display.flip()

    # # Maintain the appropriate game speed
    clock.tick(10)

# All done! Stop and quit the mixer.
pygame.mixer.music.stop()
pygame.mixer.quit()

pygame.quit()
