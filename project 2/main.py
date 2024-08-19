from collections import deque

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
                if 'S' in cell_contents:  # Kiểm tra nếu có tiếng "Scream"
                    percepts.append('Scream')  # Nghe tiếng "Scream" nếu Wumpus bị giết
        return percepts


from collections import deque

class Agent:
    def __init__(self, environment):
        self.environment = environment
        self.current_pos = (0, 0)
        self.facing_direction = 'E'
        self.health_status = 100
        self.gold_acquired = False
        self.is_alive = True
        self.action_history = []
        self.visited = set()
        self.path = []
        self.visited.add(self.current_pos)

    def point_assessment(self, action):
        if action == "found gold":
            self.point += 5000
        elif action == "die":
            self.point -= 10000
        else:
            self.point -= 10

    def record_action(self, action):
        r, c = self.current_pos
        self.action_history.append(f"({r+1},{c+1}): {action}")

    def is_safe_to_advance(self, position):
        """Check if the next position is safe to advance."""
        r, c = position
        percepts = self.environment.get_percepts(r, c)
        print(f"Checking safety for position {position}. Percepts: {percepts}")

        if 'Breeze' in percepts or 'Stench' in percepts or 'Whiff' in percepts:
            print("Not safe to advance!")
            return False  # Not safe if there are pits, Wumpus, or gas nearby
        print("Safe to advance.")
        return True
    def advance(self):
        """Move forward according to the current facing direction."""
        r, c = self.current_pos
        if self.facing_direction == 'N':
            r -= 1
        elif self.facing_direction == 'S':
            r += 1
        elif self.facing_direction == 'E':
            c += 1
        elif self.facing_direction == 'W':
            c -= 1

        next_pos = (r, c)

        if 0 <= r < self.environment.grid_size and 0 <= c < self.environment.grid_size:
            if self.is_safe_to_advance(next_pos):
                self.current_pos = next_pos
                self.visited.add(self.current_pos)
                self.record_action("moved forward")
                print(f"Moved to {self.current_pos}")
                self.check_percepts()
                if 'G' in self.environment.get_cell_contents(r, c):
                    print("Gold found! Stopping the game.")
                    self.record_action("found gold")
                    self.gold_acquired = True
                    return
            else:
                print("Danger detected! Avoiding.")
                self.avoid_obstacles()
        else:
            print("Blocked by boundary! Changing direction.")
            self.avoid_obstacles()


    def rotate_left(self):
        directions = ['N', 'W', 'S', 'E']
        self.facing_direction = directions[(directions.index(self.facing_direction) + 1) % 4]
        self.record_action("rotated left")
        print(f"Turned left. Now facing {self.facing_direction}")

    def rotate_right(self):
        directions = ['N', 'E', 'S', 'W']
        self.facing_direction = directions[(directions.index(self.facing_direction) + 1) % 4]
        self.record_action("rotated right")
        print(f"Turned right. Now facing {self.facing_direction}")

    def check_percepts(self):
        """Check the percepts at the current position and act accordingly."""
        r, c = self.current_pos
        percepts = self.environment.get_percepts(r, c)
        print(f"Percepts at {self.current_pos}: {', '.join(percepts)}")

        if 'Stench' in percepts:
            print("Stench detected! Wumpus nearby.")
            self.avoid_obstacles()

        if 'Breeze' in percepts:
            print("Breeze detected! Pit nearby.")
            self.avoid_obstacles()

        if 'Whiff' in percepts:
            print("Whiff detected! Poisonous gas nearby.")
            self.avoid_obstacles()

        if 'Glow' in percepts:
            print("Glow detected! Healing potion nearby.")
            self.collect_healing_potion()

        if 'Scream' in percepts:
            print("Scream heard! Wumpus has been killed.")

    def avoid_obstacles(self):
        """Avoid obstacles based on percepts and avoid endless loops."""
        for _ in range(4):  # Try all four directions
            self.rotate_right()
            r, c = self.current_pos
            next_pos = None

            if self.facing_direction == 'N':
                next_pos = (r - 1, c)
            elif self.facing_direction == 'S':
                next_pos = (r + 1, c)
            elif self.facing_direction == 'E':
                next_pos = (r, c + 1)
            elif self.facing_direction == 'W':
                next_pos = (r, c - 1)

            if next_pos and 0 <= next_pos[0] < self.environment.grid_size and 0 <= next_pos[1] < self.environment.grid_size:
                if next_pos not in self.visited and self.is_safe_to_advance(next_pos):
                    self.advance()
                    return
        print("No safe moves available. Ending the game.")
        self.is_alive = False

    def start_game(self):
        """Start the game loop."""
        while self.is_alive:
            if self.gold_acquired:
                print("Gold acquired, stopping the game.")
                break
            else:
                self.advance()

            if self.health_status <= 0:
                print("Health depleted! Game Over.")
                self.record_action("health depleted")
                break

        # Save the path and actions to the output file
        self.export_results('result1.txt')

    def export_results(self, file_name):
        """Save the action history to an output file."""
        with open(file_name, 'w') as f:
            for action in self.action_history:
                f.write(action + '\n')
        print(f"Actions saved to {file_name}")

# Khởi tạo và bắt đầu trò chơi
program = Program('map1.txt')  # Tạo đối tượng Program với bản đồ từ tệp 'map1.txt'
program.display_map()  # Hiển thị bản đồ

agent = Agent(program)  # Tạo đối tượng Agent và liên kết với Program
agent.start_game()  # Bắt đầu chơi
