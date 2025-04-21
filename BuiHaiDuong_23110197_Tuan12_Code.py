import pygame, sys, time, heapq
from collections import deque
import random
import math

from typing import List, Tuple, Deque, Set, Dict, Optional, Union

pygame.init()
w, h = 800, 700
s = pygame.display.set_mode((w, h))
pygame.display.set_caption("XepHinh")

C_WHITE = (255, 255, 255)
C_BLACK = (0, 0, 0)
C_LIGHT_GRAY = (220, 220, 220)
C_GREEN = (0, 128, 0)
C_BLUE = (100, 100, 255)
C_RED = (255, 100, 100)
C_DARK_GRAY = (200, 200, 200)
C_HIGHLIGHT = (255, 255, 0) 

f = pygame.font.Font(None, 36)
f2 = pygame.font.Font(None, 24)
f_dropdown = pygame.font.Font(None, 20)

State = Tuple[int, ...]
BeliefState = Set[State] 

d: State = (2, 6, 5, 1, 3, 8, 4, 7, 0) 
g: State = (1, 2, 3, 4, 5, 6, 7, 8, 0) 

current_algo = "None"
solution_info = {"path": "", "solve_time": 0.0, "display_time": 0.0}
algorithms = [
    "BFS", "DFS", "IDDFS", "Greedy", "UCS", "A*", "IDA*",
    "Simple HC", "Steepest HC", "Stochastic HC",
    "Simulated Annealing", "Genetic Algorithm", "BFS Sensorless",
    "Backtracking", "CSP Backtracking"
]
dropdown_active = False
dropdown_rect = pygame.Rect(350, 170, 200, 30)
dropdown_item_height = 25
dropdown_item_rects = []

def ve_board(current_state: State, highlighted_tile_index: Optional[int] = None):
    board_offset_x, board_offset_y = 20, 20
    tile_size = 100
    for i in range(3):
        for j in range(3):
            idx = i * 3 + j
            r = pygame.Rect(board_offset_x + j * tile_size, board_offset_y + i * tile_size, tile_size, tile_size)

            if idx == highlighted_tile_index:
                color = C_HIGHLIGHT 
            elif current_state[idx] == 0:
                color = C_LIGHT_GRAY 
            else:
                color = C_WHITE 

            pygame.draw.rect(s, color, r)
            pygame.draw.rect(s, C_BLACK, r, 1) 

            if current_state[idx] != 0:
                text_surface = f.render(str(current_state[idx]), True, C_BLACK)
                text_rect = text_surface.get_rect(center=r.center)
                s.blit(text_surface, text_rect)

