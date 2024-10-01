import pygame
from bird import Bird
from pipe import Pipe, create_pipe

pygame.init()
clock = pygame.time.Clock()

FPS = 60
WIDTH, HEIGHT = 800, 600
GAME_RUNNING = True
GAME_STARTED = False

BACKGROUND_PATH = "assets/bg.png"

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Pipes section
pipes = pygame.sprite.Group()
pipes.add(create_pipe(WIDTH, 1))
pipes.add(create_pipe(WIDTH, 2))

# Bird section
bg_image = pygame.image.load(BACKGROUND_PATH)
bird = Bird()

# Font section
pygame.font.init()
font_game_over = pygame.font.SysFont('Comic Sans MS', 72)
font_score = pygame.font.SysFont('comicsans', 48)

text_surface = font_game_over.render('Flippy Wings', False, (0, 0, 255))
text_gameover = font_game_over.render('GAME OVER', False, (0, 255, 0))

score = 0
number_of_pipes_on_the_right = 2

def check_if_scored(pipes):
    global number_of_pipes_on_the_right
    n = 0
    score = 0
    for pipe in pipes.sprites():
        if pipe.rect_up.right > WIDTH // 2:
            n += 1

    if n < number_of_pipes_on_the_right:
        score = 1

    number_of_pipes_on_the_right = n
    return score


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

    score += check_if_scored(pipes)

    text_score = font_score.render(f"score: {score}", False, (0, 0, 255))
    screen.blit(text_score, (0, 0))

    pygame.display.flip()
    clock.tick(FPS)


score_submitting = True
name = "Player"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if score_submitting:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print("Submitting")
                    with open("leaderboard.txt", "a") as file:
                        file.write(f"{name} {score}\n")
                    score_submitting = False
                elif event.key == pygame.K_BACKSPACE:
                    print("Backspace")
                    name = name[:-1]
                else:
                    name += event.unicode


    screen.blit(bg_image, (0, 0))
    screen.blit(bg_image, (WIDTH // 2, 0))
    bird.draw(screen)
    for pipe in pipes:
        pipe.draw(screen)

    name_text = font_score.render(name, False, (0, 0, 255))
    screen.blit(text_gameover, (WIDTH // 2 - text_surface.get_width() // 2, 0))
    screen.blit(name_text, (WIDTH // 2 - name_text.get_rect().width // 2, HEIGHT // 2 - name_text.get_rect().height // 2))

    pygame.display.flip()
    clock.tick(FPS)
