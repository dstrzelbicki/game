import pygame
import random

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((400, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

# Game variables
gravity = 0.5
bird_movement = 0
bird_pos = pygame.Vector2(100, 300)
bird_radius = 20

pipe_width = 70
pipe_gap = 200
pipe_velocity = 3
pipes = []
SPAWN_PIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWN_PIPE, 1500)

score = 0
game_active = True

def draw_bird():
    pygame.draw.circle(screen, "yellow", (int(bird_pos.x), int(bird_pos.y)), bird_radius)

def create_pipe():
    height = random.randint(100, 400)
    top_pipe = pygame.Rect(400, 0, pipe_width, height)
    bottom_pipe = pygame.Rect(400, height + pipe_gap, pipe_width, 600 - height - pipe_gap)
    return (
        {"rect": top_pipe, "passed": False, "type": "top"},
        {"rect": bottom_pipe, "passed": False, "type": "bottom"}
    )

def move_pipes(pipes):
    for pipe in pipes:
        pipe["rect"].centerx -= pipe_velocity
    return [pipe for pipe in pipes if pipe["rect"].right > 0]

def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, "green", pipe["rect"])

def check_collision(pipes):
    for pipe in pipes:
        if pipe["rect"].collidepoint(bird_pos.x, bird_pos.y):
            return False
    if bird_pos.y - bird_radius <= 0 or bird_pos.y + bird_radius >= 600:
        return False
    return True

def display_score(score):
    text = font.render(f"Score: {score}", True, "white")
    screen.blit(text, (10, 10))

# Game loop
running = True
while running:
    screen.fill("skyblue")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = -8
            if event.key == pygame.K_SPACE and not game_active:
                # Restart the game
                bird_pos = pygame.Vector2(100, 300)
                bird_movement = 0
                pipes.clear()
                score = 0
                game_active = True

        if event.type == SPAWN_PIPE and game_active:
            pipes.extend(create_pipe())

    if game_active:
        # Bird physics
        bird_movement += gravity
        bird_pos.y += bird_movement
        draw_bird()

        # Pipes
        pipes = move_pipes(pipes)
        draw_pipes(pipes)

        # Collision check
        game_active = check_collision(pipes)

        # Score logic (only top pipes)
        for pipe in pipes:
            if pipe["type"] == "top" and not pipe["passed"]:
                if pipe["rect"].right < bird_pos.x:
                    pipe["passed"] = True
                    score += 1

        display_score(score)

    else:
        # Game Over screen
        text = font.render("Game Over", True, "white")
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)
        display_score(score)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
