import pygame, sys, time, heapq
from collections import deque, defaultdict
import random
import math

from typing import List, Tuple, Deque, Set, Dict, Optional, Union

pygame.init()
w, h = 600, 650
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
C_BUTTON_BLUE = (0, 100, 200) 

f = pygame.font.Font(None, 36)
f2 = pygame.font.Font(None, 24)
f_dropdown = pygame.font.Font(None, 20)
f_button = pygame.font.Font(None, 28) 

State = Tuple[int, ...]
BeliefState = Set[State]
Action = str

d: State = (2, 6, 5, 1, 3, 8, 4, 7, 0)
g: State = (1, 2, 3, 4, 5, 6, 7, 8, 0)

current_algo = "None"
solution_info = {"path": "", "solve_time": 0.0, "display_time": 0.0}
algorithms = [
    "BFS", "DFS", "IDDFS", "Greedy", "UCS", "A*", "IDA*",
    "Simple HC", "Steepest HC", "Stochastic HC",
    "Simulated Annealing", "Genetic Algorithm", "BFS Sensorless",
    "Backtracking", "CSP Backtracking",
    "Q-Learning"
]
dropdown_active = False
dropdown_rect = pygame.Rect(350, 200, 200, 30)
dropdown_item_height = 25
dropdown_item_rects = []

start_button_rect = pygame.Rect(dropdown_rect.left, dropdown_rect.bottom - 60, dropdown_rect.width, 30) 

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

    s.blit(f2.render(f"Start: {d}", True, C_BLACK), (info_x, info_y))
    s.blit(f2.render(f"Goal:  {g}", True, C_BLACK), (info_x, info_y + 30))
    s.blit(f2.render(f"Algorithm: {current_algo}", True, C_BLACK), (info_x, info_y + 60))
    time_label = "Training+Solve" if current_algo == "Q-Learning" else "Processing Time"
    s.blit(f2.render(f"{time_label}: {info['solve_time']:.4f} s", True, C_BLACK), (info_x, info_y + 90))
    s.blit(f2.render(f"Display Time: {info['display_time']:.4f} s", True, C_BLACK), (info_x, info_y + 120))

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

    if dropdown_active:
        base_y = dropdown_rect.bottom + 2

        for i, algo_name in enumerate(algorithms):

            item_rect = pygame.Rect(dropdown_rect.left, base_y + i * dropdown_item_height, dropdown_rect.width, dropdown_item_height)

            dropdown_item_rects.append(item_rect)
            bg_color = C_BLUE if item_rect.collidepoint(pygame.mouse.get_pos()) else C_LIGHT_GRAY
            pygame.draw.rect(s, bg_color, item_rect)
            pygame.draw.rect(s, C_DARK_GRAY, item_rect, 1)
            item_text = f_dropdown.render(algo_name, True, C_BLACK)
            s.blit(item_text, (item_rect.x + 5, item_rect.y + 5))

    pygame.draw.rect(s, C_BUTTON_BLUE, start_button_rect, border_radius=5)
    pygame.draw.rect(s, C_BLACK, start_button_rect, 1, border_radius=5)
    start_text_surf = f_button.render("Start", True, C_WHITE)
    start_text_rect = start_text_surf.get_rect(center=start_button_rect.center)
    s.blit(start_text_surf, start_text_rect)

    path_area_y = start_button_rect.bottom + 130
    max_width, padding = w - 40, 20 
    text_x, text_y = padding, path_area_y + 30
    s.blit(f2.render("Path:", True, C_BLACK), (padding, path_area_y))

    path_display = info['path']
    if isinstance(path_display, str):
        display_string = path_display
        current_line = ""
        max_lines = (h - text_y) // (f2.get_height() + 2) 
        line_count = 0
        for char in display_string:
            if line_count >= max_lines:
                 last_line_surf = f2.render(current_line + "...", True, C_BLACK)
                 s.blit(last_line_surf, (text_x, text_y))
                 current_line = "" 
                 break

            test_line = current_line + char
            text_surf_test = f2.render(test_line, True, C_BLACK)

            if text_surf_test.get_width() > max_width:
                s.blit(f2.render(current_line, True, C_BLACK), (text_x, text_y))
                text_y += f2.get_height() + 2
                line_count += 1
                current_line = char
            else:
                current_line = test_line

        if current_line and line_count < max_lines:
             s.blit(f2.render(current_line, True, C_BLACK), (text_x, text_y))

    elif isinstance(path_display, list):
         s.blit(f2.render(str(path_display), True, C_BLACK), (text_x, text_y))

