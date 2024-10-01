import pygame
from bird import Bird
from pipe import Pipe, create_pipe

pygame.init()
clock = pygame.time.Clock()

FPS = 60
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
GAME_RUNNING = True

BACKGROUND_PATH = "assets/bg.png"

pipes = pygame.sprite.Group()
pipes.add(create_pipe(WIDTH, 1))
pipes.add(create_pipe(WIDTH, 2))

bg_image = pygame.image.load(BACKGROUND_PATH)
bird = Bird()

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 72)
text_surface = my_font.render('Flippy Wings', False, (0, 0, 255))
text_gameover = my_font.render('GAME OVER', False, (0, 255, 0))

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


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(text_gameover, (WIDTH // 2 - text_surface.get_width() // 2, 0))
    pygame.display.flip()
    clock.tick(FPS)
