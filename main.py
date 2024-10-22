import pygame
from bird import Bird
from pipe import create_pipe, Pipe

pygame.init()
clock = pygame.time.Clock()

FPS = 60
WIDTH, HEIGHT = 800, 600
BACKGROUND_PATH = "assets/bg.png"


DIFFICULTY_SETTINGS = {
    "Easy": {'pipe_gap': 200, 'pipe_offset': 300, 'pipe_speed': 3},
    "Medium": {'pipe_gap': 200, 'pipe_offset': 200, 'pipe_speed': 4},
    "Hard": {'pipe_gap': 150, 'pipe_offset': 200, 'pipe_speed': 5}
}

difficulty = "Easy"


def set_difficulty(diff):
    selected_difficulty = DIFFICULTY_SETTINGS[difficulty]
    Pipe.pipe_offset = selected_difficulty["pipe_offset"]
    Pipe.pipe_offset = selected_difficulty["pipe_gap"]
    Pipe.pipe_speed = selected_difficulty["pipe_speed"]

"""
    Somewhere in the code we call this function
"""
set_difficulty(difficulty)

GAME_RUNNING = True
GAME_STARTED = False
pipes = pygame.sprite.Group()
pipes.add([create_pipe(WIDTH, i) for i in range(WIDTH // Pipe.pipe_offset + 1)])
game_score = 0
bird = Bird()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Bird section
bg_image = pygame.image.load(BACKGROUND_PATH)

# Font section
pygame.font.init()
font_game_over = pygame.font.SysFont('Comic Sans MS', 72)
font_score = pygame.font.SysFont('comicsans', 40)
font_reset = pygame.font.SysFont('comicsans', 32)

welcome_text = font_game_over.render('Flippy Wings', False, (0, 0, 255))
text_gameover = font_game_over.render('GAME OVER', False, (0, 255, 0))


def reset_game():
    print("Reset game")
    global GAME_RUNNING, GAME_STARTED, pipes, game_score, bird
    GAME_RUNNING = True
    GAME_STARTED = False
    pipes = pygame.sprite.Group()
    pipes.add([create_pipe(WIDTH, i) for i in range(WIDTH // Pipe.pipe_offset + 1)])
    game_score = 0
    bird = Bird()


def handle_pipes(pipes):
    pipes_sorted = sorted(pipes, key=lambda pipe: pipe.rect_up.x)
    if pipes_sorted[0].rect_up.right < 0:
        pipes_sorted[0].reset_pipe(pipes_sorted[-1].rect_up.x + Pipe.pipe_offset)


def check_if_scored(pipes):
    score = 0
    for pipe in pipes.sprites():
        if pipe.rect_up.right < bird.rect.centerx and not pipe.scored:
            score += 1
            pipe.scored = True

    return score


while True:
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
            screen.blit(welcome_text, (WIDTH // 2 - welcome_text.get_width() // 2, 0))
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

        if bird.rect.bottom > HEIGHT:
            GAME_RUNNING = False

        game_score += check_if_scored(pipes)
        handle_pipes(pipes)

        text_score = font_score.render(f"score: {game_score}", False, (0, 0, 255))
        screen.blit(text_score, (0, 0))

        pygame.display.flip()
        clock.tick(FPS)

    score_submitting = True
    name = "Player"

    scores_list = []

    while True:
        did_reset = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if score_submitting:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        print("Submitting")
                        with open("leaderboard.txt", "a") as file:
                            file.write(f"{name} {game_score}\n")
                        with open("leaderboard.txt", "r") as file:
                            for line in file:
                                result = line.split(' ')
                                scores_list.append((result[0], int(result[1])))
                        scores_list.sort(key=lambda player: player[1], reverse=True)
                        score_submitting = False
                    elif event.key == pygame.K_BACKSPACE:
                        print("Backspace")
                        name = name[:-1]
                    elif event.key and event.unicode.isalnum():  # only letters and numbers
                        name += event.unicode
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        print("R key presssed")
                        reset_game()
                        did_reset = True
                    elif event.key == pygame.K_q:
                        quit(0)
        if did_reset:
            break

        screen.blit(bg_image, (0, 0))
        screen.blit(bg_image, (WIDTH // 2, 0))
        bird.draw(screen)
        for pipe in pipes:
            pipe.draw(screen)

        if not score_submitting:
            LEADERBOARD_COLOR = (255, 204, 0, 128)  # RGBA red green blue alpha [0 - 255]
            leaderboard_surface = pygame.Surface((WIDTH // 2, HEIGHT // 2), pygame.SRCALPHA)
            leaderboard_rect = leaderboard_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            leaderboard_surface.fill(LEADERBOARD_COLOR)

            for i, player in enumerate(scores_list[:3]):
                text_surface = font_score.render(f"{i+1}. {player[0]}: {player[1]}", False, (0, 0, 255))
                leaderboard_surface.blit(text_surface, (0, i * 45))

            if game_score < scores_list[:3][-1][1]:
                text_surface = font_score.render(f"Your score: {game_score}", False, (0, 0, 255))
                leaderboard_surface.blit(text_surface, (0, 180))

            text_surface = font_reset.render("R to reset or Q to quit", False, (0, 0, 255))
            leaderboard_surface.blit(text_surface, (0, 225))

            screen.blit(leaderboard_surface, leaderboard_rect)

        if score_submitting:
            name_text = font_score.render(name, False, (0, 0, 255))
            screen.blit(name_text, (WIDTH // 2 - name_text.get_rect().width // 2,
                                    HEIGHT // 2 - name_text.get_rect().height // 2))

        screen.blit(text_gameover, (WIDTH // 2 - text_gameover.get_width() // 2, 0))

        pygame.display.flip()
        clock.tick(FPS)