def ke(x: State) -> List[Tuple[Action, State]]:
    neighbors = []
    try:
        z = x.index(0)
    except ValueError:
        print(f"Error: State {x} does not contain 0!")
        return []

    r, c = z // 3, z % 3

    possible_moves: List[Tuple[int, int, Action]] = [(1, 0, 'D'), (-1, 0, 'U'), (0, 1, 'R'), (0, -1, 'L')]

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
    start_time = time.perf_counter()
    queue: Deque[Tuple[str, State]] = deque([("", start_node)])
    visited: Set[State] = {start_node}

    while queue:
        path, current_state = queue.popleft()
        if current_state == goal_node:
            return path, time.perf_counter() - start_time

        for move, next_state in ke(current_state):
            if next_state not in visited:
                visited.add(next_state)
                queue.append((path + move, next_state))

    return "No Solution", time.perf_counter() - start_time

def dfs(start_node: State, goal_node: State, max_depth: int = 30) -> Tuple[str, float]:
    start_time = time.perf_counter()
    stack: List[Tuple[str, State, int]] = [("", start_node, 0)]
    visited: Dict[State, int] = {start_node: 0}

    while stack:
        path, current_state, depth = stack.pop()

        if current_state == goal_node:
            return path, time.perf_counter() - start_time

        if depth >= max_depth:
            continue

        for move, next_state in reversed(ke(current_state)):
            new_depth = depth + 1
            if next_state not in visited or new_depth < visited[next_state]:
                visited[next_state] = new_depth
                stack.append((path + move, next_state, new_depth))

    return f"No Solution (depth limit {max_depth}?)", time.perf_counter() - start_time

def ucs(start_node: State, goal_node: State) -> Tuple[str, float]:
    start_time = time.perf_counter()
    priority_queue: List[Tuple[int, str, State]] = [(0, "", start_node)]
    visited: Dict[State, int] = {start_node: 0}

    while priority_queue:
        cost, path, current_state = heapq.heappop(priority_queue)

        if current_state == goal_node:
            return path, time.perf_counter() - start_time

        if cost > visited[current_state]:
            continue

        for move, next_state in ke(current_state):
            new_cost = cost + 1
            if next_state not in visited or new_cost < visited[next_state]:
                visited[next_state] = new_cost
                heapq.heappush(priority_queue, (new_cost, path + move, next_state))

    return "No Solution", time.perf_counter() - start_time

def iddfs(start_node: State, goal_node: State, max_limit: int = 50) -> Tuple[str, float]:
    start_time = time.perf_counter()
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
            return result, time.perf_counter() - start_time

    return f"No Solution (within limit {max_limit})", time.perf_counter() - start_time

def greedy(start_node: State, goal_node: State) -> Tuple[str, float]:
    start_time = time.perf_counter()
    priority_queue: List[Tuple[int, str, State]] = [(heuristic(start_node, goal_node), "", start_node)]
    visited: Set[State] = {start_node}

    while priority_queue:
        _, path, current_state = heapq.heappop(priority_queue)

        if current_state == goal_node:
            return path, time.perf_counter() - start_time

        for move, next_state in ke(current_state):
            if next_state not in visited:
                visited.add(next_state)
                h_cost = heuristic(next_state, goal_node)
                heapq.heappush(priority_queue, (h_cost, path + move, next_state))

    return "No Solution", time.perf_counter() - start_time

