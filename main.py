import pygame
import sys
from random import randrange, randint
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

W_S, H_S = 1200, 800

lives = 3
num = 0
i = 0
speed_x = speed_x_start = randint(15, 17)
speed_y = speed_y_start = randint(15, 17)
block = 100
b = False
block_menu = True
stop = False
collide1 = False
n = []

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

rect_size = w, h = 222, 70
rect_pos = ((W_S - w) // 2, ((H_S + h) // 2))

BG = pygame.image.load(os.path.join('bg.jpg'))
bgs = BG.get_rect()

ball = pygame.image.load(os.path.join('ball.png'))
ball_rect = ball.get_rect(center=((W_S // 2), (H_S - 81)))
ball_rect = ball_rect_start = ball.get_rect(
    center=((W_S // 2), (H_S - 51 - (ball_rect.h // 2))))

platform = pygame.image.load(os.path.join('platform1.png'))
platform_rect = platform.get_rect(center=((W_S // 2), (H_S - 80)))
platform_rect.top = H_S - 50


def print_text(message, x, y, size):
    font = pygame.font.SysFont('Arial', size, True, False)
    text = font.render(message, True, (0, 0, 0))
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)


def delay():
    global block_menu, stop
    stop = True
    block_menu = False


def qui():
    sys.exit(0)


def start():
    global b, i, block_list, color_list, lives, num, speed_x, speed_y
    b = True
    if lives == 0:
        num = 0
        speed_x = speed_x_start
        speed_y = speed_y_start
        lives = 3
    else:
        speed_y = speed_y * 1.5
        speed_x = speed_x * 1.5
    block_list = [pygame.Rect(
        10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(
            10) for j in range(4)]
    color_list = [(randrange(30, 256), randrange(
        30, 256), randrange(30, 256)) for i in range(10) for j in range(4)]


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

        font = pygame.font.SysFont('Arial', 40, True, False)
        text = font.render(text, True, (0, 0, 0))
        text_rect = text.get_rect(center=(x + w // 2, y + h // 2))
        screen.blit(text, text_rect)


'____________________________ MAIN ____________________________'

button = Button(220, 70)

pygame.display.set_icon(pygame.image.load('ball.ico'))
pygame.display.set_caption('Арканоид')
screen = pygame.display.set_mode((W_S, H_S))
FPS = 60
clock = pygame.time.Clock()

block_list = [pygame.Rect(
    10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
color_list = [(randrange(30, 256), randrange(
    30, 256), randrange(30, 256)) for i in range(10) for j in range(4)]

while True:
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
    screen.blit(BG, bgs)
    bricks = [pygame.draw.rect(screen, color_list[
        color], block) for color, block in enumerate(block_list)]
    if block_menu:
        button.blit((W_S - 220) // 2, ((H_S + 60) // 2), 'Start game', delay)
        button.blit((W_S - 220) // 2, ((H_S + 230) // 2), 'Quit', qui)
    if stop:
        i += 1
    if i == 101:
        b = False
    screen.blit(ball, ball_rect)
    screen.blit(platform, platform_rect)
    print_text(f'Lives: {(lives)}', (W_S - 70), (H_S - 65), 30)
    if i <= block:
        ball_rect = ball_rect
    else:
        ball_rect = ball_rect.move(speed_x, speed_y)
    if ball_rect.top <= 5:
        speed_y = -speed_y
    if ball_rect.right >= W_S or ball_rect.left <= 0:
        speed_x = -speed_x
    if ball_rect.colliderect(platform_rect):
        speed_y = -speed_y
        speed_x = -speed_x
    if ball_rect.colliderect(platform_rect) and \
            ball_rect.bottom <= (platform_rect.bottom - 10):
        speed_x = -speed_x
    if ball_rect.bottom >= H_S:
        i = 0
        lives -= 1
    if lives == 0 and not b:
        i = 0
        print_text('GAME OVER!', (W_S // 2), (H_S // 2), 50)
        print_text(f'You score: {num}', (W_S // 2), ((H_S + 430) // 2), 50)
        button.blit((W_S - 220) // 2, ((H_S + 60) // 2), 'Play again', start)
        button.blit((W_S - 220) // 2, ((H_S + 230) // 2), 'Quit', qui)
    hit_index = ball_rect.collidelist(block_list)
    print_text(f'Points: {(num)}', (W_S - 70), (H_S - 100), 30)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        hit_color = color_list.pop(hit_index)
        speed_y = -speed_y
        num += 1
    if i == 0:
        ball_rect = ball_rect_start = ball.get_rect(
            center=((W_S // 2), (H_S - 51 - (ball_rect.h // 2))))
        platform_rect = platform_rect_start = platform.get_rect(
            center=((W_S // 2), (H_S - 50)))
        platform_rect.top = H_S - 50
    if block_list == n and not b:
        i = 0
        i -= 1
        print_text('YOU WON!', (W_S // 2), (H_S // 2), 50)
        print_text(f'You score: {num}', (W_S // 2), ((H_S + 430) // 2), 50)
        button.blit((W_S - 220) // 2, ((H_S + 60) // 2), 'Сontinue?', start)
        button.blit((W_S - 220) // 2, ((H_S + 230) // 2), 'Quit', qui)
    pygame.display.update()
    clock.tick(FPS)
