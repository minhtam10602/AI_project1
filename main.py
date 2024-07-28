import heapq
from collections import deque
import copy

# Function to parse the city map
def parse_city_map_lv2(file_path_level2):
    with open(file_path_level2, 'r') as file:
        lines = file.readlines()
    
    first_line = lines[0].strip().split()
    
    if len(first_line) < 3:
        raise ValueError("The first line of the input file must contain the vehicle name, start position, and maximum delivery time.")
    
    vehicle_name = first_line[0]
    start_position = eval(first_line[1])
    max_time = int(first_line[2])
    
    city_map = []
    for line in lines[1:]:
        city_map.append(line.strip().split())
        
    return city_map, start_position, max_time, vehicle_name

def parse_city_map_lv3(file_path_level3):
    with open(file_path_level3, 'r') as file:
        lines = file.readlines()
    
    first_line = lines[0].strip().split()
    
    if len(first_line) < 3:
        raise ValueError("The first line of the input file must contain start position, end position and fuel.")
    
    start_position = eval(first_line[0])
    end_position = eval(first_line[1])
    fuel = int(first_line[2])
    
    city_map = []
    for line in lines[1:]:
        city_map.append(line.strip().split())
        
    return city_map, start_position, end_position, fuel

def parse_city_map_lv1(file_path_level1):
    with open(file_path_level1, 'r') as file:
        lines = file.readlines()
        
    city_map = []
    for line in lines:
        city_map.append(line.strip().split())
        
    return city_map

def parse_city_map_lv4(file_path_level4):
    with open(file_path_level4, 'r') as file:
        lines = file.readlines()

    city_map = []
    for line in lines[1:]:
        city_map.append(line.strip().split())
        
    return city_map

# Duyệt lấy vị trí các agent trong file input theo số lượng được khai báo
def get_points(city_map, n_agent):
    coordinates = {}
    agent = [item for sublist in [[f'S{i}', f'G{i}'] for i in range(1, n_agent + 1)] for item in sublist]

    print(agent)
    for i, row in enumerate(city_map):
        for j, value in enumerate(row):
            if value in agent:
                coordinates[value] = (i, j)
    return coordinates

# Chuyển đổi map theo agent đang duyệt để tránh bị đúng hoặc đi ngang các agent khác
def define_new_maps(start, goal, coordiante, city_map):
    new_grid = copy.deepcopy(city_map)
    for i in coordiante:
        if coordiante[i] not in (start, goal):
            new_grid[coordiante[i][0]][coordiante[i][1]] = -1
    return new_grid