def astar(start_node: State, goal_node: State) -> Tuple[str, float]:
    start_time = time.perf_counter()
    priority_queue: List[Tuple[int, int, str, State]] = [(heuristic(start_node, goal_node), 0, "", start_node)]
    visited: Dict[State, int] = {start_node: 0}

    while priority_queue:
        f_cost_ignored, g_cost, path, current_state = heapq.heappop(priority_queue)

        if current_state == goal_node:
            return path, time.perf_counter() - start_time

        if g_cost > visited[current_state]:
             continue

        for move, next_state in ke(current_state):
            new_g_cost = g_cost + 1
            if next_state not in visited or new_g_cost < visited[next_state]:
                visited[next_state] = new_g_cost
                h_cost = heuristic(next_state, goal_node)
                f_cost = new_g_cost + h_cost
                heapq.heappush(priority_queue, (f_cost, new_g_cost, path + move, next_state))

    return "No Solution", time.perf_counter() - start_time

def ida_star(start_node: State, goal_node: State) -> Tuple[str, float]:
    start_time = time.perf_counter()
    bound = heuristic(start_node, goal_node)

    while True:
        result = search_ida([start_node], "", 0, bound, goal_node)

        if isinstance(result, str):
            return result, time.perf_counter() - start_time
        if result == float('inf'):
            return "No Solution", time.perf_counter() - start_time
        if not isinstance(result, (int, float)):
             print(f"Error: Unexpected IDA* result type: {type(result)}, value: {result}")
             return "Error in IDA*", time.perf_counter() - start_time

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
    start_time = time.perf_counter()
    current_state = start_node
    current_h = heuristic(current_state, goal_node)
    path = ""

    for _ in range(max_iterations):
        if current_state == goal_node:
            return path, time.perf_counter() - start_time

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

    return (path if current_state == goal_node else "No Solution (local optimum?)"), time.perf_counter() - start_time

def steepest_hill_climbing(start_node: State, goal_node: State, max_iterations: int = 1000) -> Tuple[str, float]:
    start_time = time.perf_counter()
    current_state = start_node
    current_h = heuristic(current_state, goal_node)
    path = ""

    for _ in range(max_iterations):
        if current_state == goal_node:
            return path, time.perf_counter() - start_time

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

    return (path if current_state == goal_node else "No Solution (local optimum?)"), time.perf_counter() - start_time

def stochastic_hill_climbing(start_node: State, goal_node: State, max_iterations: int = 5000) -> Tuple[str, float]:
    start_time = time.perf_counter()
    current_state = start_node
    current_h = heuristic(current_state, goal_node)
    path = ""

    for _ in range(max_iterations):
        if current_state == goal_node:
            return path, time.perf_counter() - start_time

        neighbors = ke(current_state)
        uphill_neighbors = []
        for move, next_state in neighbors:
            next_h = heuristic(next_state, goal_node)
            if next_h < current_h:
                 uphill_neighbors.append((move, next_state, next_h))

        if uphill_neighbors:
            chosen_move, next_state, next_h = random.choice(uphill_neighbors)
            current_state = next_state
            current_h = next_h
            path += chosen_move
        else:
             break

    return (path if current_state == goal_node else "No Solution (local optimum/limit?)"), time.perf_counter() - start_time

def simulated_annealing(start_node: State, goal_node: State, initial_temp: float = 100, cooling_rate: float = 0.995, min_temp: float = 0.1, max_iterations: int = 20000) -> Tuple[str, float]:
    start_time = time.perf_counter()
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
            return final_path, time.perf_counter() - start_time

        neighbors = ke(current_state)
        if not neighbors: break

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

    return result_path, time.perf_counter() - start_time

def genetic_algorithm(start_node: State, goal_node: State, population_size: int = 100, generations: int = 150, mutation_rate: float = 0.15, elite_size: int = 5) -> Tuple[str, float]:
    ga_start_time = time.perf_counter() 

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
    goal_found_in_ga = False

    for gen in range(generations):
        pop_with_fitness: List[Tuple[float, State]] = [(fitness(state), state) for state in population]
        pop_with_fitness.sort(reverse=True, key=lambda x: x[0])

        if pop_with_fitness[0][0] == 1.0:

            best_state_overall = pop_with_fitness[0][1] 
            goal_found_in_ga = True
            print(f"GA found goal state in generation {gen}.")
            break 

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

    ga_end_time = time.perf_counter() 
    ga_time = ga_end_time - ga_start_time

    final_path = "No Solution (GA limit)"
    total_time = ga_time

    if best_state_overall == goal_node or goal_found_in_ga:
        print("Goal state confirmed by GA. Searching for path using A*...")

        astar_path, astar_time = astar(start_node, goal_node) 
        total_time = ga_time + astar_time 

        if "No Solution" not in astar_path and "Error" not in astar_path:
            print(f"A* found path: {len(astar_path)} steps in {astar_time:.4f}s")
            final_path = astar_path 
        else:
            print(f"A* failed to find path ({astar_path}) after GA found goal.")

            final_path = f"GA Found Goal, but A* failed ({astar_path})"

    return final_path, total_time

