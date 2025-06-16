import heapq
from typing import List, Tuple, Optional, Set
from copy import deepcopy

class PuzzleState:
    """表示八码数图的状态"""

    def __init__(self, board: List[List[int]], g_cost: int = 0, parent=None, move: str = ""):
        self.board = board
        self.g_cost = g_cost  # 从起始状态到当前状态的实际代价
        self.parent = parent  # 父状态，用于路径重构
        self.move = move      # 到达此状态的移动
        self.blank_pos = self._find_blank()
        self.h_cost = self._manhattan_distance()  # 启发式代价
        self.f_cost = self.g_cost + self.h_cost   # 总代价

    def _find_blank(self) -> Tuple[int, int]:
        """找到空白位置（0表示空白）"""
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return (i, j)
        return (0, 0)

    def _manhattan_distance(self) -> int:
        """计算曼哈顿距离启发式函数"""
        distance = 0
        target = {1: (0, 0), 2: (0, 1), 3: (0, 2),
                 4: (1, 0), 5: (1, 1), 6: (1, 2),
                 7: (2, 0), 8: (2, 1), 0: (2, 2)}

        for i in range(3):
            for j in range(3):
                if self.board[i][j] != 0:
                    target_pos = target[self.board[i][j]]
                    distance += abs(i - target_pos[0]) + abs(j - target_pos[1])
        return distance

    def is_goal(self) -> bool:
        """检查是否为目标状态"""
        goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        return self.board == goal

    def get_neighbors(self) -> List['PuzzleState']:
        """获取所有可能的邻居状态"""
        neighbors = []
        row, col = self.blank_pos

        # 定义四个方向的移动：上、下、左、右
        directions = [(-1, 0, "上"), (1, 0, "下"), (0, -1, "左"), (0, 1, "右")]

        for dr, dc, move_name in directions:
            new_row, new_col = row + dr, col + dc

            # 检查边界
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                # 创建新状态
                new_board = deepcopy(self.board)
                # 交换空白位置和目标位置
                new_board[row][col], new_board[new_row][new_col] = \
                    new_board[new_row][new_col], new_board[row][col]

                neighbor = PuzzleState(new_board, self.g_cost + 1, self, move_name)
                neighbors.append(neighbor)

        return neighbors

    def __lt__(self, other):
        """用于优先队列比较"""
        return self.f_cost < other.f_cost

    def __eq__(self, other):
        """状态相等比较"""
        return self.board == other.board

    def __hash__(self):
        """用于集合和字典"""
        return hash(str(self.board))

    def __str__(self):
        """字符串表示"""
        result = ""
        for row in self.board:
            for cell in row:
                if cell == 0:
                    result += "* "
                else:
                    result += f"{cell} "
            result += "\n"
        return result.strip()

def solve_puzzle(initial_board: List[List[int]]) -> Optional[List[str]]:
    """使用A*算法解决八码数图问题"""

    # 检查是否有解（逆序对数量必须为偶数）
    if not is_solvable(initial_board):
        return None

    initial_state = PuzzleState(initial_board)

    # 如果初始状态就是目标状态
    if initial_state.is_goal():
        return []

    # A*搜索
    open_set = [initial_state]  # 优先队列
    closed_set: Set[str] = set()  # 已访问状态

    while open_set:
        current = heapq.heappop(open_set)

        # 将当前状态加入已访问集合
        state_key = str(current.board)
        if state_key in closed_set:
            continue
        closed_set.add(state_key)

        # 检查是否到达目标
        if current.is_goal():
            return reconstruct_path(current)

        # 探索邻居状态
        for neighbor in current.get_neighbors():
            neighbor_key = str(neighbor.board)
            if neighbor_key not in closed_set:
                heapq.heappush(open_set, neighbor)

    return None  # 无解

def is_solvable(board: List[List[int]]) -> bool:
    """检查八码数图是否有解"""
    # 将二维数组转换为一维，排除空白位置
    flat = []
    for row in board:
        for cell in row:
            if cell != 0:
                flat.append(cell)

    # 计算逆序对数量
    inversions = 0
    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            if flat[i] > flat[j]:
                inversions += 1

    # 八码数图有解当且仅当逆序对数量为偶数
    return inversions % 2 == 0

def reconstruct_path(goal_state: PuzzleState) -> List[str]:
    """重构从初始状态到目标状态的路径"""
    path = []
    current = goal_state

    while current.parent is not None:
        path.append(current.move)
        current = current.parent

    path.reverse()
    return path

def parse_input(input_str: str) -> List[List[int]]:
    """解析输入字符串为3x3矩阵"""
    lines = input_str.strip().split('\n')
    board = []

    for line in lines:
        row = []
        for char in line:
            if char == '*':
                row.append(0)  # 空白位置用0表示
            elif char.isdigit():
                row.append(int(char))
        if len(row) == 3:  # 确保每行有3个元素
            board.append(row)

    return board

def format_output(moves: List[str]) -> str:
    """格式化输出结果"""
    if not moves:
        return "拼图已经是目标状态，无需移动。"

    result = f"解决步骤（共{len(moves)}步）：\n"
    for i, move in enumerate(moves, 1):
        result += f"{i}. 向{move}移动\n"

    return result

def main():
    """主程序"""
    print("八码数图求解器")
    print("请输入初始状态（3行，每行3个字符，*表示空白）：")
    print("示例输入：")
    print("378")
    print("416")
    print("2*5")
    print()

    # 读取输入
    input_lines = []
    for i in range(3):
        line = input(f"第{i+1}行: ").strip()
        input_lines.append(line)

    input_str = '\n'.join(input_lines)

    try:
        # 解析输入
        initial_board = parse_input(input_str)

        print("\n初始状态：")
        initial_state = PuzzleState(initial_board)
        print(initial_state)

        print("目标状态：")
        print("1 2 3")
        print("4 5 6")
        print("7 8 *")
        print()

        # 求解
        print("正在求解...")
        solution = solve_puzzle(initial_board)

        if solution is None:
            print("此拼图无解！")
        else:
            print(format_output(solution))

            # 演示解决过程
            print("\n解决过程演示：")
            current_board = deepcopy(initial_board)
            current_state = PuzzleState(current_board)
            print(f"初始状态：")
            print(current_state)
            print()

            for i, move in enumerate(solution, 1):
                # 模拟移动
                neighbors = current_state.get_neighbors()
                for neighbor in neighbors:
                    if neighbor.move == move:
                        current_state = neighbor
                        break

                print(f"第{i}步：向{move}移动")
                print(current_state)
                print()

    except Exception as e:
        print(f"发生错误：{e}")

if __name__ == "__main__":
    main()