def ve_ui(info: dict):
    global dropdown_item_rects
    dropdown_item_rects = [] 

    info_x, info_y = 350, 20

    # Vẽ thông tin UI
    s.blit(f2.render(f"Start: {d}", True, C_BLACK), (info_x, info_y))
    s.blit(f2.render(f"Goal:  {g}", True, C_BLACK), (info_x, info_y + 30))
    s.blit(f2.render(f"Algorithm: {current_algo}", True, C_BLACK), (info_x, info_y + 60))
    s.blit(f2.render(f"Processing Time: {info['solve_time']:.4f} s", True, C_BLACK), (info_x, info_y + 90))
    s.blit(f2.render(f"Display Time: {info['display_time']:.4f} s", True, C_BLACK), (info_x, info_y + 120))

    # Vẽ dropdown menu
    pygame.draw.rect(s, C_GREEN, dropdown_rect, border_radius=5)
    pygame.draw.rect(s, C_DARK_GRAY, dropdown_rect, 1, border_radius=5) 
    selected_text = current_algo if current_algo != "None" else "Select Algorithm"
    text_surf = f2.render(selected_text, True, C_WHITE)
    text_rect = text_surf.get_rect(center=dropdown_rect.center)
    s.blit(text_surf, text_rect)

    arrow_points = [(dropdown_rect.right - 15, dropdown_rect.centery - 3),
                    (dropdown_rect.right - 5, dropdown_rect.centery - 3),
                    (dropdown_rect.right - 10, dropdown_rect.centery + 3)]
    pygame.draw.polygon(s, C_WHITE, arrow_points)

    # Vẽ các mục trong dropdown menu (nếu đang mở)
    if dropdown_active:
        base_y = dropdown_rect.bottom + 2
        for i, algo_name in enumerate(algorithms):
            item_rect = pygame.Rect(dropdown_rect.left, base_y + i * dropdown_item_height, dropdown_rect.width, dropdown_item_height)
            dropdown_item_rects.append(item_rect) 

            # Kiểm tra nếu chuột đang hover
            if item_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(s, C_BLUE, item_rect)  # Màu nền khi hover
            else:
                pygame.draw.rect(s, C_LIGHT_GRAY, item_rect)  # Màu nền mặc định

            pygame.draw.rect(s, C_DARK_GRAY, item_rect, 1)  # Viền
            item_text = f_dropdown.render(algo_name, True, C_BLACK)
            s.blit(item_text, (item_rect.x + 5, item_rect.y + 5))

    path_area_y = 350
    max_width, padding = w - 40, 20
    text_x, text_y = padding, path_area_y + 30
    s.blit(f2.render("Path:", True, C_BLACK), (padding, path_area_y))

    path_display = info['path']
    if isinstance(path_display, str):

        words = path_display if len(path_display) < 100 else path_display[:100] + "..."
        current_line = ""
        for char in words:
            test_line = current_line + char
            text_surf_test = f2.render(test_line, True, C_BLACK)
            if text_surf_test.get_width() > max_width:

                s.blit(f2.render(current_line, True, C_BLACK), (text_x, text_y))
                text_y += f2.get_height() + 2 
                current_line = char 
            else:
                current_line = test_line 

            if text_y > h - 30: 
                 s.blit(f2.render("...", True, C_BLACK), (text_x + f2.size(current_line)[0], text_y))
                 break

        if current_line and text_y <= h - 30:
             s.blit(f2.render(current_line, True, C_BLACK), (text_x, text_y))

    elif isinstance(path_display, list): 
         s.blit(f2.render(str(path_display), True, C_BLACK), (text_x, text_y))

def ke(x: State) -> List[Tuple[str, State]]:
    neighbors = []
    try:
        z = x.index(0) 
    except ValueError:
        print(f"Error: State {x} does not contain 0!")
        return [] 

    r, c = z // 3, z % 3 

    possible_moves = [(1, 0, 'D'), (-1, 0, 'U'), (0, 1, 'R'), (0, -1, 'L')]

    for dr, dc, move_char in possible_moves:
        nr, nc = r + dr, c + dc 

        if 0 <= nr < 3 and 0 <= nc < 3:
            y = list(x) 
            nz = nr * 3 + nc 
            y[z], y[nz] = y[nz], y[z] 
            neighbors.append((move_char, tuple(y))) 

    return neighbors

def heuristic(x: State, goal: State = g) -> int:
    dist = 0
    for i, val in enumerate(x):
        if val != 0: 
            try:
                goal_idx = goal.index(val)
                current_row, current_col = i // 3, i % 3
                goal_row, goal_col = goal_idx // 3, goal_idx % 3
                dist += abs(current_row - goal_row) + abs(current_col - goal_col)
            except ValueError:
                print(f"Warning: Value {val} from state {x} not found in goal {goal}. Heuristic might be inaccurate.")

                pass
    return dist

def bfs(start_node: State, goal_node: State) -> Tuple[str, float]:
    start_time = time.time()
    queue: Deque[Tuple[str, State]] = deque([("", start_node)])
    visited: Set[State] = {start_node}

    while queue:
        path, current_state = queue.popleft()
        if current_state == goal_node:
            return path, time.time() - start_time

        for move, next_state in ke(current_state):
            if next_state not in visited:
                visited.add(next_state)
                queue.append((path + move, next_state))

    return "No Solution", time.time() - start_time

def dfs(start_node: State, goal_node: State, max_depth: int = 30) -> Tuple[str, float]:
    start_time = time.time()
    stack: List[Tuple[str, State, int]] = [("", start_node, 0)] 
    visited: Dict[State, int] = {start_node: 0} 

    while stack:
        path, current_state, depth = stack.pop()

        if current_state == goal_node:
            return path, time.time() - start_time

        if depth >= max_depth:
            continue

        for move, next_state in reversed(ke(current_state)):
            new_depth = depth + 1

            if next_state not in visited or new_depth < visited[next_state]:
                visited[next_state] = new_depth
                stack.append((path + move, next_state, new_depth))

    return f"No Solution (depth limit {max_depth}?)", time.time() - start_time

