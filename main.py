import pygame

pygame.init()
clock = pygame.time.Clock()

FPS = 60
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

BIRD_IMG_PATH = "assets/birdup.png"

bird_acceleration = .2
bird_max_speed = 5
bird_init_speed = 3

bird_image = pygame.image.load(BIRD_IMG_PATH)
bird_rect = bird_image.get_rect()
bird_rect.center = (WIDTH // 2, HEIGHT // 2)


class Bird(pygame.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.gravity = bird_acceleration
        self.speed = bird_init_speed
        self.max_speed = bird_max_speed

    def update(self):
        self.rect.y += self.speed
        if self.speed < self.max_speed:
            self.speed += self.gravity

        if self.rect.y > HEIGHT:
            self.rect.y = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def bounce(self):
        self.speed = -bird_init_speed


bird = Bird(BIRD_IMG_PATH)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.bounce()

    # set background
    screen.fill((255, 255, 255))

    # move the bird
    bird.update()
    bird.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
