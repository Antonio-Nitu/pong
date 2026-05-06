import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
PADDLE_SPEED = 5
BALL_SPEED = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 48)


class Paddle:
    W, H = 12, 80

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, self.W, self.H)

    def move(self, up, down):
        keys = pygame.key.get_pressed()
        # Fix C: move unconditionally then hard-clamp; old pre-move guard
        # allowed overshooting by up to PADDLE_SPEED-1 pixels past the wall.
        if keys[up]:
            self.rect.y -= PADDLE_SPEED
        if keys[down]:
            self.rect.y += PADDLE_SPEED
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)


class Ball:
    SIZE = 12

    def __init__(self):
        self._serve_dir = 1
        self.reset()

    def reset(self):
        self.rect = pygame.Rect(
            WIDTH // 2 - self.SIZE // 2,
            HEIGHT // 2 - self.SIZE // 2,
            self.SIZE, self.SIZE,
        )
        # Fix D: alternate serve direction so the ball goes toward the scorer.
        self._serve_dir *= -1
        self.vx = BALL_SPEED * self._serve_dir
        self.vy = BALL_SPEED

    def update(self, left_paddle, right_paddle):
        self.rect.x += self.vx
        self.rect.y += self.vy

        # Fix A: force correct sign with abs() and clamp position; old vy*=-1
        # left the ball past the wall where it would flip again next frame.
        if self.rect.top <= 0:
            self.vy = abs(self.vy)
            self.rect.top = 0
        elif self.rect.bottom >= HEIGHT:
            self.vy = -abs(self.vy)
            self.rect.bottom = HEIGHT

        # Fix B: direction guard prevents double-bounce when ball overlaps a
        # paddle across multiple frames; clamp position to end the overlap.
        if self.rect.colliderect(left_paddle.rect) and self.vx < 0:
            self.vx = abs(self.vx)
            self.rect.left = left_paddle.rect.right
        elif self.rect.colliderect(right_paddle.rect) and self.vx > 0:
            self.vx = -abs(self.vx)
            self.rect.right = right_paddle.rect.left

    def draw(self):
        pygame.draw.ellipse(screen, WHITE, self.rect)

    def out_of_bounds(self):
        # Fix E: ball must be fully off-screen before scoring.
        if self.rect.right < 0:
            return "right"
        if self.rect.left > WIDTH:
            return "left"
        return None


def draw_dashed_center():
    for y in range(0, HEIGHT, 20):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 1, y, 2, 10))


def main():
    left = Paddle(20, HEIGHT // 2 - Paddle.H // 2)
    right = Paddle(WIDTH - 20 - Paddle.W, HEIGHT // 2 - Paddle.H // 2)
    ball = Ball()
    scores = [0, 0]

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        left.move(pygame.K_w, pygame.K_s)
        right.move(pygame.K_UP, pygame.K_DOWN)
        ball.update(left, right)

        scorer = ball.out_of_bounds()
        if scorer:
            scores[0 if scorer == "left" else 1] += 1
            ball.reset()

        screen.fill(BLACK)
        draw_dashed_center()
        left.draw()
        right.draw()
        ball.draw()

        left_score = font.render(str(scores[0]), True, WHITE)
        right_score = font.render(str(scores[1]), True, WHITE)
        screen.blit(left_score, (WIDTH // 2 - 80, 20))
        screen.blit(right_score, (WIDTH // 2 + 50, 20))

        pygame.display.flip()


if __name__ == "__main__":
    main()