def ucs(start_node: State, goal_node: State) -> Tuple[str, float]:
    start_time = time.time()

    priority_queue: List[Tuple[int, str, State]] = [(0, "", start_node)]
    visited: Dict[State, int] = {start_node: 0} 

    while priority_queue:
        cost, path, current_state = heapq.heappop(priority_queue)

        if current_state == goal_node:
            return path, time.time() - start_time

        if cost > visited[current_state]:
            continue

        for move, next_state in ke(current_state):
            new_cost = cost + 1 

            if next_state not in visited or new_cost < visited[next_state]:
                visited[next_state] = new_cost
                heapq.heappush(priority_queue, (new_cost, path + move, next_state))

    return "No Solution", time.time() - start_time

def iddfs(start_node: State, goal_node: State, max_limit: int = 50) -> Tuple[str, float]:
    start_time = time.time()

    def dls(path: str, current_state: State, nodes_in_path: List[State], depth_limit: int) -> Optional[str]:
        if current_state == goal_node:
            return path
        if len(path) >= depth_limit:
            return None 

        for move, next_state in ke(current_state):

             if next_state not in nodes_in_path:
                nodes_in_path.append(next_state) 
                result = dls(path + move, next_state, nodes_in_path, depth_limit)
                nodes_in_path.pop() 
                if result is not None:
                    return result 

        return None 

    for depth in range(max_limit + 1): 
        result = dls("", start_node, [start_node], depth) 
        if result is not None:

            return result, time.time() - start_time

    return f"No Solution (within limit {max_limit})", time.time() - start_time

def greedy(start_node: State, goal_node: State) -> Tuple[str, float]:
    start_time = time.time()

    priority_queue: List[Tuple[int, str, State]] = [(heuristic(start_node, goal_node), "", start_node)]
    visited: Set[State] = {start_node} 

    while priority_queue:
        _, path, current_state = heapq.heappop(priority_queue) 

        if current_state == goal_node:
            return path, time.time() - start_time

        for move, next_state in ke(current_state):
            if next_state not in visited:
                visited.add(next_state)
                h_cost = heuristic(next_state, goal_node)
                heapq.heappush(priority_queue, (h_cost, path + move, next_state))

    return "No Solution", time.time() - start_time

def astar(start_node: State, goal_node: State) -> Tuple[str, float]:
    start_time = time.time()

    priority_queue: List[Tuple[int, int, str, State]] = [(heuristic(start_node, goal_node), 0, "", start_node)]
    visited: Dict[State, int] = {start_node: 0} 

    while priority_queue:
        f_cost_ignored, g_cost, path, current_state = heapq.heappop(priority_queue)

        if current_state == goal_node:
            return path, time.time() - start_time

        if g_cost > visited[current_state]:
             continue

        for move, next_state in ke(current_state):
            new_g_cost = g_cost + 1

            if next_state not in visited or new_g_cost < visited[next_state]:
                visited[next_state] = new_g_cost
                h_cost = heuristic(next_state, goal_node)
                f_cost = new_g_cost + h_cost
                heapq.heappush(priority_queue, (f_cost, new_g_cost, path + move, next_state))

    return "No Solution", time.time() - start_time

def ida_star(start_node: State, goal_node: State) -> Tuple[str, float]:
    start_time = time.time()
    bound = heuristic(start_node, goal_node) 

    while True:

        result = search_ida([start_node], "", 0, bound, goal_node)

        if isinstance(result, str): 
            return result, time.time() - start_time

        if result == float('inf'): 
            return "No Solution", time.time() - start_time

        if not isinstance(result, (int, float)):
             print(f"Error: Unexpected IDA* result type: {type(result)}, value: {result}")
             return "Error in IDA*", time.time() - start_time

        bound = result

