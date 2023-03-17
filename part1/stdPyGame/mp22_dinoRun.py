import pygame
import os
import random

pygame.init()

ASSETS = './stdPyGame/Assets/'
SCREEN_WIDTH = 1100     # 게임윈도우 넓이
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, 600))
icon = pygame.image.load('./stdPyGame/dinoRun.png')
pygame.display.set_icon(icon)

BG = pygame.image.load(os.path.join(f'{ASSETS}Other', 'Track.png'))

RUNNING = [pygame.image.load('./stdPyGame/Assets/Dino/DinoRun1.png'),
           pygame.image.load(f'{ASSETS}Dino/DinoRun2.png')]
DUCKING = [pygame.image.load(f'{ASSETS}Dino/DinoDuck1.png'),
           pygame.image.load(f'{ASSETS}Dino/DinoDuck2.png')]
JUMPING = pygame.image.load(f'{ASSETS}Dino/DinoJump.png')
# 구름 이미지
CLOUD = pygame.image.load(f'{ASSETS}Other/Cloud.png')
# 익룡 이미지
BIRD = [pygame.image.load(f'{ASSETS}Bird/Bird1.png'),
        pygame.image.load(f'{ASSETS}Bird/Bird2.png')]
# 선인장 이미지 로드 / 애니메이션을 위한게 아니라 선인장 종류가 세 개씩
LARGE_CACTUS = [pygame.image.load(f'{ASSETS}Cactus/LargeCactus1.png'),
                pygame.image.load(f'{ASSETS}Cactus/LargeCactus2.png'),
                pygame.image.load(f'{ASSETS}Cactus/LargeCactus2.png')]
SMALL_CACTUS = [pygame.image.load(f'{ASSETS}Cactus/SmallCactus1.png'),
                pygame.image.load(f'{ASSETS}Cactus/SmallCactus2.png'),
                pygame.image.load(f'{ASSETS}Cactus/SmallCactus2.png')]

