import pygame
import sys
from random import randrange, randint
from os import environ

environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

W_S, H_S = 1200, 800

lives = 3
num = 0
i = 0
speed_x = randint(6, 8)
speed_y = speed_y_start = randint(-8, -6)
block = 100

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

rect_size = w, h = 222, 70
rect_pos = ((W_S - w) // 2, ((H_S + h) // 2))

BG = pygame.image.load('img/bg.jpg')
bgs = BG.get_rect()

ball = pygame.image.load('img/ball.png')
ball_rect = ball.get_rect(center=((W_S // 2), (H_S - 81)))
ball_rect = ball_rect_start = ball.get_rect(
    center=((W_S // 2), (H_S - 51 - (ball_rect.h // 2))))

platform = pygame.image.load('img/platform1.png')
platform_rect = platform.get_rect(center=((W_S // 2), (H_S - 80)))
platform_rect.top = H_S - 50


def print_text(message, x, y, size):
    font = pygame.font.SysFont('Arial', size, True, False)
    text = font.render(message, True, (0, 0, 0))
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)


def again():
    return


class Button():
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.inactive_color = WHITE
        self.active_color = BLUE

    def blit(self, x, y, text, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.w and y < mouse[1] < y + self.h:
            self.rect = pygame.draw.rect(
                screen, self.active_color, (x, y, self.w, self.h))

            if click[0] == 1 and action is not None:
                action()

        else:
            pygame.draw.rect(
                screen, self.inactive_color, (x, y, self.w, self.h))

        font = pygame.font.SysFont('Arial', 50, True, False)
        text = font.render(text, True, (0, 0, 0))
        text_rect = text.get_rect(topleft=(x + 10, y + 6))
        screen.blit(text, text_rect)


# начальные установки для платформы и шара
def init():
    global i, ball_rect, platform_rect
    if i == 0:
        ball_rect = ball_rect_start = ball.get_rect(
            center=((W_S // 2), (H_S - 51 - (ball_rect.h // 2))))
        platform_rect = platform_rect_start = platform.get_rect(
            center=((W_S // 2), (H_S - 50)))
        platform_rect.top = H_S - 50


def move_and_stop():
    global ball_rect, i, speed_x, speed_y, BLACK
    global speed_y_start, block, platform_rect, lives
    button = Button(220, 70)
    print_text(f'Lives: {(lives)}', (W_S - 70), (H_S - 65), 30)
    if i <= block:
        ball_rect = ball_rect
    else:
        ball_rect = ball_rect.move(speed_x, speed_y)
    if ball_rect.top <= 0:
        speed_y = -speed_y
    if ball_rect.right >= W_S or ball_rect.left <= 0:
        speed_x = -speed_x
    if ball_rect.colliderect(platform_rect):
        speed_x = -speed_x
        speed_y = -speed_y
    if ball_rect.colliderect(platform_rect) and \
            ball_rect.bottom <= (platform_rect.bottom - 36):
        speed_x = -speed_x
    if ball_rect.bottom >= H_S:
        i = 0
        lives -= 1
    if lives <= 0:
        i = 0
        print_text('GAME OVER!', (W_S // 2), (H_S // 2), 50)
        button.blit((W_S - 220) // 2, ((H_S + 60) // 2), 'Play again', again)
        pygame.mouse.set_visible(True)


# основные установки
def run():
    global platform_rect, i, block, rect_pos, rect_size
    for e in pygame.event.get():
        if e.type == pygame.QUIT or \
                e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            sys.exit(0)
        elif e.type == pygame.MOUSEMOTION and i >= block:
            platform_rect.center = e.pos
            platform_rect.top = H_S - 50
            if platform_rect.right >= W_S:
                platform_rect.right = W_S
            if platform_rect.left <= 0:
                platform_rect.left = 0


# столкновение шара и кирпичей
def collide():
    global speed_y, ball_rect, num, rect1, BLUE, WHITE, BLACK
    collide1 = False
    hit_index = ball_rect.collidelist(block_list)
    print_text(f'Points: {(num)}', (W_S - 70), (H_S - 100), 30)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        hit_color = color_list.pop(hit_index)
        speed_y = -speed_y
        num += 1


def win():
    global i
    button = Button(222, 70)
    n = []
    if block_list == n:
        i = 0
        i -= 1
        print_text('YOU WON!', (W_S // 2), (H_S // 2), 50)
        button.blit((W_S - 220) // 2, ((H_S + 60) // 2), 'Play again', again)
        pygame.mouse.set_visible(True)


'____________________________ MAIN ____________________________'

pygame.display.set_caption('Cringe Арканоид')
screen = pygame.display.set_mode((W_S, H_S))
pygame.mouse.set_visible(False)
FPS = 60
clock = pygame.time.Clock()

# установка кирпичей
brick = pygame.image.load('img/brick0.png')
block_list = [pygame.Rect(
    10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
color_list = [(randrange(30, 256), randrange(
    30, 256), randrange(30, 256)) for i in range(10) for j in range(4)]

while True:
    i += 1  # задержка
    run()
    screen.blit(BG, bgs)
    # вывод кирпичей
    bricks = [pygame.draw.rect(screen, color_list[
        color], block) for color, block in enumerate(block_list)]
    screen.blit(ball, ball_rect)
    screen.blit(platform, platform_rect)
    move_and_stop()
    collide()
    init()
    win()
    pygame.display.update()
    clock.tick(FPS)
    pygame.display.set_caption(f'Cringe Арканоид{int(clock.get_fps())}')