def search_ida(nodes_in_current_path: List[State], current_path_moves: str, g_cost: int, bound: float, goal_node: State) -> Union[str, float]:
    current_state = nodes_in_current_path[-1]
    h_cost = heuristic(current_state, goal_node)
    f_cost = g_cost + h_cost

    if f_cost > bound:
        return f_cost 

    if current_state == goal_node:
        return current_path_moves 

    min_exceeding_cost = float('inf')

    for move, next_state in ke(current_state):

        if next_state not in nodes_in_current_path:
            nodes_in_current_path.append(next_state) 

            result = search_ida(nodes_in_current_path, current_path_moves + move, g_cost + 1, bound, goal_node)

            nodes_in_current_path.pop() 

            if isinstance(result, str): 
                return result 

            if isinstance(result, (int, float)):
                 min_exceeding_cost = min(min_exceeding_cost, result)

    return min_exceeding_cost 

def simple_hill_climbing(start_node: State, goal_node: State, max_iterations: int = 1000) -> Tuple[str, float]:
    start_time = time.time()
    current_state = start_node
    current_h = heuristic(current_state, goal_node)
    path = ""

    for _ in range(max_iterations):
        if current_state == goal_node:
            return path, time.time() - start_time

        neighbors = ke(current_state)
        moved = False

        random.shuffle(neighbors)
        for move, next_state in neighbors:
            next_h = heuristic(next_state, goal_node)
            if next_h < current_h: 
                current_state = next_state
                current_h = next_h
                path += move
                moved = True
                break 

        if not moved: 
            break 

    return (path if current_state == goal_node else "No Solution (local optimum?)"), time.time() - start_time

def steepest_hill_climbing(start_node: State, goal_node: State, max_iterations: int = 1000) -> Tuple[str, float]:
    start_time = time.time()
    current_state = start_node
    current_h = heuristic(current_state, goal_node)
    path = ""

    for _ in range(max_iterations):
        if current_state == goal_node:
            return path, time.time() - start_time

        neighbors = ke(current_state)
        best_neighbor = None
        best_h = current_h 
        best_move = ""

        for move, next_state in neighbors:
            next_h = heuristic(next_state, goal_node)
            if next_h < best_h: 
                best_h = next_h
                best_neighbor = next_state
                best_move = move

        if best_neighbor is not None and best_h < current_h:
            current_state = best_neighbor
            current_h = best_h
            path += best_move
        else: 
            break 

    return (path if current_state == goal_node else "No Solution (local optimum?)"), time.time() - start_time

def stochastic_hill_climbing(start_node: State, goal_node: State, max_iterations: int = 5000) -> Tuple[str, float]:
    start_time = time.time()
    current_state = start_node
    current_h = heuristic(current_state, goal_node)
    path = ""

    for _ in range(max_iterations):
        if current_state == goal_node:
            return path, time.time() - start_time

        neighbors = ke(current_state)
        uphill_neighbors = [] 
        for move, next_state in neighbors:
            next_h = heuristic(next_state, goal_node)

            if next_h < current_h:
                 uphill_neighbors.append((move, next_state, next_h))

        if not uphill_neighbors:
             break 

        chosen_move, next_state, next_h = random.choice(uphill_neighbors)

        current_state = next_state
        current_h = next_h
        path += chosen_move

    return (path if current_state == goal_node else "No Solution (local optimum/limit?)"), time.time() - start_time

def simulated_annealing(start_node: State, goal_node: State, initial_temp: float = 100, cooling_rate: float = 0.995, min_temp: float = 0.1, max_iterations: int = 20000) -> Tuple[str, float]:
    start_time = time.time()
    current_state = start_node
    current_h = heuristic(current_state, goal_node)

    best_state = current_state
    best_h = current_h
    temp = initial_temp
    iterations = 0

    path_states: Dict[State, str] = {start_node: ""}

    while temp > min_temp and iterations < max_iterations:
        if current_state == goal_node:
            final_path = path_states.get(goal_node, "Path Error (Goal reached but not tracked?)")
            return final_path, time.time() - start_time

        neighbors = ke(current_state)
        if not neighbors: 
            break

        move, next_state = random.choice(neighbors)
        next_h = heuristic(next_state, goal_node)

        delta_h = next_h - current_h 

        accept = False
        if delta_h < 0: 
            accept = True
        else: 
            try:
                acceptance_prob = math.exp(-delta_h / temp)
                accept = random.random() < acceptance_prob
            except OverflowError: 
                 accept = False

        if accept:

            current_path_to_old_state = path_states.get(current_state, "") 
            new_path_to_next_state = current_path_to_old_state + move

            if next_state not in path_states or len(new_path_to_next_state) < len(path_states[next_state]):
                  path_states[next_state] = new_path_to_next_state

            current_state = next_state
            current_h = next_h

            if current_h < best_h:
                best_h = current_h
                best_state = current_state

        temp *= cooling_rate
        iterations += 1

    result_path = "No Solution (SA limit/cooled)"

    if best_state == goal_node:

        result_path = path_states.get(best_state, "Goal Found (SA path tracking error)")

    return result_path, time.time() - start_time

