import pygame
import sys
import random

# 초기화
pygame.init()

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# 화면 크기 설정
screen_width = 500
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("블록 깨기 게임")

# 폰트 설정
small_font = pygame.font.SysFont(None, 36)
large_font = pygame.font.SysFont(None, 72)

# 게임 속도 조절을 위한 Clock 객체 생성
clock = pygame.time.Clock()

# 게임 상태 변수
score = 0
missed = 0
game_over = 0  # 게임 상태: 0-진행 중, 1-성공, 2-실패
SUCCESS = 1
FAILURE = 2

# 벽돌 초기화
bricks = []
COLUMN_COUNT = 8
ROW_COUNT = 7
for column_index in range(COLUMN_COUNT):
    for row_index in range(ROW_COUNT):
        brick = pygame.Rect(column_index * 70 + 10, row_index * (16 + 5) + 35, 60, 16)
        bricks.append(brick)

# 공 초기화
ball = pygame.Rect(screen_width // 2 - 16 // 2, screen_height // 2 - 16 // 2, 16, 16)
ball_dx = 5
ball_dy = -5

# 패들 초기화
paddle = pygame.Rect(screen_width // 2 - 80 // 2, screen_height - 16, 80, 16)
paddle_dx = 0

# 게임 루프
while True:
    # 게임 프레임 설정
    clock.tick(30)
    screen.fill(BLACK)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                paddle_dx = -10
            elif event.key == pygame.K_RIGHT:
                paddle_dx = 10
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                paddle_dx = 0

    # 패들 이동 및 화면 경계 검사
    paddle.left += paddle_dx
    if paddle.left < 0 or paddle.left > screen_width - paddle.width:
        paddle.left = max(0, min(paddle.left, screen_width - paddle.width))

    # 공 이동
    ball.left += ball_dx
    ball.top += ball_dy

    # 공의 화면 경계 검사
    if ball.left <= 0 or ball.left >= screen_width - ball.width:
        ball_dx = -ball_dx + random.uniform(-0.5, 0.5)  # -0.5 ~ +0.5 사이의 각도 랜덤 변형
    if ball.top < 0:
        ball_dy = -ball_dy + random.uniform(-0.5, 0.5)  # -0.5 ~ +0.5 사이의 각도 랜덤 변형
    elif ball.top >= screen_height:
        missed += 1
        ball.left = screen_width // 2 - ball.width // 2
        ball.top = screen_height // 2 - ball.width // 2
        ball_dy = -ball_dy

    # 놓친 공이 3개 이상이면 게임 오버
    if missed >= 3:
        game_over = FAILURE

    # 공과 벽돌 충돌 검사
    for brick in bricks:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_dy = -ball_dy + random.uniform(-0.5, 0.5)  # -0.5 ~ +0.5 사이의 각도 랜덤 변형
            deflection = random.randint(-10, 10)
            ball_dx += deflection / 10
            if ball_dx == 0:
                ball_dx = 1
            score += 1
            break

    # 공과 패들 충돌 검사
    if ball.colliderect(paddle):
        ball_dy = -ball_dy + random.uniform(-0.5, 0.5)  # -0.5 ~ +0.5 사이의 각도 랜덤 변형
        if ball_dx < 0 and ball.centerx > paddle.right or ball_dx > 0 and ball.centerx < paddle.left:
            ball_dx = -ball_dx

    # 벽돌을 모두 제거하면 성공
    if len(bricks) == 0:
        game_over = SUCCESS

    # 벽돌 그리기
    for brick in bricks:
        pygame.draw.rect(screen, GREEN, brick)

    # 게임 진행 중일 때 공과 패들 그리기
    if game_over == 0:
        pygame.draw.circle(screen, WHITE, (ball.centerx, ball.centery), ball.width // 2)
        pygame.draw.rect(screen, BLUE, paddle)

    # 점수와 놓친 공 수 표시
    score_image = small_font.render(f'Point {score}', True, YELLOW)
    screen.blit(score_image, (10, 10))

    missed_image = small_font.render(f'Missed {missed}', True, YELLOW)
    screen.blit(missed_image, missed_image.get_rect(right=screen_width - 10, top=10))

    # 게임 오버 메시지 표시
    if game_over > 0:
        if game_over == SUCCESS:
            success_image = large_font.render('성공', True, RED)
            screen.blit(success_image, success_image.get_rect(center=(screen_width // 2, screen_height // 2)))
        elif game_over == FAILURE:
            failure_image = large_font.render('실패', True, RED)
            screen.blit(failure_image, failure_image.get_rect(center=(screen_width // 2, screen_height)))