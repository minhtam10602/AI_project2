from collections import deque
import random

class Program:
    def __init__(self, file_path):
        # Khởi tạo chương trình với bản đồ từ tệp tin
        self.grid_map = self.load_map(file_path)  # Tải bản đồ từ tệp
        self.grid_size = len(self.grid_map)  # Kích thước của bản đồ
        self.init_percepts()  # Khởi tạo các nhận thức trên bản đồ

    def load_map(self, file_path):
        # Đọc dữ liệu từ tệp tin và tạo bản đồ
        with open(file_path, 'r') as f:
            lines = f.readlines()
            size = int(lines[0].strip())  # Đọc kích thước bản đồ
            map_data = []

            for line in lines[1:]:
                elements = line.strip().split('.')  # Tách các phần tử của dòng
                if len(elements) != size:
                    # Cảnh báo nếu độ dài của hàng không khớp với kích thước
                    print(f"Cảnh báo: Độ dài hàng {len(elements)} không khớp với kích thước lưới {size}.")
                    while len(elements) < size:
                        elements.append('-')  # Thêm các ký tự '-' nếu cần thiết
                map_data.append(elements)

            if len(map_data) != size:
                raise ValueError(f"Kích thước lưới {len(map_data)} không khớp với kích thước đã chỉ định {size}.")
            return map_data

    def init_percepts(self):
        """Khởi tạo các nhận thức cho từng ô trong lưới."""
        # Thêm các nhận thức vào lưới. Ví dụ này giả sử rằng các nhận thức không được lưu trữ riêng biệt và được tính toán động.
        pass

    def display_map(self):
        """Hiển thị bản đồ hiện tại."""
        print(f"Kích thước lưới: {self.grid_size}")
        for row in self.grid_map:
            print(' '.join(row))
        print()

    def get_cell_contents(self, row, col):
        """Lấy nội dung của ô tại vị trí (row, col)."""
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            return self.grid_map[row][col]
        else:
            raise IndexError(f"Tọa độ ngoài phạm vi: ({row}, {col})")

    def get_percepts(self, row, col):
        """Lấy các nhận thức cho vị trí ô được chỉ định."""
        percepts = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Đông, Nam, Tây, Bắc

        for dr, dc in directions:
            adj_row, adj_col = row + dr, col + dc
            if 0 <= adj_row < self.grid_size and 0 <= adj_col < self.grid_size:
                cell_contents = self.get_cell_contents(adj_row, adj_col)
                if 'P' in cell_contents:
                    percepts.append('Breeze')  # Ô lân cận chứa hố
                if 'W' in cell_contents:
                    percepts.append('Stench')  # Ô lân cận chứa Wumpus
                if 'P_G' in cell_contents:
                    percepts.append('Whiff')   # Ô lân cận chứa khí độc
                if 'H_P' in cell_contents:
                    percepts.append('Glow')   # Ô lân cận chứa thuốc hồi phục
        return percepts


