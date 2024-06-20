import pygame
import sys
import random

# 게임 초기화
pygame.init()

# 색상 정의
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 화면 크기 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pacman')

# 블록 크기 설정
block_size = 40

# 맵 데이터 정의
map_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# 팩맨 초기 위치 및 속도 설정
pacman_x = screen_width // 2
pacman_y = screen_height // 2
pacman_speed = 5

# 유령 클래스 정의
class Ghost:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def move(self):
        directions = ['up', 'down', 'left', 'right']
        direction = random.choice(directions)
        if direction == 'up' and self.y - self.speed >= 0:
            self.y -= self.speed
        elif direction == 'down' and self.y + self.speed < screen_height:
            self.y += self.speed
        elif direction == 'left' and self.x - self.speed >= 0:
            self.x -= self.speed
        elif direction == 'right' and self.x + self.speed < screen_width:
            self.x += self.speed

    def draw(self):
        pygame.draw.circle(screen, RED, (self.x, self.y), 20)

# 유령 초기화
ghosts = [
    Ghost(random.randint(0, screen_width), random.randint(0, screen_height), 3),
    Ghost(random.randint(0, screen_width), random.randint(0, screen_height), 3)
]

# 충돌 감지 함수
def detect_collision(x1, y1, x2, y2, size):
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return distance < size

# 맵 그리기 함수
def draw_map():
    for row in range(len(map_data)):
        for col in range(len(map_data[row])):
            if map_data[row][col] == 1:
                pygame.draw.rect(screen, BLUE, (col * block_size, row * block_size, block_size, block_size))
            elif map_data[row][col] == 2:
                pygame.draw.circle(screen, WHITE, (col * block_size + block_size // 2, row * block_size + block_size // 2), 5)

# 점수 아이템이 모두 먹혔는지 확인하는 함수
def all_items_collected():
    for row in map_data:
        if 2 in row:
            return False
    return True

# 점수 초기화
score = 0
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 72)

# 게임 루프
clock = pygame.time.Clock()
running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # 키 입력 처리
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            pacman_x -= pacman_speed
        if keys[pygame.K_RIGHT]:
            pacman_x += pacman_speed
        if keys[pygame.K_UP]:
            pacman_y -= pacman_speed
        if keys[pygame.K_DOWN]:
            pacman_y += pacman_speed

        # 벽 충돌 처리
        if map_data[pacman_y // block_size][pacman_x // block_size] == 1:
            if keys[pygame.K_LEFT]:
                pacman_x += pacman_speed
            if keys[pygame.K_RIGHT]:
                pacman_x -= pacman_speed
            if keys[pygame.K_UP]:
                pacman_y += pacman_speed
            if keys[pygame.K_DOWN]:
                pacman_y -= pacman_speed

        # 점수 아이템 먹기 처리
        if map_data[pacman_y // block_size][pacman_x // block_size] == 2:
            map_data[pacman_y // block_size][pacman_x // block_size] = 0
            score += 10

        # 모든 점수 아이템이 먹혔는지 확인
        if all_items_collected():
            game_over = True

        # 화면 채우기
        screen.fill(BLACK)

        # 맵 그리기
        draw_map()

        # 팩맨 그리기
        pygame.draw.circle(screen, YELLOW, (pacman_x, pacman_y), 20)

        # 유령 이동 및 그리기
        for ghost in ghosts:
            ghost.move()
            ghost.draw()
            # 충돌 감지
            if detect_collision(pacman_x, pacman_y, ghost.x, ghost.y, 40):
                print("Pacman was caught by a ghost!")
                running = False

        # 점수 표시
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

    else:
        # 클리어 메시지 표시
        screen.fill(BLACK)
        clear_text = game_over_font.render('clear', True, WHITE)
        screen.blit(clear_text, (screen_width // 2 - clear_text.get_width() // 2, screen_height // 2 - clear_text.get_height() // 2))

    # 화면 업데이트
    pygame.display.flip()

    # 프레임 속도 설정
    clock.tick(30)

pygame.quit()
sys.exit()