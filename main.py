import pygame

pygame.init()
clock = pygame.time.Clock()

FPS = 60
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

BIRD_IMG_PATH = "assets/birdup.png"

bird_velocity = 3
bird_acceleration = .2

bird_image = pygame.image.load(BIRD_IMG_PATH)
bird_rect = bird_image.get_rect()
bird_rect.center = (WIDTH // 2, HEIGHT // 2)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = -5


    # set background
    screen.fill((255, 255, 255))

    # move the bird
    bird_rect.y += bird_velocity
    bird_velocity += bird_acceleration

    screen.blit(bird_image, bird_rect)

    pygame.display.flip()
    clock.tick(FPS)