def genetic_algorithm(start_node: State, goal_node: State, population_size: int = 100, generations: int = 150, mutation_rate: float = 0.15, elite_size: int = 5) -> Tuple[str, float]:
    start_time = time.time()

    def fitness(state: State, goal: State = goal_node) -> float:
        h = heuristic(state, goal)

        return 1.0 / (1.0 + h)

    def mutate(state: State) -> State:
        neighbors = ke(state)
        if neighbors:
            _, mutated_state = random.choice(neighbors)
            return mutated_state
        return state 

    population: Set[State] = {start_node}
    q: Deque[Tuple[State, int]] = deque([(start_node, 0)]) 
    visited_init: Set[State] = {start_node}
    initial_explore_depth = 4 

    while len(population) < population_size // 2 and q: 
         curr, depth = q.popleft()
         if depth >= initial_explore_depth: continue
         for _, neighbor in ke(curr):
             if neighbor not in visited_init and len(population) < population_size // 2:
                 visited_init.add(neighbor)
                 population.add(neighbor)
                 q.append((neighbor, depth + 1))

    while len(population) < population_size:
         p = list(range(9)) 
         random.shuffle(p)

         population.add(tuple(p))

    best_state_overall = start_node
    best_fitness_overall = fitness(start_node)

    for gen in range(generations):

        pop_with_fitness: List[Tuple[float, State]] = [(fitness(state), state) for state in population]
        pop_with_fitness.sort(reverse=True, key=lambda x: x[0]) 

        if pop_with_fitness[0][0] == 1.0: 

            return "Goal Found (GA - No Path)", time.time() - start_time

        current_gen_best_fitness, current_gen_best_state = pop_with_fitness[0]
        if current_gen_best_fitness > best_fitness_overall:
             best_fitness_overall = current_gen_best_fitness
             best_state_overall = current_gen_best_state

        new_population: Set[State] = set()

        elites = {state for _, state in pop_with_fitness[:elite_size]}
        new_population.update(elites)

        population_list = [state for _, state in pop_with_fitness] 
        while len(new_population) < population_size:

             p1 = random.choice(population_list)
             p2 = random.choice(population_list)
             parent = p1 if fitness(p1) >= fitness(p2) else p2

             offspring = mutate(parent) if random.random() < mutation_rate else parent
             new_population.add(offspring)

        population = new_population

        population.add(best_state_overall)

        while len(population) > population_size:

             population.pop() 

    final_message = "No Solution (GA limit)"

    if best_state_overall == goal_node:
        final_message = "Goal Found (GA - No Path)"

    return final_message, time.time() - start_time

def bfs_sensorless(initial_belief_state: BeliefState, goal_state: State) -> Tuple[str, float]:
    start_time = time.time()

    if not isinstance(initial_belief_state, set) or not initial_belief_state:
        return "Error: Invalid input set", time.time() - start_time
    if not all(isinstance(s, tuple) and len(s) == 9 for s in initial_belief_state):
         return "Error: Invalid states in input set", time.time() - start_time
    if not (isinstance(goal_state, tuple) and len(goal_state) == 9):
         return "Error: Invalid goal state", time.time() - start_time

    queue: Deque[Tuple[str, BeliefState]] = deque([("", initial_belief_state)])

    visited: Set[frozenset[State]] = {frozenset(initial_belief_state)}

    while queue:
        path, current_belief = queue.popleft()

        all_states_are_goal = all(s == goal_state for s in current_belief)
        if all_states_are_goal:
             return path, time.time() - start_time

        next_belief_states_per_move: Dict[str, BeliefState] = {}

        possible_moves = ['U', 'D', 'L', 'R'] 
        for move in possible_moves:
            next_belief_for_this_move: BeliefState = set()
            possible_for_all = True
            for state in current_belief: 

                found_next = False
                for m, next_state_tuple in ke(state): 
                    if m == move:
                        next_belief_for_this_move.add(next_state_tuple)
                        found_next = True
                        break

            if next_belief_for_this_move:
                 next_belief_states_per_move[move] = next_belief_for_this_move

        for move, next_belief in next_belief_states_per_move.items():

            frozen_next_belief = frozenset(next_belief)
            if frozen_next_belief not in visited:
                visited.add(frozen_next_belief)

                queue.append((path + move, next_belief))

    return "No Solution", time.time() - start_time
