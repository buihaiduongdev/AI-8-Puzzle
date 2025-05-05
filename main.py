import pygame
import sys
import time
import json
from typing import List, Tuple, Optional, Dict, Any
from analyze_results import plot_results 

from algo import (
    State, BeliefState, Action, d_default, g, algo_functions, algorithms,
    bfs_sensorless, heuristic 
)
from ui import (
    W, H, C_WHITE, C_BLACK,
    ve_board, ve_ui,
    DROPDOWN_RECT, START_BUTTON_RECT, COMPARE_BUTTON_RECT, DROPDOWN_ITEM_HEIGHT
)
MAX_RETRIES_PER_ALGO = 20
RETRY_DELAY_SECONDS = 0.1

pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("XepHinh Solver")
clock = pygame.time.Clock()

current_start_state: State = d_default 
current_goal_state: State = g
current_algo: str = "None" 
solution_info: Dict[str, Any] = {
    "path": "",         
    "solve_time": 0.0,  
    "display_time": 0.0 
}
dropdown_active: bool = False 

current_dropdown_item_rects: List[pygame.Rect] = []

def run_algorithm(algo_name: str):
    """Runs the selected algorithm and handles UI updates/animation."""
    global current_algo, solution_info, current_start_state, current_goal_state

    if algo_name == "None" or algo_name not in algo_functions:
        print(f"Cannot run algorithm: {algo_name}")
        solution_info = {"path": f"Select a valid algorithm", "solve_time": 0.0, "display_time": 0.0}
        return

    current_algo = algo_name
    print(f"\nRunning Algorithm: {algo_name}")

    solution_info = {"path": "Solving...", "solve_time": 0.0, "display_time": 0.0}
    redraw_screen() 
    pygame.time.wait(50) 

    solve_start_time = time.perf_counter()
    path_result: Any = f"Error: Algo func '{algo_name}' not found"
    solve_time: float = 0.0
    algo_func = algo_functions[algo_name]

    try:

        if algo_name == "BFS Sensorless":
            initial_belief_state: BeliefState = {current_start_state} 

            path_result, solve_time = bfs_sensorless(initial_belief_state, current_goal_state)

        else:

            path_result, solve_time = algo_func(current_start_state, current_goal_state)

    except Exception as e:
        path_result = f"Error during solve: {e}"
        solve_time = time.perf_counter() - solve_start_time 
        print(f"!!! Exception occurred in {algo_name}: {e}")
        import traceback
        traceback.print_exc()

    display_start_time = time.perf_counter()
    solution_info = {"path": path_result, "solve_time": solve_time, "display_time": 0.0}
    print(f"Result ({algo_name}): {path_result}")
    print(f"Solve Time ({algo_name}): {solve_time:.4f} s")

    animation_possible = (isinstance(path_result, str) and
                          "No Solution" not in path_result and
                          "Error" not in path_result and
                          "Failed" not in path_result and 
                          path_result) 

    current_visual_state = list(current_start_state) 
    redraw_screen(current_visual_state) 

    if animation_possible:
        print("Animating path...")
        paused = False
        for move_idx, move_char in enumerate(path_result):
            while paused: 
                 for event in pygame.event.get():
                     if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                     if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                         paused = False
                         print("Resuming animation...")
                     elif event.type == pygame.MOUSEBUTTONDOWN:

                         prev_algo = current_algo
                         handle_click(event.pos)
                         if prev_algo != current_algo:
                             print("Algorithm changed during pause, stopping animation.")
                             return 
                 redraw_screen(tuple(current_visual_state)) 
                 clock.tick(10) 

            should_stop_animation = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                     paused = True
                     print("Animation paused. Press SPACE to resume.")
                elif event.type == pygame.MOUSEBUTTONDOWN:
                     if event.button == 1:
                         previous_algo = current_algo
                         handle_click(event.pos) 
                         if current_algo != previous_algo:
                             print("Algorithm selection changed during animation, stopping.")
                             should_stop_animation = True
                             break 

            if should_stop_animation:

                 redraw_screen()
                 return 

            try:
                z = current_visual_state.index(0) 
            except ValueError:
                 print(f"Animation Error: 0 not found in state {tuple(current_visual_state)}")
                 solution_info["path"] = "Animation Error: Invalid intermediate state"
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

                moving_tile_index = nz 
                current_visual_state[z], current_visual_state[nz] = current_visual_state[nz], current_visual_state[z]

                current_display_time = time.perf_counter() - display_start_time
                solution_info["display_time"] = current_display_time
                redraw_screen(tuple(current_visual_state), highlighted_tile_index=z) 
                pygame.time.wait(150) 

    final_display_time = time.perf_counter() - display_start_time
    solution_info["display_time"] = final_display_time
    redraw_screen(tuple(current_visual_state)) 
    print(f"Run finished for {algo_name}.")