def bfs_sensorless(initial_belief_state: BeliefState, goal_state: State) -> Tuple[str, float]:
    start_time = time.perf_counter()
    if not isinstance(initial_belief_state, set) or not initial_belief_state:
        return "Error: Invalid input set", time.perf_counter() - start_time
    if not all(isinstance(s, tuple) and len(s) == 9 for s in initial_belief_state):
         return "Error: Invalid states in input set", time.perf_counter() - start_time
    if not (isinstance(goal_state, tuple) and len(goal_state) == 9):
         return "Error: Invalid goal state", time.perf_counter() - start_time

    queue: Deque[Tuple[str, BeliefState]] = deque([("", initial_belief_state)])
    visited: Set[frozenset[State]] = {frozenset(initial_belief_state)}

    while queue:
        path, current_belief = queue.popleft()

        all_states_are_goal = all(s == goal_state for s in current_belief)
        if all_states_are_goal:
             return path, time.perf_counter() - start_time

        next_belief_states_per_move: Dict[Action, BeliefState] = {}
        possible_moves: List[Action] = ['U', 'D', 'L', 'R']

        for move in possible_moves:
            next_belief_for_this_move: BeliefState = set()
            for state in current_belief:
                found_next_for_state = False
                for m, next_state_tuple in ke(state):
                    if m == move:
                        next_belief_for_this_move.add(next_state_tuple)
                        found_next_for_state = True
                        break
            if next_belief_for_this_move:
                 next_belief_states_per_move[move] = next_belief_for_this_move

        for move, next_belief in next_belief_states_per_move.items():
            frozen_next_belief = frozenset(next_belief)
            if frozen_next_belief not in visited:
                visited.add(frozen_next_belief)
                queue.append((path + move, next_belief))

    return "No Solution", time.perf_counter() - start_time

def backtracking(start_node: State, goal_node: State, max_depth: int = 30) -> Tuple[str, float]:
    start_time = time.perf_counter()
    stack = [("", start_node, [start_node])]

    while stack:
        path, current_state, nodes_in_path = stack.pop()

        if current_state == goal_node:
            return path, time.perf_counter() - start_time

        if len(path) >= max_depth:
            continue

        for move, next_state in reversed(ke(current_state)):
            if next_state not in nodes_in_path:
                new_path_nodes = nodes_in_path + [next_state]
                stack.append((path + move, next_state, new_path_nodes))

    return f"No Solution (depth limit {max_depth}?)", time.perf_counter() - start_time

def csp_backtracking(start_node: State, goal_node: State, max_depth: int = 30) -> Tuple[str, float]:
    start_time = time.perf_counter()
    stack = [("", start_node, [start_node])]

    while stack:
        path, current_state, nodes_in_path = stack.pop()

        if current_state == goal_node:
            return path, time.perf_counter() - start_time

        if len(path) >= max_depth:
            continue

        for move, next_state in reversed(ke(current_state)):
            if next_state not in nodes_in_path:
                new_path_nodes = nodes_in_path + [next_state]
                stack.append((path + move, next_state, new_path_nodes))

    return f"No Solution (depth limit {max_depth}?)", time.perf_counter() - start_time

