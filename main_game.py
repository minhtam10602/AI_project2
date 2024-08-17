import pygame
import sys
from collections import deque

# Import các lớp Program và Agent từ file hiện tại (cần thay thế bằng tên file gốc của bạn)
from main.py import Program, Agent  # Thay 'your_existing_file' bằng tên file hiện tại

# Khởi tạo Pygame
pygame.init()

# Thiết lập màn hình hiển thị
screen_size = 600  # Kích thước của cửa sổ
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("Agent Game")

# Đặt màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Khởi tạo chương trình với bản đồ từ tệp 'map1.txt'
program = Program('map1.txt')

# Thiết lập kích thước ô lưới
cell_size = screen_size // program.grid_size

def draw_grid():
    """Vẽ lưới và các vật thể trên bản đồ."""
    for row in range(program.grid_size):
        for col in range(program.grid_size):
            # Vị trí của ô
            rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, WHITE, rect, 1)  # Vẽ ô

            cell_content = program.get_cell_contents(row, col)

            if 'P' in cell_content:
                pygame.draw.circle(screen, BLACK, rect.center, cell_size // 4)
            elif 'W' in cell_content:
                pygame.draw.circle(screen, (255, 0, 0), rect.center, cell_size // 4)
            elif 'G' in cell_content:
                pygame.draw.circle(screen, (255, 255, 0), rect.center, cell_size // 4)

def draw_agent(agent):
    """Vẽ agent trên bản đồ."""
    row, col = agent.current_pos
    agent_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
    pygame.draw.rect(screen, (0, 255, 0), agent_rect)

def draw_text(screen, text, position, font_size=24, color=(255, 255, 255)):
    """Hiển thị văn bản trên màn hình."""
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def display_action_history(screen, file_path):
    """Đọc và hiển thị lịch sử hành động từ file."""
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        y_offset = 10  # Đặt vị trí ban đầu để hiển thị văn bản

        for line in lines:
            draw_text(screen, line.strip(), (10, y_offset))
            y_offset += 30  # Tăng dần vị trí để hiển thị dòng tiếp theo
    except FileNotFoundError:
        print(f"File {file_path} không tồn tại.")

# Khởi tạo đối tượng Agent
agent = Agent(program)

# Vòng lặp chính của trò chơi
while agent.is_alive:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BLACK)  # Làm mới màn hình

    draw_grid()  # Vẽ bản đồ
    draw_agent(agent)  # Vẽ agent
    display_action_history(screen, 'result1.txt')  # Hiển thị lịch sử hành động

    agent.advance()  # Tiến hành hành động của agent

    pygame.display.flip()  # Cập nhật màn hình

    if agent.gold_acquired or not agent.is_alive:
        break

pygame.quit()
