import heapq
from collections import deque

# Đọc file input
def parse_city_map(file_path):
    with open(file_path, 'r') as file:
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
                
    return None 

def ucs(city_map, start, goal):
    rows, cols = len(city_map), len(city_map[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    pq = [(0, start, [])] 
    
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
                
    return None

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def greedy_best_first_search(city_map, start, goal):
    rows, cols = len(city_map), len(city_map[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    pq = [(heuristic(start, goal), start, [])] 
    
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
                
    return None 

def a_star_search(city_map, start, goal):
    rows, cols = len(city_map), len(city_map[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    pq = [(0 + heuristic(start, goal), 0, start, [])] 
    
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
                
    return None 

# Xuất file ouptut
def save_path_to_file(paths, filename):
    with open(filename, 'w') as file:
        for algorithm, path in paths.items():
            file.write(algorithm + '\n')
            if path:
                for coord in path:
                    file.write(f"({coord[0]}, {coord[1]}) ")
            else:
                file.write("No path found")
            file.write('\n\n')

file_path = 'input_level1.txt'  
city_map = parse_city_map(file_path)


start = (1, 0)  
goal = (9, 0)

paths = {}
paths["BFS"] = bfs(city_map, start, goal)
paths["DFS"] = dfs(city_map, start, goal)
paths["UCS"] = ucs(city_map, start, goal)
paths["Greedy Best First Search"] = greedy_best_first_search(city_map, start, goal)
paths["A*"] = a_star_search(city_map, start, goal)


save_path_to_file(paths, "output_level1.txt")