def q_learning(
    start_node: State,
    goal_node: State,
    episodes: int = 10000,
    alpha: float = 0.1,
    gamma: float = 0.9,
    epsilon_start: float = 1.0,
    epsilon_end: float = 0.01,
    epsilon_decay: float = 0.999,
    max_steps_per_episode: int = 200,
    max_path_len_solve: int = 100
) -> Tuple[str, float]:
    start_time = time.perf_counter()
    print(f"Starting Q-Learning Training ({episodes} episodes)...")

    q_table: Dict[State, Dict[Action, float]] = defaultdict(lambda: defaultdict(float))
    epsilon = epsilon_start

    for episode in range(episodes):
        current_state: State = start_node

        if episode % 1000 == 0 and episode > 0:
            print(f" Q-Learning Episode: {episode}, Epsilon: {epsilon:.3f}")

        for step in range(max_steps_per_episode):
            if current_state == goal_node:
                break

            valid_moves = ke(current_state)
            if not valid_moves: break

            action: Action
            next_state: State
            if random.random() < epsilon:
                action, next_state = random.choice(valid_moves)
            else:
                best_q = -float('inf')
                best_actions = []
                for move, ns in valid_moves:
                    q_val = q_table[current_state][move]
                    if q_val > best_q:
                        best_q = q_val
                        best_actions = [(move, ns)]
                    elif q_val == best_q:
                         best_actions.append((move, ns))

                if not best_actions:
                     action, next_state = random.choice(valid_moves)
                else:
                     action, next_state = random.choice(best_actions)

            reward: float = -1.0
            if next_state == goal_node:
                reward = 100.0

            max_next_q: float = 0.0
            if next_state != goal_node:
                next_valid_moves_qvals = [q_table[next_state][m] for m, _ in ke(next_state)]
                if next_valid_moves_qvals:
                    max_next_q = max(next_valid_moves_qvals)

            old_q = q_table[current_state][action]
            new_q = old_q + alpha * (reward + gamma * max_next_q - old_q)
            q_table[current_state][action] = new_q

            current_state = next_state

        if epsilon > epsilon_end:
            epsilon *= epsilon_decay

    training_time = time.perf_counter() - start_time
    print(f"Q-Learning Training Finished in {training_time:.4f}s. Extracting path...")

    path = ""
    current_state = start_node
    visited_solve: Set[State] = {current_state}

    for _ in range(max_path_len_solve):
        if current_state == goal_node:
            total_time = time.perf_counter() - start_time
            print(f"Q-Learning Path Found: {path}")
            return path, total_time

        valid_moves = ke(current_state)
        if not valid_moves:
            total_time = time.perf_counter() - start_time
            print("Q-Learning: Stuck during path extraction (no valid moves).")
            return "No Solution (QL Stuck)", total_time

        best_q = -float('inf')
        best_actions_solve = []
        action_to_state_map: Dict[Action, State] = {}

        for move, next_s in valid_moves:
            action_to_state_map[move] = next_s
            q_val = q_table[current_state].get(move, 0.0)
            if q_val > best_q:
                best_q = q_val
                best_actions_solve = [move]
            elif q_val == best_q:
                 best_actions_solve.append(move)

        if not best_actions_solve:
             chosen_action, next_state = random.choice(valid_moves)
             print(f"Warning: QL resorting to random move from {current_state} during extraction.")
        else:
            chosen_action = random.choice(best_actions_solve)
            next_state = action_to_state_map[chosen_action]

        if next_state in visited_solve:
            total_time = time.perf_counter() - start_time
            print(f"Q-Learning: Cycle detected during path extraction ({path + chosen_action}), stopping.")
            return f"No Solution (QL Cycle: ...{path[-10:]})", total_time

        path += chosen_action
        current_state = next_state
        visited_solve.add(current_state)

    total_time = time.perf_counter() - start_time
    print(f"Q-Learning: Max path length ({max_path_len_solve}) reached during extraction.")
    return f"No Solution (QL Max Path {max_path_len_solve})", total_time

