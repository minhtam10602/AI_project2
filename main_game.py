import pygame
import sys
from main import Program, Agent

# Khởi tạo Pygame
pygame.init()

# Thiết lập màn hình hiển thị với khu vực thêm cho lịch sử hành động
screen_width = 800  # Chiều rộng của cửa sổ
screen_height = 600  # Chiều cao của cửa sổ
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Agent Game")

# Đặt màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (169, 169, 169)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)

# Khởi tạo chương trình với bản đồ từ tệp 'map1.txt'
program = Program('map1.txt')

# Thiết lập kích thước ô lưới
grid_width = 600  # Khu vực cho lưới
cell_size = grid_width // program.grid_size

# Đặt tốc độ khung hình (FPS)
clock = pygame.time.Clock()
fps = 10  # Số khung hình mỗi giây (giới hạn tốc độ khung hình)

# Thời gian giữa các bước di chuyển của agent
pause_duration = 1000  # 1000 ms = 1 giây
last_move_time = pygame.time.get_ticks()

def draw_grid():
    """Vẽ lưới và các vật thể trên bản đồ."""
    for row in range(program.grid_size):
        for col in range(program.grid_size):
            # Vị trí của ô
            rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, WHITE, rect, 1)  # Vẽ ô

            cell_content = program.get_cell_contents(row, col)

            # Vẽ các đối tượng và nhận thức trên bản đồ
            if 'P' in cell_content:
                pygame.draw.circle(screen, WHITE, rect.center, cell_size // 4)  # Pit
            elif 'W' in cell_content:
                pygame.draw.circle(screen, RED, rect.center, cell_size // 4)  # Wumpus
            elif 'G' in cell_content:
                pygame.draw.circle(screen, YELLOW, rect.center, cell_size // 4)  # Gold
            elif 'P_G' in cell_content:
                pygame.draw.circle(screen, GRAY, rect.center, cell_size // 4)  # Poisonous Gas
            elif 'H_P' in cell_content:
                pygame.draw.circle(screen, CYAN, rect.center, cell_size // 4)  # Healing Potion
            elif 'S' in cell_content:
                pygame.draw.circle(screen, PURPLE, rect.center, cell_size // 4)  # Stench
            elif 'B' in cell_content:
                pygame.draw.circle(screen, BLUE, rect.center, cell_size // 4)  # Breeze
            elif 'Wh' in cell_content:
                pygame.draw.circle(screen, ORANGE, rect.center, cell_size // 4)  # Whiff
            elif 'G_L' in cell_content:
                pygame.draw.circle(screen, GREEN, rect.center, cell_size // 4)  # Glow

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

        # Vẽ một vùng nền đen để hiển thị lịch sử hành động
        history_area = pygame.Rect(grid_width, 0, screen_width - grid_width, screen_height)
        pygame.draw.rect(screen, BLACK, history_area)

        # Hiển thị lịch sử hành động trong vùng riêng biệt
        y_offset = 10  # Đặt vị trí ban đầu để hiển thị văn bản

        for line in lines[-20:]:  # Chỉ hiển thị 20 hành động gần nhất để tránh tràn màn hình
            draw_text(screen, line.strip(), (grid_width + 10, y_offset), font_size=20, color=WHITE)
            y_offset += 25  # Tăng dần vị trí để hiển thị dòng tiếp theo
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

    # Kiểm tra nếu thời gian đủ lâu để tiến hành bước tiếp theo
    current_time = pygame.time.get_ticks()
    if current_time - last_move_time > pause_duration:
        agent.advance()  # Tiến hành hành động của agent
        last_move_time = current_time  # Cập nhật thời gian của bước di chuyển cuối cùng

    pygame.display.flip()  # Cập nhật màn hình

    clock.tick(fps)  # Điều chỉnh tốc độ khung hình

    if agent.gold_acquired or not agent.is_alive:
        break

pygame.quit()