def backtracking(start_node: State, goal_node: State, max_depth: int = 1000) -> Tuple[str, float]:
    """Backtracking algorithm with depth limit."""
    start_time = time.time()

    stack = [("", start_node, 0)]  # Stack to simulate recursion: (path, current_state, depth)
    visited = set()

    while stack:
        path, current_state, depth = stack.pop()

        if depth > max_depth:
            continue  # Skip if depth exceeds max_depth

        if current_state == goal_node:
            return path, time.time() - start_time

        if current_state not in visited:
            visited.add(current_state)

            for move, next_state in ke(current_state):
                if next_state not in visited:
                    stack.append((path + move, next_state, depth + 1))

    return "No Solution", time.time() - start_time


def csp_backtracking(start_node: State, goal_node: State, max_depth: int = 1000) -> Tuple[str, float]:
    """CSP Backtracking algorithm with depth limit."""
    start_time = time.time()

    def is_valid(state: State) -> bool:
        """Check if a state satisfies the constraints (e.g., valid puzzle state)."""
        return len(state) == 9 and set(state) == set(range(9))

    stack = [("", start_node, 0)]  # Stack to simulate recursion: (path, current_state, depth)
    visited = set()

    while stack:
        path, current_state, depth = stack.pop()

        if depth > max_depth:
            continue  # Skip if depth exceeds max_depth

        if current_state == goal_node:
            return path, time.time() - start_time

        if current_state not in visited:
            visited.add(current_state)

            for move, next_state in ke(current_state):
                if next_state not in visited and is_valid(next_state):
                    stack.append((path + move, next_state, depth + 1))

    return "No Solution", time.time() - start_time
algo_functions = {
    "BFS": bfs,
    "DFS": dfs,
    "IDDFS": iddfs,
    "Greedy": greedy,
    "UCS": ucs,
    "A*": astar,
    "IDA*": ida_star,
    "Simple HC": simple_hill_climbing,
    "Steepest HC": steepest_hill_climbing,
    "Stochastic HC": stochastic_hill_climbing,
    "Simulated Annealing": simulated_annealing,
    "Genetic Algorithm": genetic_algorithm,
    "BFS Sensorless": bfs_sensorless, 
     "Backtracking": backtracking,
    "CSP Backtracking": csp_backtracking,
}