def bfs(city_map, start, goal):
    rows, cols = len(city_map), len(city_map[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    queue = deque([(start, [])])
    
    while queue:
        (x, y), path = queue.popleft()
        
        if (x, y) == goal:
            return path + [(x, y)]
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < rows and 0 <= ny < cols and city_map[nx][ny] != '-1' and not visited[nx][ny]:
                visited[nx][ny] = True
                queue.append(((nx, ny), path + [(x, y)]))
                
    return None
    
# DFS implementation
def dfs(city_map, start, goal):
    rows, cols = len(city_map), len(city_map[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    stack = [(start, [])]

    while stack:
        (x, y), path = stack.pop()

        if (x, y) == goal:
            return path + [(x, y)]

        if not visited[x][y]:
            visited[x][y] = True
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy

                if 0 <= nx < rows and 0 <= ny < cols:
                    if city_map[nx][ny] != '-1' and not visited[nx][ny]:
                        stack.append(((nx, ny), path + [(x, y)]))
                    else:
                        print(f"Skipping cell ({nx}, {ny}) with value {city_map[nx][ny]}")
                else:
                    print(f"Skipping out-of-bounds cell ({nx}, {ny})")

    return None  # No path found

# UCS implementation
def ucs(city_map, start, goal):
    rows, cols = len(city_map), len(city_map[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    pq = [(0, start, [])]  # Priority queue with cost, position, and path
    
    while pq:
        cost, (x, y), path = heapq.heappop(pq)
        
        if (x, y) == goal:
            return path + [(x, y)]
        
        if not visited[x][y]:
            visited[x][y] = True
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                
                if 0 <= nx < rows and 0 <= ny < cols and city_map[nx][ny] != '-1' and not visited[nx][ny]:
                    heapq.heappush(pq, (cost + 1, (nx, ny), path + [(x, y)]))
                
    return None  # No path found

# Greedy Best-First Search implementation
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def greedy_best_first_search(city_map, start, goal):
    rows, cols = len(city_map), len(city_map[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    pq = [(heuristic(start, goal), start, [])]  # Priority queue with heuristic, position, and path
    
    while pq:
        _, (x, y), path = heapq.heappop(pq)
        
        if (x, y) == goal:
            return path + [(x, y)]
        
        if not visited[x][y]:
            visited[x][y] = True
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                
                if 0 <= nx < rows and 0 <= ny < cols and city_map[nx][ny] != '-1' and not visited[nx][ny]:
                    heapq.heappush(pq, (heuristic((nx, ny), goal), (nx, ny), path + [(x, y)]))
                
    return None  # No path found

# A* Search implementation
def a_star_search(city_map, start, goal):
    rows, cols = len(city_map), len(city_map[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    pq = [(0 + heuristic(start, goal), 0, start, [])]  # Priority queue with f, g, position, and path
    
    while pq:
        f, g, (x, y), path = heapq.heappop(pq)
        
        if (x, y) == goal:
            return path + [(x, y)]
        
        if not visited[x][y]:
            visited[x][y] = True
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                
                if 0 <= nx < rows and 0 <= ny < cols and city_map[nx][ny] != '-1' and not visited[nx][ny]:
                    new_g = g + 1
                    new_f = new_g + heuristic((nx, ny), goal)
                    heapq.heappush(pq, (new_f, new_g, (nx, ny), path + [(x, y)]))
                
    return None  # No path found

# A* Search implementation considering toll booths and delivery time
def a_star_search_with_time_constraint(city_map, start, goal, max_time):
    rows, cols = len(city_map), len(city_map[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    pq = [(0 + heuristic(start, goal), 0, start, [], 0)]  # Priority queue with f, g, position, path, and total time
    
    while pq:
        f, g, (x, y), path, total_time = heapq.heappop(pq)
        
        if (x, y) == goal and total_time <= max_time:
            return path + [(x, y)], total_time
        
        if not visited[x][y]:
            visited[x][y] = True
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                
                if 0 <= nx < rows and 0 <= ny < cols and city_map[nx][ny] != '-1' and not visited[nx][ny]:
                    toll = int(city_map[nx][ny]) if city_map[nx][ny].isdigit() else 0
                    new_g = g + 1
                    new_f = new_g + heuristic((nx, ny), goal)
                    new_time = total_time + 1 + toll
                    if new_time <= max_time:
                        heapq.heappush(pq, (new_f, new_g, (nx, ny), path + [(x, y)], new_time))
                
    return None, None  # No path found or path exceeds max time
# A* Search implementation considering fuel cost and gas station

def a_star_search_with_fuel_constraint(city_map, start, goal, full_fuel):
    rows, cols = len(city_map), len(city_map[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    pq = [(0 + heuristic(start, goal), 0, start, [], full_fuel)]
    
    while pq:
        f, g, (x, y), path, fuel = heapq.heappop(pq)
        
        if (x, y) == goal:
            return path + [(x, y)], fuel
        
        if fuel == 0:
            continue #fuel has run out
        
        if not visited[x][y]:
            visited[x][y] = True
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                
                if 0 <= nx < rows and 0 <= ny < cols and city_map[nx][ny] != '-1' and not visited[nx][ny]:
                    new_fuel = full_fuel if city_map[nx][ny] == 'F' else fuel - 1
                    new_g = g + 1
                    new_f = new_g + heuristic((nx, ny), goal)
                    heapq.heappush(pq, (new_f, new_g, (nx, ny), path + [(x, y)], new_fuel))
        
        
    return None, None #No path found or fuel runs out before reaching the goal
            

# Function to save the path to a file
def save_path_to_file(paths, filename):
    with open(filename, 'w') as file:
        for algorithm, (path, total_time) in paths.items():
            file.write(algorithm + '\n')
            if path:
                for coord in path:
                    file.write(f"({coord[0]}, {coord[1]}) ")
                if total_time:
                    file.write(f"\nTotal Time: {total_time} minutes")
            else:
                file.write("No path found or path exceeds max time")
            file.write('\n\n')

# Parse the city map
file_path_level1 = 'input_level1_1.txt'
file_path_level2 = 'input_level2_1.txt'
file_path_level3 = 'input_level3.txt'
city_map1 = parse_city_map_lv1(file_path_level1)
city_map2, start, max_time, vehicle_name = parse_city_map_lv2(file_path_level2)
city_map3, start3, goal3, fuel = parse_city_map_lv3(file_path_level3) 
file_path_level4 = 'input_level4.txt'

city_map = parse_city_map_lv1(file_path_level1)
city_map, start, max_time, vehicle_name = parse_city_map_lv2(file_path_level2)

# Define the goal position
goal = (9, 0)  # Adjust according to the specific goal position

# Run each search algorithm and store the results
paths1 = {}
paths1["BFS"] = (bfs(city_map1, start, goal), None)
paths1["DFS"] = (dfs(city_map1, start, goal), None)
paths1["UCS"] = (ucs(city_map1, start, goal), None)
paths1["Greedy Best First Search"] = (greedy_best_first_search(city_map1, start, goal), None)
paths1["A*"] = (a_star_search(city_map1, start, goal), None)


# Save the paths to a single file
save_path_to_file(paths1, "output_level1.txt")

paths2 = {}

paths2["A* with Time Constraint"] = a_star_search_with_time_constraint(city_map2, start, goal, max_time)
save_path_to_file(paths2, "output_level2.txt")

paths3 = {}
paths3["A* with fuel Constraint"] = a_star_search_with_fuel_constraint(city_map=city_map3, start=start3, goal=goal3, full_fuel=fuel)
save_path_to_file(paths3, "output_level3.txt")
# Số lượng phần tử phải tương ứng với số lượng S1, S2,... G1, G2,.. được tạo ra trong file input
def level_4(file_path, n_agents):
    city_map = parse_city_map_lv4(file_path)
    coordiante = get_points(city_map, n_agents)

    paths = {}

    for i in range(1, n_agents + 1):  # Đảm bảo vòng lặp từ 1 đến n_agents
        new_map = define_new_maps(coordiante[f'S{i}'], coordiante[f'G{i}'], coordiante, city_map)
        # print(new_map)
        paths[f"BFS-{i}"] = (bfs(new_map, coordiante[f'S{i}'], coordiante[f'G{i}']), None)
        paths[f"DFS-{i}"] = (dfs(new_map, coordiante[f'S{i}'], coordiante[f'G{i}']), None)
        paths[f"UCS-{i}"] = (ucs(new_map, coordiante[f'S{i}'], coordiante[f'G{i}']), None)
        paths[f"Greedy Best First Search - {i}"] = (greedy_best_first_search(new_map, coordiante[f'S{i}'], coordiante[f'G{i}']), None)
        paths[f"A*-{i}"] = (a_star_search(new_map, coordiante[f'S{i}'], coordiante[f'G{i}']), None)

        print(city_map)
        # Save the paths to a single file for the current agent
        save_path_to_file(paths, f"output_level4_agent_{i}.txt")
        
        # Xóa path để tránh khi xử lí agent mới sẽ bị trùng data của agent cũ
        paths.clear()

level_4(file_path_level4, 3)
