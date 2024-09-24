import random

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

PIPE_UP_IMG_PATH = "assets/pipedown.png"
PIPE_DOWN_IMG_PATH = "assets/pipeup.png"

bird_acceleration = .5
bird_max_speed = 15
bird_init_speed = 10
bird_max_angle = 30

bird_image = pygame.image.load(BIRD_UP_IMG_PATH)
bird_rect = bird_image.get_rect()
bird_rect.center = (WIDTH // 2, HEIGHT // 2)

pipe_gap = 200
pipe_offset = 400
pipe_speed = 3


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


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x_position):
        super().__init__()
        self.image_up = pygame.transform.scale_by(pygame.image.load(PIPE_UP_IMG_PATH), 1.5)
        self.image_down = pygame.transform.scale_by(pygame.image.load(PIPE_DOWN_IMG_PATH), 1.5)
        self.rect_up = self.image_up.get_rect()
        self.rect_down = self.image_down.get_rect()

        self.rect_up.x = x_position
        self.rect_down.x = x_position

        self.randomize_height()

    def randomize_height(self):
        height_offset = random.randint(100, HEIGHT - 100)
        self.rect_up.y = height_offset - self.rect_down.height - pipe_gap // 2
        self.rect_down.y = height_offset + pipe_gap // 2

    def reset_pipe(self):
        self.randomize_height()
        self.rect_up.x = WIDTH + self.rect_down.width
        self.rect_down.x = WIDTH + self.rect_down.width

    def update(self):
        self.rect_up.x -= pipe_speed
        self.rect_down.x -= pipe_speed

        if self.rect_up.right < 0:
            self.reset_pipe()

    def draw(self, screen):
        screen.blit(self.image_up, self.rect_up)
        screen.blit(self.image_down, self.rect_down)


pipes = pygame.sprite.Group()
pipes.add(Pipe(WIDTH + pipe_offset))
pipes.add(Pipe(WIDTH + pipe_offset*2))

bg_image = pygame.image.load(BACKGROUND_PATH)
bird = Bird()

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 72)
text_surface = my_font.render('Flippy Wings', False, (0, 0, 255))

GAME_STARTED = False

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

    while not GAME_STARTED:
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    GAME_STARTED = True
        pygame.display.flip()
        clock.tick(FPS)

    # move the bird
    bird.update()
    pipes.update()

    bird.draw(screen)
    for pipe in pipes:
        pipe.draw(screen)

    for pipe in pipes:
        if bird.rect.colliderect(pipe.rect_up) or bird.rect.colliderect(pipe.rect_down):
            GAME_RUNNING = False

    pygame.display.flip()
    clock.tick(FPS)
