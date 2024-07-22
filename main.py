import heapq
from collections import deque

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

def parse_city_map_lv1(file_path_level1):
    with open(file_path_level1, 'r') as file:
        lines = file.readlines()
        
    city_map = []
    for line in lines:
        city_map.append(line.strip().split())
        
    return city_map

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

# BFS implementation
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
                
    return None  # No path found

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
                
                if 0 <= nx < rows and 0 <= ny < cols and city_map[nx][ny] != '-1' and not visited[nx][ny]:
                    stack.append(((nx, ny), path + [(x, y)]))
                
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

# Function to save the path to a file
def save_path_to_file(paths, filename):
    with open(filename, 'w') as file:
        for algorithm, (path, total_time) in paths.items():
            file.write(algorithm + '\n')
            if path:
                for coord in path:
                    file.write(f"({coord[0]}, {coord[1]}) ")
                file.write(f"\nTotal Time: {total_time} minutes")
            else:
                file.write("No path found or path exceeds max time")
            file.write('\n\n')

# Parse the city map
file_path_level1 = 'input_level1.txt'
file_path_level2 = 'input_level2.txt'
city_map = parse_city_map_lv1(file_path_level1)
city_map, start, max_time, vehicle_name = parse_city_map_lv2(file_path_level2)

# Define the goal position
goal = (9, 0)  # Adjust according to the specific goal position

# Run each search algorithm and store the results
paths = {}
paths["BFS"] = (bfs(city_map, start, goal), None)
paths["DFS"] = (dfs(city_map, start, goal), None)
paths["UCS"] = (ucs(city_map, start, goal), None)
paths["Greedy Best First Search"] = (greedy_best_first_search(city_map, start, goal), None)
paths["A*"] = (a_star_search(city_map, start, goal), None)


# Save the paths to a single file
save_path_to_file(paths, "output_level1.txt")

paths["A* with Time Constraint"] = a_star_search_with_time_constraint(city_map, start, goal, max_time)
save_path_to_file(paths, "output_level2.txt")