algo_functions = {
    "BFS": bfs, "DFS": dfs, "IDDFS": iddfs, "Greedy": greedy, "UCS": ucs,
    "A*": astar, "IDA*": ida_star, "Simple HC": simple_hill_climbing,
    "Steepest HC": steepest_hill_climbing, "Stochastic HC": stochastic_hill_climbing,
    "Simulated Annealing": simulated_annealing, "Genetic Algorithm": genetic_algorithm,
    "BFS Sensorless": bfs_sensorless, "Backtracking": backtracking,
    "CSP Backtracking": csp_backtracking, "Q-Learning": q_learning
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

    solve_start_time = time.perf_counter()
    path_result = "Error: Algo func not found"
    solve_time = 0.0

    try:
        if algo_name == "BFS Sensorless":
            initial_belief_state: BeliefState = {d}
            path_result, solve_time = algo_func(initial_belief_state, g)
        elif algo_name in algo_functions:
            path_result, solve_time = algo_func(d, g)
        else:
            path_result = f"Error: {algo_name} not implemented."
            solve_time = time.perf_counter() - solve_start_time

    except Exception as e:
        path_result = f"Error during solve: {e}"
        solve_time = time.perf_counter() - solve_start_time
        print(f"Exception occurred in {algo_name}: {e}")
        import traceback
        traceback.print_exc()

    display_start_time = time.perf_counter()
    solution_info = {"path": path_result, "solve_time": solve_time, "display_time": 0.0}
    print(f"Result: {path_result}")
    print(f"Solve Time (reported by function): {solve_time:.4f} s")

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

            should_stop_animation = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                     if event.button == 1:

                         previous_algo = current_algo
                         handle_click(event.pos)

                         if current_algo != previous_algo:
                             print("Algorithm selection changed during animation, stopping.")
                             should_stop_animation = True
                             break 

            if should_stop_animation:
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
                 print(f"Error: Invalid move '{move_char}' in path at index {move_idx} from state {tuple(current_visual_state)}")
                 solution_info["path"] = f"Error: Invalid move '{move_char}' in path at step {move_idx+1}"
                 break 

            if nz != -1:
                current_visual_state[z], current_visual_state[nz] = current_visual_state[nz], current_visual_state[z]
                current_display_time = time.perf_counter() - display_start_time
                solution_info["display_time"] = current_display_time
                s.fill(C_WHITE)
                ve_board(tuple(current_visual_state), highlighted_tile_index=z)
                ve_ui(solution_info)
                pygame.display.flip()
                pygame.time.wait(150)

    final_display_time = time.perf_counter() - display_start_time
    solution_info["display_time"] = final_display_time
    s.fill(C_WHITE)
    ve_board(tuple(current_visual_state)) 
    ve_ui(solution_info)
    pygame.display.flip()
    print("Run finished.")

def handle_click(pos: Tuple[int, int]):
    global dropdown_active, current_algo, solution_info 

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

                current_algo = selected_algo_name
                solution_info["path"] = "" 
                solution_info["solve_time"] = 0.0
                solution_info["display_time"] = 0.0

                if selected_algo_name not in algo_functions:
                     print(f"Error: Algorithm function for '{selected_algo_name}' not implemented.")
                     solution_info["path"] = f"Error: {selected_algo_name} not implemented."

                dropdown_active = False
                clicked_on_item = True

                s.fill(C_WHITE)
                ve_board(d)
                ve_ui(solution_info)
                pygame.display.flip()
                break 

        dropdown_full_height = dropdown_rect.height
        if dropdown_item_rects:
            dropdown_full_height += len(dropdown_item_rects) * dropdown_item_height + 2
        dropdown_area_rect = pygame.Rect(dropdown_rect.left, dropdown_rect.top,
                                        dropdown_rect.width, dropdown_full_height)
        if not clicked_on_item and not dropdown_area_rect.collidepoint(pos):
            dropdown_active = False

            s.fill(C_WHITE)
            ve_board(d)
            ve_ui(solution_info)
            pygame.display.flip()

        return 

    if start_button_rect.collidepoint(pos):
        print("Start button clicked.")
        if current_algo != "None" and current_algo in algo_functions:
            print(f"Running selected algorithm: {current_algo}")
            algo_func = algo_functions[current_algo]

            run_algorithm(algo_func, current_algo)
        elif current_algo == "None":
             print("No algorithm selected.")

        else: 
             print(f"Selected algorithm '{current_algo}' cannot be run (not implemented?).")

             solution_info["path"] = f"Error: Cannot run {current_algo}."
             solution_info["solve_time"] = 0.0
             solution_info["display_time"] = 0.0
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