def run_algorithm(algo_func, algo_name: str):
    global current_algo, solution_info
    current_algo = algo_name
    print(f"\nRunning Algorithm: {algo_name}") 

    solution_info = {"path": "Solving...", "solve_time": 0.0, "display_time": 0.0}
    s.fill(C_WHITE)

    ve_board(d)
    ve_ui(solution_info)
    pygame.display.flip()
    pygame.time.wait(50) 

    solve_start_time = time.time()
    path_result = "Error: Algo func not found"
    solve_time = 0.0

    try:

        if algo_name == "BFS Sensorless":

            initial_belief_state: BeliefState = {d} 
            path_result, solve_time = algo_func(initial_belief_state, g)
        elif algo_name in algo_functions:

            path_result, solve_time = algo_func(d, g)
        else:
            print(f"Error: Algorithm function not implemented for {algo_name}")

    except Exception as e:
        path_result = f"Error during solve: {e}"
        solve_time = time.time() - solve_start_time
        print(f"Exception occurred in {algo_name}: {e}")
        import traceback
        traceback.print_exc() 

    display_start_time = time.time()
    solution_info = {"path": path_result, "solve_time": solve_time, "display_time": 0.0}
    print(f"Result: {path_result}")
    print(f"Solve Time: {solve_time:.4f} s")

    current_visual_state = list(d)
    animation_possible = (isinstance(path_result, str) and
                          "No Solution" not in path_result and
                          "Error" not in path_result and
                          "Found (GA" not in path_result and 
                          path_result) 

    s.fill(C_WHITE)
    ve_board(tuple(current_visual_state))
    ve_ui(solution_info)
    pygame.display.flip()

    if animation_possible:
        print("Animating path...")
        for move_idx, move_char in enumerate(path_result):

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                     handle_click(event.pos) 

                     if current_algo != algo_name:
                         print("Algorithm changed during animation, stopping.")
                         return 

            try:
                z = current_visual_state.index(0) 
            except ValueError:
                 print(f"Animation Error: 0 not found in state {tuple(current_visual_state)}")
                 solution_info["path"] = "Animation Error: Invalid state"
                 break 

            nz = -1 
            r, c = z // 3, z % 3 

            if move_char == 'U' and r > 0: nz = z - 3
            elif move_char == 'D' and r < 2: nz = z + 3
            elif move_char == 'L' and c > 0: nz = z - 1
            elif move_char == 'R' and c < 2: nz = z + 1
            else:

                 print(f"Error: Invalid move '{move_char}' attempted in sequence at index {move_idx} from state {tuple(current_visual_state)} (empty at {z})")
                 solution_info["path"] = f"Error: Invalid move '{move_char}' in path at step {move_idx+1}"

                 s.fill(C_WHITE)
                 ve_board(tuple(current_visual_state)) 
                 ve_ui(solution_info)
                 pygame.display.flip()
                 animation_possible = False 
                 break 

            if nz != -1:

                current_visual_state[z], current_visual_state[nz] = current_visual_state[nz], current_visual_state[z]

                current_display_time = time.time() - display_start_time
                solution_info["display_time"] = current_display_time

                s.fill(C_WHITE)

                ve_board(tuple(current_visual_state), highlighted_tile_index=z) 

                ve_ui(solution_info)
                pygame.display.flip()
                pygame.time.wait(200) 

    final_display_time = time.time() - display_start_time
    solution_info["display_time"] = final_display_time
    s.fill(C_WHITE)

    ve_board(tuple(current_visual_state))
    ve_ui(solution_info) 
    pygame.display.flip()
    print("Run finished.")

def handle_click(pos: Tuple[int, int]):
    """Handles mouse clicks for dropdown interaction."""
    global dropdown_active, current_algo

    if dropdown_rect.collidepoint(pos):
        dropdown_active = not dropdown_active

        s.fill(C_WHITE)

        ve_board(d)
        ve_ui(solution_info)
        pygame.display.flip()
        return

    if dropdown_active:
        clicked_on_item = False
        for i, item_rect in enumerate(dropdown_item_rects):
            if item_rect.collidepoint(pos):
                selected_algo_name = algorithms[i]
                print(f"Selected: {selected_algo_name}")
                if selected_algo_name in algo_functions:
                     current_algo = selected_algo_name 
                     algo_func = algo_functions[selected_algo_name]
                     dropdown_active = False 

                     run_algorithm(algo_func, selected_algo_name)

                     clicked_on_item = True

                     break
                else:
                     print(f"Error: Algorithm function for '{selected_algo_name}' not implemented.")
                     current_algo = "None" 
                     solution_info["path"] = f"Error: {selected_algo_name} not implemented."
                     dropdown_active = False
                     clicked_on_item = True

                     s.fill(C_WHITE)
                     ve_board(d)
                     ve_ui(solution_info)
                     pygame.display.flip()
                     break

        dropdown_area_rect = pygame.Rect(dropdown_rect.left, dropdown_rect.top,
                                        dropdown_rect.width, dropdown_rect.height + len(dropdown_item_rects)*dropdown_item_height)
        if not clicked_on_item and not dropdown_area_rect.collidepoint(pos):
            dropdown_active = False

            s.fill(C_WHITE)
            ve_board(d) 
            ve_ui(solution_info)
            pygame.display.flip()

def main():
    global dropdown_active 

    clock = pygame.time.Clock()
    running = True

    s.fill(C_WHITE)
    ve_board(d) 
    ve_ui(solution_info)
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                 if event.button == 1: 
                    handle_click(event.pos)

        clock.tick(30) 

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()