class Dino: # 공룡 클래스
    X_POS = 80; Y_POS = 310; Y_POS_DUCK = 340 # 공룡 위치 변수  # Y다른 이유는 DUCK이미지 크기 다름을 고려
    JUMP_VEL = 9.0 # 점프 속도
    def __init__(self) -> None:
        self.run_img = RUNNING; self.duck_img = DUCKING; self.jump_img = JUMPING 
        self.dino_run = True; self.dino_duck = False; self.dino_jump = False    # 기본 공룡 상태: run

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL   # 점프속도 초기값 9.0
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()  # 이미지 사각형 정보
        self.dino_rect.x = self.X_POS   # 공룡 위치 설정
        self.dino_rect.y = self.Y_POS

    def update(self, userInput) -> None:
        if self.dino_run:
            self.run()
        elif self.dino_duck:
            self.duck()
        elif self.dino_jump:
            self.jump()

        if self.step_index >= 10: self.step_index = 0 # 애니메이션 스텝

        if userInput[pygame.K_UP] and not self.dino_jump:   # 점프
            self.dino_run = False
            self.dino_duck = False
            self.dino_jump = True
            self.dino_rect.y = self.Y_POS                   # 이게 없으면 공룡이 하늘로 날아감
        elif userInput[pygame.K_DOWN] and not self.dino_jump:   # 수구리
            self.dino_run = False
            self.dino_duck = True
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):   # 런
            self.dino_run = True
            self.dino_duck = False
            self.dino_jump = False

    def run(self):
        self.image = self.run_img[self.step_index // 5] # (0~9)//5 = 0 or 1
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def duck(self):
        self.image = self.duck_img[self.step_index // 5] # duck_img
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK  # duck이미지는 높이가 작으닌깐
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_rect:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:  # -9.0이 되면 점프 중단
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL   # 9.0으로 초기화

    def draw(self,SCREEN) -> None:
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

class Cloud: # 구름 클래스
    def __init__(self) -> None:
        self.x = SCREEN_WIDTH + random.randint(300, 500)    # 구름 등장 시간 랜덤으로 느리게
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self) -> None:
        self.x -= game_speed
        if self.x < -self.width:     # 화면밖으로 벗어나면
            self.x = SCREEN_WIDTH + random.randint(1300, 2000)
            self.y = random.randint(50, 100)
    
    def draw(self, SCREEN) -> None:
        SCREEN.blit(self.image, (self.x, self.y))

class Obstacle: # (조상) 장애물 클래스
    def __init__(self, image, type) -> None:
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH # 1100  

    def update(self) -> None:
        self.rect.x -= game_speed
        if self.rect.x <= -self.rect.width:      # 왼쪽 화면 밖으로 벗어나면    # - 가 없으면 공룡과 익룡 부딪힐 때 사라짐
            obstacles.pop()    # 장애물 리스트에서 하나 꺼내오기

    def draw(self, SCREEN) -> None:
        SCREEN.blit(self.image[self.type], self.rect)

class Bird(Obstacle):           # 장애물 클래스 상속클래스
    def __init__(self, image) -> None:
        self.type = 0           # 새는 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0          # 0번 이미지로 시작

    def draw(self, SCREEN) -> None:     # draw 재정의
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1

class LargeCactus(Obstacle):    # 장애물 클래스 상속클래스
    def  __init__(self, image) -> None:
        self.type = random.randint(0, 2)        # 큰 선인장은 세 개니까 하나를 고름
        super().__init__(image, self.type)
        self.rect.y = 300

class SmallCactus(Obstacle):    # 장애물 클래스 상속클래스
    def  __init__(self, image) -> None:
        self.type = random.randint(0, 2)        # 작은 선인장은 세 개니까 하나를 고름
        super().__init__(image, self.type)
        self.rect.y = 325

def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles       # 점수 글로벌에서 초기화
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0  # 게임점수
    run = True
    clock = pygame.time.Clock()
    dino = Dino()       # 공룡객체 생성
    cloud = Cloud()     # 구름객체 생성
    game_speed = 14
    obstacles = []   # 장애물 리스트
    
    font = pygame.font.Font(f'{ASSETS}NanumGothicBold.ttf', 20)     # 폰트 나눔고딕으로 변경

    # 함수 내 함수(점수표시)
    def score():        
        global points, game_speed
        points += 1
        if points % 100 == 0:       # 100, 200, 300, ... 올라가면
            game_speed += 1         # 속도 증가

        txtScore = font.render(f'SCORE : {points}', True, (83, 83, 83))     # 공룡색 - 회색
        txtRect = txtScore.get_rect()
        txtRect.center = (1000, 40)
        SCREEN.blit(txtScore, txtRect)


    # 함수 내 함수(배경그리기)
    def background():   # main() 함수에서만 쓰는 함수   # 땅바닥을 update, draw 동식에 해주는 함수
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()        # 2404
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))   # 0, 380 먼저 그림
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))   # 2404 + 0, 380   # 2D 게임은 두 번 그려야 그려짐
        if x_pos_bg <= -image_width:
            #SCREEN_WIDTH.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0

        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255,255,255))  # 배경 흰색
        userInput =  pygame.key.get_pressed()

        background()
        score()

        # 구름 먼저 그려야 공룡 위로 안 지나감
        cloud.draw(SCREEN)  # 구름 애니메이션
        cloud.update()      

        dino.draw(SCREEN)   # 공룡 그리기
        dino.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:       # 작은 선인장
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:       # 큰 선인장
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:       # 새
                obstacles.append(Bird(BIRD))

        for obs in obstacles:
            obs.draw(SCREEN)
            obs.update()
            
            # collision detection; 충돌감지
            if dino.dino_rect.colliderect(obs.rect):
                pygame.draw.rect(SCREEN, (255,0,0), dino.dino_rect, 3)

        clock.tick(30)
        pygame.display.update()

if __name__ == '__main__':
    main()
            
