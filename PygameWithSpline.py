import pygame
import numpy as np
from scipy.interpolate import CubicSpline
from CubicSpline import * 
import sys


# 우클릭: 키추가, 키를 
# Pygame 초기화
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
font = pygame.font.Font(None, 24)  

# 화면 중앙 좌표
center_x, center_y = width // 2, height // 2
# 데이터 포인트
points = [(0, height // 2), (width, height // 2)]
selected_point = None

# 데이터 포인트의 x, y 좌표 배열 생성
x = [p[0] for p in points]
y = [p[1] for p in points]
spline = CubicSpline(x, y)

# 스플라인과 가장 가까운 점을 찾아 그 위치에 새로운 포인트 추가
def add_point_at_position(pos):

    closest_distance = float('inf')
    closest_index = 0
    for i in range(len(points) - 1):
        p1, p2 = points[i], points[i + 1]
        dist = min_distance_to_segment(pos, p1, p2)
        if dist < closest_distance:
            closest_distance = dist
            closest_index = i
    points.insert(closest_index + 1, pos)

# 선분과 점 사이의 최소 거리 계산
def min_distance_to_segment(p, p1, p2):
    line_vec = np.array(p2) - np.array(p1)
    p1_to_p_vec = np.array(p) - np.array(p1)
    line_len_squared = np.dot(line_vec, line_vec)
    t = max(0, min(1, np.dot(p1_to_p_vec, line_vec) / line_len_squared))
    closest_point = np.array(p1) + t * line_vec
    dist = np.linalg.norm(np.array(p) - closest_point)
    
    return dist

# 그리드 및 숫자 표시 함수
def draw_grid_and_numbers():
    grid_color = (200, 200, 200)  # 회색
    grid_spacing = 50  # 그리드 간격

    # 수평선 그리기
    for y in range(0, height, grid_spacing):
        pygame.draw.line(screen, grid_color, (0, y), (width, y))
        text_surface = font.render(f'{height - y}', True, grid_color)
        screen.blit(text_surface, (5, y))

    # 수직선 그리기
    for x in range(0, width, grid_spacing):
        pygame.draw.line(screen, grid_color, (x, 0), (x, height))
        text_surface = font.render(f'{x}', True, grid_color)
        screen.blit(text_surface, (x, 5))

# 큐브 관련 변수
cube_size = 20
cube_position = None
moving = False
time_step = 0
time_speed = 0.1  # 시간의 흐름 속도

# 메인 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if event.button == 1:  # 좌클릭
                closest_point = min(points, key=lambda p: (p[0] - mouse_pos[0])**2 + (p[1] - mouse_pos[1])**2)
                if (closest_point[0] - mouse_pos[0])**2 + (closest_point[1] - mouse_pos[1])**2 < 100:  # 임계값 설정
                    selected_point = points.index(closest_point)
            elif event.button == 3:  # 우클릭
                add_point_at_position(mouse_pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            selected_point = None

        elif event.type == pygame.MOUSEMOTION and selected_point is not None:
            points[selected_point] = event.pos

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DELETE and selected_point is not None:
                del points[selected_point]
                selected_point = None
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                moving = not moving
                time_step = 0  # 시간 초기화
                
        # 스플라인에 따라 큐브 이동
    if moving:
        if time_step < len(spline_points):
            cube_position = spline_points[int(time_step)]
            time_step += time_speed
        else:
            moving = False  # 스플라인 끝에 도달하면 멈춤
  # 스플라인 재계산
    x = [p[0] for p in points]
    y = [height - p[1] for p in points]
    spline_points = NCS_Formula(x, y)
    spline_points = [(p[0], height - p[1]) for p in spline_points]


    # 화면 업데이트
    screen.fill((255, 255, 255))
    draw_grid_and_numbers()
    
    # 축 그리기
    pygame.draw.line(screen, (0, 0, 0), (center_x, 0), (center_x, height), 1)  # y축
    pygame.draw.line(screen, (0, 0, 0), (0, center_y), (width, center_y), 1)  # x축

    # 데이터 포인트 및 스플라인 그리기
    for i, p in enumerate(points):
        color = (255, 0, 0) if i != selected_point else (0, 123, 0)
        pygame.draw.circle(screen, color, p, 5)
        
        if i == selected_point:
            text_surface = font.render(f'{p[0]}, {height - p[1]}', True, (0, 0, 0))
            screen.blit(text_surface, (p[0] + 10, p[1] + 10))

    for i in range(len(spline_points) - 1):
        start_pos = spline_points[i]
        end_pos = spline_points[i + 1]
        pygame.draw.line(screen, (0, 0, 0), start_pos, end_pos, 2)

    if cube_position:
        pygame.draw.rect(screen, (0, 0, 255), (cube_position[0] - cube_size // 2, cube_position[1] - cube_size // 2, cube_size, cube_size))
        
    pygame.display.flip()

pygame.quit()