class Agent:
    def __init__(self, environment):
        # Khởi tạo tác nhân với môi trường
        self.environment = environment
        self.current_pos = (0, 0)  # Vị trí hiện tại của tác nhân
        self.facing_direction = 'E'  # Hướng hiện tại của tác nhân
        self.health_status = 100  # Trạng thái sức khỏe
        self.gold_acquired = False  # Có vàng không
        self.is_alive = True  # Tác nhân còn sống không
        self.action_history = []  # Lịch sử hành động
        self.visited = set()  # Theo dõi các vị trí đã thăm
        self.path = []  # Theo dõi con đường để đi theo

    def record_action(self, action):
        """Ghi lại hành động vào lịch sử."""
        r, c = self.current_pos
        self.action_history.append(f"({r+1},{c+1}): {action}")

    def advance(self):
        """Tiến về phía trước theo hướng hiện tại."""
        r, c = self.current_pos
        if self.facing_direction == 'N':
            r -= 1
        elif self.facing_direction == 'S':
            r += 1
        elif self.facing_direction == 'E':
            c += 1
        elif self.facing_direction == 'W':
            c -= 1

        if 0 <= r < self.environment.grid_size and 0 <= c < self.environment.grid_size:
            self.current_pos = (r, c)
            self.visited.add(self.current_pos)
            self.record_action("moved forward")
            print(f"Moved to {self.current_pos}")
            self.check_percepts()
        else:
            print("Blocked by boundary!")
            # Thay đổi hướng và thử lại
            self.rotate_right()
            self.advance()

    def rotate_left(self):
        """Xoay sang trái theo hướng hiện tại."""
        directions = ['N', 'W', 'S', 'E']
        self.facing_direction = directions[(directions.index(self.facing_direction) + 1) % 4]
        self.record_action("rotated left")
        print(f"Turned left. Now facing {self.facing_direction}")

    def rotate_right(self):
        """Xoay sang phải theo hướng hiện tại."""
        directions = ['N', 'E', 'S', 'W']
        self.facing_direction = directions[(directions.index(self.facing_direction) + 1) % 4]
        self.record_action("rotated right")
        print(f"Turned right. Now facing {self.facing_direction}")

    def check_percepts(self):
        """Kiểm tra các nhận thức tại vị trí hiện tại."""
        r, c = self.current_pos
        percepts = self.environment.get_percepts(r, c)
        print(f"Percepts at {self.current_pos}: {', '.join(percepts)}")

        if 'Stench' in percepts:
            print("Stench detected! Wumpus nearby.")
        if 'Breeze' in percepts:
            print("Breeze detected! Pit nearby.")
        if 'Whiff' in percepts:
            print("Whiff detected! Poisonous gas nearby.")
        if 'Glow' in percepts:
            print("Glow detected! Healing potion nearby.")
        if 'Scream' in percepts:
            print("Scream heard! Wumpus has been killed.")

    def find_path_to(self, goal):
        """Tìm đường ngắn nhất đến mục tiêu bằng BFS."""
        from collections import deque
        
        start = self.current_pos
        queue = deque([[start]])
        visited = set()
        visited.add(start)

        while queue:
            path = queue.popleft()
            pos = path[-1]

            if pos == goal:
                self.path = path
                return

            for direction in ['N', 'E', 'S', 'W']:
                next_pos = self.move_in_direction(pos, direction)
                if next_pos and next_pos not in visited:
                    visited.add(next_pos)
                    queue.append(path + [next_pos])

    def move_in_direction(self, pos, direction):
        """Di chuyển theo hướng chỉ định từ vị trí hiện tại."""
        r, c = pos
        if direction == 'N':
            r -= 1
        elif direction == 'S':
            r += 1
        elif direction == 'E':
            c += 1
        elif direction == 'W':
            c -= 1

        if 0 <= r < self.environment.grid_size and 0 <= c < self.environment.grid_size:
            return (r, c)
        else:
            return None

    def follow_path(self):
        """Đi theo con đường đã tính toán trước đó."""
        for next_pos in self.path:
            while self.current_pos != next_pos:
                self.face_direction(next_pos)
                self.advance()
                if not self.is_alive:
                    return
            self.path.remove(next_pos)

    def face_direction(self, goal):
        """Xoay để đối mặt với hướng của vị trí mục tiêu."""
        r1, c1 = self.current_pos
        r2, c2 = goal
        if r2 < r1:
            target_direction = 'N'
        elif r2 > r1:
            target_direction = 'S'
        elif c2 < c1:
            target_direction = 'W'
        elif c2 > c1:
            target_direction = 'E'

        while self.facing_direction != target_direction:
            self.rotate_right()

    def avoid_obstacles(self):
        """Tránh các chướng ngại vật dựa trên các nhận thức."""
        r, c = self.current_pos
        percepts = self.environment.get_percepts(r, c)
        
        if 'Breeze' in percepts or 'Whiff' in percepts:
            self.rotate_left()  # Chiến lược ví dụ
        elif 'Stench' in percepts:
            self.rotate_right()  # Chiến lược ví dụ

    def export_results(self, file_name):
        """Lưu lịch sử hành động vào tệp tin."""
        with open(file_name, 'w') as f:
            for action in self.action_history:
                f.write(action + '\n')
        print(f"Actions saved to {file_name}")

    def start_game(self):
        """Bắt đầu trò chơi và điều khiển tác nhân."""
        while self.is_alive:
            if self.gold_acquired:
                if self.current_pos == (0, 0):
                    print("Escaped with the gold! Victory!")
                    self.record_action("escaped with gold")
                    break
                else:
                    self.find_path_to((0, 0))
                    self.follow_path()
            else:
                gold_pos = None
                for r in range(self.environment.grid_size):
                    for c in range(self.environment.grid_size):
                        if 'G' in self.environment.get_cell_contents(r, c):
                            gold_pos = (r, c)
                            break
                    if gold_pos:
                        break
                if gold_pos:
                    self.find_path_to(gold_pos)
                    self.follow_path()
                else:
                    self.rotate_right()

            if self.health_status <= 0:
                print("Health depleted! Game Over.")
                self.record_action("health depleted")
                break

        self.export_results('result1.txt')


# Khởi tạo và bắt đầu trò chơi
program = Program('map1.txt')  # Tạo đối tượng Program với bản đồ từ tệp 'map1.txt'
program.display_map()  # Hiển thị bản đồ

agent = Agent(program)  # Tạo đối tượng Agent và liên kết với Program
agent.start_game()  # Bắt đầu chơi
