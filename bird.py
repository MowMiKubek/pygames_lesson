import pygame

WIDTH, HEIGHT = 800, 600

BIRD_UP_IMG_PATH = "assets/birdup.png"
BIRD_DOWN_IMG_PATH = "assets/birddown.png"

bird_acceleration = .5
bird_max_speed = 15
bird_init_speed = 10
bird_max_angle = 30

bird_image = pygame.image.load(BIRD_UP_IMG_PATH)
bird_rect = bird_image.get_rect()
bird_rect.center = (WIDTH // 2, HEIGHT // 2)

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_up = pygame.image.load(BIRD_UP_IMG_PATH)
        self.image_down = pygame.image.load(BIRD_DOWN_IMG_PATH)
        self.image = self.image_up
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.gravity = bird_acceleration
        self.speed = -bird_init_speed
        self.max_speed = bird_max_speed

    def update(self):
        self.rect.y += self.speed

        if self.speed > 0:
            self.image = self.image_down
        else:
            self.image = self.image_up

        if self.speed < self.max_speed:
            self.speed += self.gravity

        if self.rect.y > HEIGHT:
            global GAME_RUNNING
            GAME_RUNNING = False

        if self.rect.y <= 0:
            self.speed = bird_init_speed // 5

    def draw(self, screen):
        angle = -bird_max_angle * self.speed / self.max_speed
        screen.blit(pygame.transform.rotate(self.image, angle), self.rect)

    def bounce(self):
        self.speed = -bird_init_speed