import pygame

pygame.init()
clock = pygame.time.Clock()

FPS = 60
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
GAME_RUNNING = True

BACKGROUND_PATH = "assets/bg.png"
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
        self.speed = bird_init_speed
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


bg_image = pygame.image.load(BACKGROUND_PATH)
bird = Bird()

while GAME_RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.bounce()

    # set background
    screen.blit(bg_image, (0, 0))
    screen.blit(bg_image, (WIDTH // 2, 0))

    # move the bird
    bird.update()
    bird.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
