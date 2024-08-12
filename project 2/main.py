class Program:
    def __init__(self, file_path):
        self.grid_map = self.load_map(file_path)  # Nạp bản đồ từ tệp
        self.grid_size = len(self.grid_map)  # Kích thước của bản đồ
        self.init_percepts()  # Khởi tạo các cảm nhận trên bản đồ

    def load_map(self, file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()  # Đọc tất cả các dòng trong tệp
            size = int(lines[0].strip())  # Kích thước của bản đồ (dòng đầu tiên)
            map_data = []

            for line in lines[1:]:
                elements = line.strip().split('.')  # Tách các phần tử trong hàng dựa trên dấu '.'
                # Kiểm tra xem hàng có đủ phần tử không
                if len(elements) != size:
                    print(f"Warning: Row length {len(elements)} does not match grid size {size}.")
                    while len(elements) < size:  # Thêm phần tử '-' nếu hàng chưa đủ
                        elements.append('-')
                map_data.append(elements)

            if len(map_data) != size:
                raise ValueError(f"Grid size {len(map_data)} does not match specified size {size}.")
            return map_data  # Trả về dữ liệu bản đồ

    def display_map(self):
        print(f"Grid size: {self.grid_size}")  # Hiển thị kích thước bản đồ
        for row in self.grid_map:
            print(' '.join(row))  # Hiển thị từng hàng của bản đồ
        print()

    def init_percepts(self):
        pass  # Hàm trống để khởi tạo cảm nhận, sẽ được bổ sung sau

    def get_cell_contents(self, row, col):
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:  # Kiểm tra nếu tọa độ hợp lệ
            return self.grid_map[row][col]  # Trả về thông tin của ô
        else:
            raise IndexError(f"Coordinates out of range: ({row}, {col})")  # Báo lỗi nếu tọa độ ngoài phạm vi

class Agent:
    def __init__(self, environment):
        self.environment = environment  # Liên kết với đối tượng Program
        self.current_pos = (0, 0)  # Vị trí khởi tạo của agent
        self.facing_direction = 'E'  # Hướng khởi tạo là hướng Đông
        self.health_status = 100  # Máu của agent khởi tạo là 100%
        self.gold_acquired = False  # Khởi tạo trạng thái chưa có vàng
        self.is_alive = True  # Khởi tạo trạng thái còn sống
        self.action_history = []  # Lịch sử các hành động đã thực hiện

    def record_action(self, action):
        r, c = self.current_pos  # Lấy tọa độ hiện tại
        self.action_history.append(f"({r+1},{c+1}): {action}")  # Ghi lại hành động cùng với tọa độ

    def advance(self):
        r, c = self.current_pos  # Lấy tọa độ hiện tại
        if self.facing_direction == 'N':  # Nếu hướng là Bắc
            r -= 1
        elif self.facing_direction == 'S':  # Nếu hướng là Nam
            r += 1
        elif self.facing_direction == 'E':  # Nếu hướng là Đông
            c += 1
        elif self.facing_direction == 'W':  # Nếu hướng là Tây
            c -= 1

        if 0 <= r < self.environment.grid_size and 0 <= c < self.environment.grid_size:  # Kiểm tra nếu di chuyển trong phạm vi
            self.current_pos = (r, c)  # Cập nhật vị trí mới
            self.record_action("moved forward")  # Ghi lại hành động di chuyển
            print(f"Moved to {self.current_pos}")  # Hiển thị vị trí mới
            self.check_percepts()  # Kiểm tra cảm nhận tại vị trí mới
        else:
            print("Blocked by boundary!")  # Thông báo nếu di chuyển ra ngoài phạm vi

    def rotate_left(self):
        directions = ['N', 'W', 'S', 'E']  # Các hướng theo thứ tự quay trái
        self.facing_direction = directions[(directions.index(self.facing_direction) + 1) % 4]  # Xác định hướng mới
        self.record_action("rotated left")  # Ghi lại hành động quay trái
        print(f"Turned left. Now facing {self.facing_direction}")  # Hiển thị hướng mới

    def rotate_right(self):
        directions = ['N', 'E', 'S', 'W']  # Các hướng theo thứ tự quay phải
        self.facing_direction = directions[(directions.index(self.facing_direction) + 1) % 4]  # Xác định hướng mới
        self.record_action("rotated right")  # Ghi lại hành động quay phải
        print(f"Turned right. Now facing {self.facing_direction}")  # Hiển thị hướng mới

    def check_percepts(self):
        r, c = self.current_pos  # Lấy tọa độ hiện tại
        contents = self.environment.get_cell_contents(r, c)  # Lấy thông tin ô hiện tại
        print(f"Percepts at {self.current_pos}: {contents}")  # Hiển thị cảm nhận tại vị trí hiện tại

        if 'W' in contents:  # Nếu gặp Wumpus
            print("Wumpus encountered! Game over.")
            self.record_action("encountered Wumpus")  # Ghi lại hành động gặp Wumpus
            self.is_alive = False  # Chết (kết thúc trò chơi)
        if 'P' in contents:  # Nếu rơi vào hố
            print("Fell into a pit! Game over.")
            self.record_action("fell into pit")  # Ghi lại hành động rơi vào hố
            self.is_alive = False  # Chết (kết thúc trò chơi)
        if 'P_G' in contents:  # Nếu gặp khí độc
            self.health_status -= 25  # Giảm máu 25%
            print(f"Poison gas! Health reduced to {self.health_status}%.")
            self.record_action("poisoned by gas")  # Ghi lại hành động gặp khí độc
        if 'H_P' in contents:  # Nếu tìm thấy thuốc hồi phục
            self.health_status += 25  # Tăng máu 25%
            print(f"Healing potion found! Health restored to {self.health_status}%.")
            self.record_action("found healing potion")  # Ghi lại hành động tìm thấy thuốc hồi phục
        if 'G' in contents:  # Nếu tìm thấy vàng
            print("Gold found!")
            self.gold_acquired = True  # Đánh dấu trạng thái đã có vàng
            self.record_action("found gold")  # Ghi lại hành động tìm thấy vàng

    def fire_arrow(self):
        print("Arrow shot!")  # Thông báo bắn mũi tên
        self.record_action("fired arrow")  # Ghi lại hành động bắn mũi tên

    def export_results(self, file_name):
        with open(file_name, 'w') as f:  # Mở tệp để ghi kết quả
            for action in self.action_history:
                f.write(action + '\n')  # Ghi từng hành động vào tệp
        print(f"Actions saved to {file_name}")  # Thông báo kết quả đã được lưu

    def start_game(self):
        while self.is_alive:  # Vòng lặp trò chơi tiếp tục khi agent còn sống
            command = input("Enter command (F=forward, L=left, R=right, S=shoot, G=grab, C=climb, Q==quit): ").upper()  # Nhập lệnh
            if command == 'F':
                self.advance()  # Di chuyển về phía trước
            elif command == 'L':
                self.rotate_left()  # Quay trái
            elif command == 'R':
                self.rotate_right()  # Quay phải
            elif command == 'S':
                self.fire_arrow()  # Bắn mũi tên
            elif command == 'G':
                if self.gold_acquired:
                    print("You already have the gold!")  # Thông báo nếu đã có vàng
                else:
                    print("No gold here to grab!")  # Thông báo nếu không có vàng để nhặt
            elif command == 'C':
                if self.current_pos == (0, 0) and self.gold_acquired:
                    print("Escaped with the gold! Victory!")  # Thông báo chiến thắng nếu đã có vàng và thoát ra
                    self.record_action("escaped with gold")  # Ghi lại hành động thoát ra với vàng
                    break
                else:
                    print("You can't climb out here.")  # Thông báo không thể thoát ra nếu không ở vị trí (0, 0)
            elif command == 'Q':
                print("Exiting the game.")  # Thông báo thoát trò chơi
                break

            if self.health_status <= 0:  # Kiểm tra nếu máu hết
                print("Health depleted! Game Over.")
                self.record_action("health depleted")  # Ghi lại hành động máu cạn kiệt
                break

        self.export_results('result1.txt')  # Lưu kết quả sau khi trò chơi kết thúc


# Khởi tạo và bắt đầu trò chơi
program = Program('map1.txt')  # Tạo đối tượng Program với bản đồ từ tệp 'map1.txt'
program.display_map()  # Hiển thị bản đồ

agent = Agent(program)  # Tạo đối tượng Agent và liên kết với Program
agent.start_game()  # Bắt đầu chơi

