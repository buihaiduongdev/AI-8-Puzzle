import time
import heapq
from collections import deque, defaultdict
import random
import math
from typing import List, Tuple, Deque, Set, Dict, Optional, Union

State = Tuple[int, ...]
BeliefState = Set[State]
Action = str

d_default: State = (2, 6, 5, 1, 3, 8, 4, 7, 0) 
g: State = (1, 2, 3, 4, 5, 6, 7, 8, 0)        

def ke(x: State) -> List[Tuple[Action, State]]:
    """Generates neighboring states and the moves to reach them."""
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
    """Calculates the Manhattan distance heuristic."""
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

def bfs(start_node: State, goal_node: State = g) -> Tuple[Union[str, List[State]], float]:
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

def dfs(start_node: State, goal_node: State = g, max_depth: int = 30) -> Tuple[Union[str, List[State]], float]:
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

def ucs(start_node: State, goal_node: State = g) -> Tuple[Union[str, List[State]], float]:
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

def iddfs(start_node: State, goal_node: State = g, max_limit: int = 50) -> Tuple[Union[str, List[State]], float]:
    start_time = time.perf_counter()

    def dls(path: str, current_state: State, nodes_in_path: List[State], depth_limit: int) -> Optional[str]:
        """Depth Limited Search helper."""
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

def greedy(start_node: State, goal_node: State = g) -> Tuple[Union[str, List[State]], float]:
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

def astar(start_node: State, goal_node: State = g) -> Tuple[Union[str, List[State]], float]:
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

def search_ida(nodes_in_current_path: List[State], current_path_moves: str, g_cost: int, bound: float, goal_node: State) -> Union[str, float]:
    """Recursive helper for IDA*."""
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

def ida_star(start_node: State, goal_node: State = g) -> Tuple[Union[str, List[State]], float]:
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

def simple_hill_climbing(start_node: State, goal_node: State = g, max_iterations: int = 1000) -> Tuple[str, float]:
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

def steepest_hill_climbing(start_node: State, goal_node: State = g, max_iterations: int = 1000) -> Tuple[str, float]:
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

def stochastic_hill_climbing(start_node: State, goal_node: State = g, max_iterations: int = 5000) -> Tuple[str, float]:
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

def simulated_annealing(start_node: State, goal_node: State = g, initial_temp: float = 100, cooling_rate: float = 0.995, min_temp: float = 0.1, max_iterations: int = 20000) -> Tuple[str, float]:
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
    elif current_state == goal_node: 
        result_path = path_states.get(current_state, "Goal Found (SA path tracking error)")

    return result_path, time.perf_counter() - start_time

def genetic_algorithm(start_node: State, goal_node: State = g, population_size: int = 100, generations: int = 150, mutation_rate: float = 0.15, elite_size: int = 5) -> Tuple[str, float]:
    """
    Uses GA to find the goal state, then A* to find the path from start to goal.
    Returns the A* path and the *total* time (GA + A*).
    """
    ga_start_time = time.perf_counter()

    def fitness(state: State, goal: State = goal_node) -> float:
        """Higher fitness for states closer to the goal (lower heuristic)."""
        h = heuristic(state, goal)

        return 1.0 / (1.0 + h)

    def mutate(state: State) -> State:
        """Applies a single random valid move to the state."""
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

    print(f"Starting GA ({generations} generations, pop_size={population_size})...")
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

             p1_idx = random.randrange(len(population_list))
             p2_idx = random.randrange(len(population_list))
             parent = population_list[p1_idx] if pop_with_fitness[p1_idx][0] >= pop_with_fitness[p2_idx][0] else population_list[p2_idx]

             offspring = mutate(parent) if random.random() < mutation_rate else parent
             new_population.add(offspring) 

        population = new_population

        population.add(best_state_overall)

        while len(population) > population_size:
             population.pop() 

        if gen % 20 == 0: 
            print(f"  GA Gen {gen}: Best heuristic = {heuristic(best_state_overall, goal_node)}")

    ga_end_time = time.perf_counter()
    ga_time = ga_end_time - ga_start_time
    print(f"GA finished in {ga_time:.4f}s.")

    final_path = "No Solution (GA limit)"
    total_time = ga_time 

    if best_state_overall == goal_node or goal_found_in_ga:
        print("Goal state candidate found by GA. Searching for path using A*...")

        astar_path, astar_time = astar(start_node, goal_node)
        total_time = ga_time + astar_time 

        if "No Solution" not in astar_path and "Error" not in astar_path:
            print(f"A* found path: {len(astar_path)} steps in {astar_time:.4f}s")
            final_path = astar_path
        else:

            print(f"A* failed to find path ({astar_path}) after GA found goal candidate.")
            final_path = f"GA Found Goal Candidate, but A* failed ({astar_path})"
    else:
        print(f"GA did not find the goal state. Best state heuristic: {heuristic(best_state_overall, goal_node)}")

    return final_path, total_time

def bfs_sensorless(initial_belief_state: BeliefState, goal_state: State = g) -> Tuple[str, float]:
    start_time = time.perf_counter()

    if not isinstance(initial_belief_state, set) or not initial_belief_state:
        return "Error: Invalid input belief state set", time.perf_counter() - start_time
    if not all(isinstance(s, tuple) and len(s) == 9 for s in initial_belief_state):
         return "Error: Invalid states within input belief set", time.perf_counter() - start_time
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

def backtracking(start_node: State, goal_node: State = g, max_depth: int = 30) -> Tuple[str, float]:
    """Simple backtracking search (essentially DFS)."""
    start_time = time.perf_counter()

    stack: List[Tuple[str, State, List[State]]] = [("", start_node, [start_node])]

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

def csp_backtracking(start_node: State, goal_node: State = g, max_depth: int = 30) -> Tuple[str, float]:
    """CSP Backtracking (Functionally equivalent to Backtracking/DFS for this problem)."""

    return backtracking(start_node, goal_node, max_depth)

def q_learning(
    start_node: State,
    goal_node: State = g,
    episodes: int = 10000,        
    alpha: float = 0.1,         
    gamma: float = 0.9,         
    epsilon_start: float = 1.0, 
    epsilon_end: float = 0.01,  
    epsilon_decay: float = 0.999, 
    max_steps_per_episode: int = 200, 
    max_path_len_solve: int = 100     
) -> Tuple[str, float]:
    """Trains a Q-table and then extracts the policy (path)."""
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
    "Q-Learning": q_learning
}

algorithms = list(algo_functions.keys())