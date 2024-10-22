import random
import pygame

PIPE_UP_IMG_PATH = "assets/pipedown.png"
PIPE_DOWN_IMG_PATH = "assets/pipeup.png"
WIDTH, HEIGHT = 800, 600


class Pipe(pygame.sprite.Sprite):
    pipe_gap = 200
    pipe_offset = 300
    pipe_speed = 3

    def __init__(self, x_position):
        super().__init__()
        self.image_up = pygame.transform.scale_by(pygame.image.load(PIPE_UP_IMG_PATH), 1.5)
        self.image_down = pygame.transform.scale_by(pygame.image.load(PIPE_DOWN_IMG_PATH), 1.5)
        self.rect_up = self.image_up.get_rect()
        self.rect_down = self.image_down.get_rect()

        self.rect_up.x = x_position
        self.rect_down.x = x_position

        self.scored = False

        self.randomize_height()

    def randomize_height(self):
        height_offset = random.randint(150, HEIGHT - 150)
        self.rect_up.y = height_offset - self.rect_down.height - self.pipe_gap // 2
        self.rect_down.y = height_offset + self.pipe_gap // 2

    def reset_pipe(self, x_position):
        self.randomize_height()
        self.rect_up.x = max(x_position, WIDTH)
        self.rect_down.x = max(x_position, WIDTH)
        self.scored = False

    def update(self):
        self.rect_up.x -= self.pipe_speed
        self.rect_down.x -= self.pipe_speed

    def draw(self, screen):
        screen.blit(self.image_up, self.rect_up)
        screen.blit(self.image_down, self.rect_down)


def create_pipe(width, n):
    return Pipe(width + Pipe.pipe_offset * n)
