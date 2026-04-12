
import pygame
import sys
import random
import time
import cv2
import mediapipe as mp

# 初始化pygame和mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# 初始化摄像头
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("无法打开摄像头")
    sys.exit()

pygame.init()

# 屏幕设置
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
GAME_WIDTH = 800
GAME_HEIGHT = 600

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)  # 分数文字颜色

# 创建屏幕
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("贪吃蛇游戏")

# 游戏区域
game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
info_surface = pygame.Surface((SCREEN_WIDTH - GAME_WIDTH, SCREEN_HEIGHT))

# 字体设置
font = pygame.font.SysFont('Arial', 30)

# 蛇的初始设置
snake_pos = [[100, 50], [90, 50], [80, 50]]
snake_speed = 10  # 每格大小
direction = 'RIGHT'
change_to = direction

# 果实设置
fruits = []
last_fruit_time = 0
fruit_interval = 20  # 20秒刷新一次

# 游戏状态
game_over = False
clock = pygame.time.Clock()
score = 0

def generate_fruits():
    """生成4个新果实"""
    global fruits
    fruits = []
    for _ in range(4):
        while True:
            x = random.randrange(20, GAME_WIDTH - 20, snake_speed)
            y = random.randrange(20, GAME_HEIGHT - 20, snake_speed)
            # 确保果实不靠近边缘
            if (20 < x < GAME_WIDTH - 20 and 
                20 < y < GAME_HEIGHT - 20 and
                [x, y] not in snake_pos):
                fruits.append([x, y])
                break

def draw_objects(direction_text=None):
    """绘制游戏对象"""
    game_surface.fill(WHITE)  # 游戏区域背景改为白色
    info_surface.fill(WHITE)
    
    # 显示分数
    score_text = font.render(f"Score: {score}", True, BLUE)
    game_surface.blit(score_text, (10, 10))
    
    # 处理摄像头画面
    ret, frame = cap.read()
    if ret:
        # 转换为RGB格式
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)
        
        # 手势识别
        results = hands.process(frame)
        
        # 绘制手势骨架
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        # 调整画面大小以适应右侧区域
        frame = cv2.resize(frame, (SCREEN_WIDTH - GAME_WIDTH, SCREEN_HEIGHT - 50))
        
        # 转换为pygame surface
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        info_surface.blit(frame_surface, (0, 0))
        
        # 显示方向文字
        if direction_text:
            text = font.render(f"Direction: {direction_text}", True, BLACK)
            info_surface.blit(text, (10, SCREEN_HEIGHT - 50))
    
    # 绘制蛇
    for pos in snake_pos:
        pygame.draw.rect(game_surface, GREEN, 
                         pygame.Rect(pos[0], pos[1], snake_speed, snake_speed))
    
    # 绘制果实
    for fruit in fruits:
        pygame.draw.rect(game_surface, RED, 
                         pygame.Rect(fruit[0], fruit[1], snake_speed, snake_speed))
    
    # 绘制到主屏幕
    screen.blit(game_surface, (0, 0))
    screen.blit(info_surface, (GAME_WIDTH, 0))

def check_collision():
    """检测碰撞"""
    global game_over
    
    # 检测墙壁碰撞
    head = snake_pos[0]
    if (head[0] < 0 or head[0] >= GAME_WIDTH or
        head[1] < 0 or head[1] >= GAME_HEIGHT):
        game_over = True
    
    # 检测自身碰撞
    if head in snake_pos[1:]:
        game_over = True

def show_game_over():
    """显示游戏结束界面"""
    font = pygame.font.SysFont('Arial', 50)
    text = font.render('Game Over', True, BLACK)
    restart_text = font.render('Restart', True, WHITE)
    
    # 计算文本位置
    text_rect = text.get_rect(center=(GAME_WIDTH//2, GAME_HEIGHT//2 - 50))
    restart_rect = restart_text.get_rect(center=(GAME_WIDTH//2, GAME_HEIGHT//2 + 50))
    
    # 绘制按钮背景
    pygame.draw.rect(game_surface, RED, restart_rect.inflate(20, 20))
    
    # 绘制文本
    game_surface.blit(text, text_rect)
    game_surface.blit(restart_text, restart_rect)
    screen.blit(game_surface, (0, 0))
    
    return restart_rect

# 主游戏循环
def main():
    global direction, change_to, last_fruit_time, game_over, snake_pos, score
    
    # 初始生成果实
    generate_fruits()
    last_fruit_time = time.time()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # 键盘控制
            # 移除键盘控制代码
        pass
        
        if not game_over:
            # 手势识别控制
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.flip(frame, 1)
                results = hands.process(frame)
                
                if results.multi_hand_landmarks:
                    hand_landmarks = results.multi_hand_landmarks[0]
                    
                    # 获取食指指尖(8)和指根(5)的坐标
                    fingertip = hand_landmarks.landmark[8]
                    fingerbase = hand_landmarks.landmark[5]
                    
                    # 计算方向向量
                    dx = fingertip.x - fingerbase.x
                    dy = fingertip.y - fingerbase.y
                    
                    # 确定主要方向
                    if abs(dx) > abs(dy):
                        change_to = 'RIGHT' if dx > 0 else 'LEFT'
                    else:
                        change_to = 'DOWN' if dy > 0 else 'UP'
            
            # 更新方向
            direction = change_to
            
            # 移动蛇
            head = snake_pos[0].copy()
            if direction == 'UP':
                head[1] -= snake_speed
            elif direction == 'DOWN':
                head[1] += snake_speed
            elif direction == 'LEFT':
                head[0] -= snake_speed
            elif direction == 'RIGHT':
                head[0] += snake_speed
            
            snake_pos.insert(0, head)
            
            # 检测是否吃到果实
            fruit_eaten = False
            for fruit in fruits[:]:
                if head == fruit:
                    fruits.remove(fruit)
                    fruit_eaten = True
                    score += 10  # 每吃一个果实加10分
                    break
            
            if not fruit_eaten:
                snake_pos.pop()
            
            # 定期刷新果实
            current_time = time.time()
            if current_time - last_fruit_time >= fruit_interval or not fruits:
                generate_fruits()
                last_fruit_time = current_time
            
            # 检测碰撞
            check_collision()
        
        # 绘制游戏
        draw_objects(change_to)
        
        if game_over:
            restart_rect = show_game_over()
            
            # 检测鼠标点击重新开始
            mouse_pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:  # 左键点击
                if restart_rect.collidepoint(mouse_pos):
                    # 重置游戏
                    game_over = False
                    snake_pos = [[100, 50], [90, 50], [80, 50]]
                    direction = 'RIGHT'
                    change_to = direction
                    score = 0  # 重置分数
                    generate_fruits()
                    last_fruit_time = time.time()
        
        pygame.display.flip()
        clock.tick(10)  # 控制游戏速度
    
    # 释放摄像头资源
    cap.release()
    hands.close()

if __name__ == "__main__":
    main()
