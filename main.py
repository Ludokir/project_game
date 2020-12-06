import pygame
import sys
from random import randrange, randint

pygame.init()

W_S, H_S = 1200, 800

num = 0
i = 0
speed_x = randint(5, 7)
speed_y = speed_y_start = randint(-8, -6)
block = 350

BG = pygame.image.load('img/bg.jpg')
bgs = BG.get_rect()

ball = pygame.image.load('img/ball.png')
ball_rect = ball.get_rect(center=((W_S // 2), (H_S - 81)))
ball_rect = ball_rect_start = ball.get_rect(
    center=((W_S // 2), (H_S - 51 - (ball_rect.h // 2))))

platform = pygame.image.load('img/platform1.png')
platform_rect = platform.get_rect(center=((W_S // 2), (H_S - 80)))
platform_rect.top = H_S - 50


# начальные установки для платформы и шара
def init():
    global i, ball_rect, platform_rect
    if i == 0:
        ball_rect = ball_rect_start = ball.get_rect(
            center=((W_S // 2), (H_S - 51 - (ball_rect.h // 2))))
        platform_rect = platform_rect_start = platform.get_rect(
            center=((W_S // 2), (H_S - 50)))
        platform_rect.top = H_S - 50


# движение шара
def move():
    global ball_rect, i, speed_x, speed_y, speed_y_start, block, platform_rect
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


def run():
    global platform_rect, i, block
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


def collide():
    global speed_y, ball_rect, num
    hit_index = ball_rect.collidelist(block_list)
    font1 = pygame.font.SysFont('Arial', 30, True, False)
    text1 = font1.render(f'Очки: {(num)}', True, (176, 42, 43))
    text_rect1 = text1.get_rect(center=((W_S - 70), (H_S - 100)))
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        hit_color = color_list.pop(hit_index)
        speed_y = -speed_y
        num += 1
    screen.blit(text1, text_rect1)


def win():
    global i
    n = []
    font = pygame.font.SysFont('Arial', 50, True, False)
    text = font.render('YOU WON!', True, (176, 42, 43))
    text_rect = text.get_rect(center=((W_S // 2), (H_S // 2)))
    if block_list == n:
        i = 0
        i -= 1
        screen.blit(text, text_rect)


'____________________________ MAIN ____________________________'

pygame.display.set_caption('Cringe Арканоид')
screen = pygame.display.set_mode((W_S, H_S))
pygame.mouse.set_visible(False)
FPS = 120
clock = pygame.time.Clock()

brick = pygame.image.load('img/brick0.png')
block_list = [pygame.Rect(
    10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
color_list = [(randrange(30, 256), randrange(
    30, 256), randrange(30, 256)) for i in range(10) for j in range(4)]

while True:
    i += 1
    run()
    screen.blit(BG, bgs)
    bricks = [pygame.draw.rect(screen, color_list[
        color], block) for color, block in enumerate(block_list)]
    screen.blit(ball, ball_rect)
    screen.blit(platform, platform_rect)
    move()
    collide()
    init()
    win()
    pygame.display.update()
    clock.tick(FPS)
