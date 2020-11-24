import pygame


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