def compare_algorithms():
    """Runs all implemented algorithms, records solve times, retrying on failure, and saves to JSON."""
    global solution_info, current_algo, current_start_state, current_goal_state

    print("\n--- Starting Algorithm Comparison (with retries on failure) ---")
    current_algo = "Comparing..." 
    solution_info = {"path": "Running comparisons...", "solve_time": 0.0, "display_time": 0.0}
    redraw_screen() 
    pygame.time.wait(50)

    results = {}

    for name, func in algo_functions.items():
        print(f"Comparing: {name}...")
        solution_info["path"] = f"Running: {name}..." 
        redraw_screen() 
        pygame.event.pump() 

        retries = 0
        success = False
        final_path_result: Any = f"Not run yet (error in retry loop for {name})" 
        final_solve_time: float = -1.0 

        while retries < MAX_RETRIES_PER_ALGO and not success:
            attempt_num = retries + 1
            print(f"  Attempt {attempt_num}/{MAX_RETRIES_PER_ALGO} for {name}...")
            solution_info["path"] = f"Running: {name} (Attempt {attempt_num})"
            redraw_screen()
            pygame.event.pump()

            try:

                current_path_result: Any
                current_solve_time: float

                if name == "BFS Sensorless":
                    initial_belief: BeliefState = {current_start_state}
                    current_path_result, current_solve_time = bfs_sensorless(initial_belief, current_goal_state)

                else:
                    current_path_result, current_solve_time = func(current_start_state, current_goal_state)

                final_path_result = current_path_result
                final_solve_time = current_solve_time

                is_valid_path = (
                    isinstance(current_path_result, str) and
                    current_path_result and 
                    "No Solution" not in current_path_result and
                    "Error" not in current_path_result and
                    "Failed" not in current_path_result and
                    "Stuck" not in current_path_result and
                    "Cycle" not in current_path_result

                )

                if is_valid_path:
                    success = True 
                    print(f"    Success on attempt {attempt_num}!")
                else:

                    retries += 1
                    if retries < MAX_RETRIES_PER_ALGO:
                        print(f"    Attempt {attempt_num} failed ('{str(current_path_result)[:60]}...'). Retrying...")
                        time.sleep(RETRY_DELAY_SECONDS) 
                    else:
                         print(f"    Attempt {attempt_num} failed. Max retries reached.")

            except Exception as e:

                print(f"  !!! Error during {name} attempt {attempt_num}: {e}")
                import traceback
                traceback.print_exc() 
                final_path_result = f"Runtime Error on attempt {attempt_num}: {e}"
                final_solve_time = -1.0 
                retries += 1
                if retries < MAX_RETRIES_PER_ALGO:
                     print("      Retrying after error...")
                     time.sleep(RETRY_DELAY_SECONDS)
                else:
                     print("      Max retries reached after error.")

        final_status = "Success" if success else f"Failed after {retries} attempts"

        results[name] = {

            "solve_time": final_solve_time if success else -1.0,

            "path_length": len(final_path_result) if success else None,

            "attempts": retries if not success else retries + 1,
            "final_status": final_status,

            "last_result_message": str(final_path_result) if not success else None
        }

        print(f"  Finished {name}: Status='{final_status}', Time={results[name]['solve_time']:.4f}s, Path Length={results[name]['path_length']}, Attempts={results[name]['attempts']}")
        if not success:
             print(f"    Last Msg: {str(final_path_result)[:100]}...") 

    try:

        sorted_results = dict(sorted(results.items()))
        with open("result.json", "w") as f:
            json.dump(sorted_results, f, indent=4)
        print("\nComparison results saved to result.json")
        solution_info["path"] = "Comparison complete. See result.json"
    except Exception as e:
        print(f"Error saving results to JSON: {e}")
        solution_info["path"] = "Comparison done, but failed to save JSON."

    solution_info["solve_time"] = 0.0 
    current_algo = "None" 
    redraw_screen() 
    print("--- Algorithm Comparison Finished ---")
    plot_results()

def handle_click(pos: Tuple[int, int]):
    """Handles mouse clicks for buttons and dropdown."""
    global dropdown_active, current_algo, solution_info, current_dropdown_item_rects

    if DROPDOWN_RECT.collidepoint(pos):
        dropdown_active = not dropdown_active

        redraw_screen() 
        return 

    if dropdown_active:
        clicked_on_item = False

        for i, item_rect in enumerate(current_dropdown_item_rects):
            if item_rect.collidepoint(pos):
                if i < len(algorithms): 
                    selected_algo_name = algorithms[i]
                    print(f"Selected: {selected_algo_name}")

                    if current_algo != selected_algo_name:
                        current_algo = selected_algo_name

                        solution_info = {"path": "", "solve_time": 0.0, "display_time": 0.0}

                        if selected_algo_name not in algo_functions:
                             print(f"Warning: Algorithm function for '{selected_algo_name}' not found in algo_functions.")
                             solution_info["path"] = f"Error: {selected_algo_name} not implemented?"

                    dropdown_active = False 
                    clicked_on_item = True
                    redraw_screen() 
                    break 

        dropdown_full_height = DROPDOWN_RECT.height
        if current_dropdown_item_rects:

             dropdown_full_height += len(current_dropdown_item_rects) * DROPDOWN_ITEM_HEIGHT + 2
        dropdown_area_rect = pygame.Rect(DROPDOWN_RECT.left, DROPDOWN_RECT.top,
                                        DROPDOWN_RECT.width, dropdown_full_height)

        if not clicked_on_item and not dropdown_area_rect.collidepoint(pos):
            dropdown_active = False

            redraw_screen() 

        return 

    if START_BUTTON_RECT.collidepoint(pos):
        print("Start button clicked.")
        if current_algo != "None":
            run_algorithm(current_algo) 
        else:
             print("No algorithm selected.")
             solution_info["path"] = "Please select an algorithm first."
             redraw_screen()
        return 

    if COMPARE_BUTTON_RECT.collidepoint(pos):
        print("Compare button clicked.")
        compare_algorithms() 
        return 

def redraw_screen(current_state: Optional[State] = None, highlighted_tile_index: Optional[int] = None):
    """Clears the screen and redraws all UI elements."""
    global current_dropdown_item_rects 

    state_to_draw = current_state if current_state else current_start_state

    screen.fill(C_WHITE) 
    ve_board(screen, state_to_draw, highlighted_tile_index) 

    mouse_pos = pygame.mouse.get_pos()
    current_dropdown_item_rects = ve_ui(
        screen,
        current_start_state,
        current_goal_state,
        current_algo,
        solution_info,
        algorithms,
        dropdown_active,
        mouse_pos 
    )

    pygame.display.flip() 

def main():
    global dropdown_active 

    running = True
    redraw_screen(current_start_state) 

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                 if event.button == 1: 
                    handle_click(event.pos)

        if dropdown_active: 
            redraw_screen(current_start_state) 

        clock.tick(30) 

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()