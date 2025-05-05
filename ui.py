import pygame
from typing import List, Tuple, Deque, Set, Dict, Optional, Union

pygame.font.init()

W, H = 600, 800 

C_WHITE = (255, 255, 255)
C_BLACK = (0, 0, 0)
C_LIGHT_GRAY = (220, 220, 220)
C_GREEN = (0, 128, 0)
C_BLUE = (100, 100, 255)
C_RED = (255, 100, 100)
C_DARK_GRAY = (200, 200, 200)
C_HIGHLIGHT = (255, 255, 0) 
C_BUTTON_BLUE = (0, 100, 200)
C_COMPARE_ORANGE = (255, 140, 0)

F_MAIN = pygame.font.Font(None, 36) 
F_INFO = pygame.font.Font(None, 24) 
F_DROPDOWN = pygame.font.Font(None, 20) 
F_BUTTON = pygame.font.Font(None, 28) 

BOARD_OFFSET_X, BOARD_OFFSET_Y = 20, 20
TILE_SIZE = 100
BOARD_SIZE = 3 * TILE_SIZE

INFO_X, INFO_Y = BOARD_OFFSET_X + BOARD_SIZE + 30, 20 

DROPDOWN_RECT = pygame.Rect(INFO_X, INFO_Y + 200, 200, 30) 
DROPDOWN_ITEM_HEIGHT = 25

START_BUTTON_RECT = pygame.Rect(DROPDOWN_RECT.left, DROPDOWN_RECT.top - 40, DROPDOWN_RECT.width, 30) 
COMPARE_BUTTON_RECT = pygame.Rect(START_BUTTON_RECT.left, START_BUTTON_RECT.top - 40, START_BUTTON_RECT.width, 30) 

PATH_AREA_Y = DROPDOWN_RECT.bottom + 100
PATH_TEXT_X = BOARD_OFFSET_X
PATH_MAX_WIDTH = W/2 

def ve_board(surface: pygame.Surface, current_state: Tuple[int, ...], highlighted_tile_index: Optional[int] = None):
    """Draws the 8-puzzle board onto the given surface."""
    for i in range(3):
        for j in range(3):
            idx = i * 3 + j
            tile_val = current_state[idx]
            r = pygame.Rect(BOARD_OFFSET_X + j * TILE_SIZE, BOARD_OFFSET_Y + i * TILE_SIZE, TILE_SIZE, TILE_SIZE)

            if idx == highlighted_tile_index:
                color = C_HIGHLIGHT 
            elif tile_val == 0:
                color = C_LIGHT_GRAY 
            else:
                color = C_WHITE 

            pygame.draw.rect(surface, color, r)
            pygame.draw.rect(surface, C_BLACK, r, 1) 

            if tile_val != 0:
                text_surface = F_MAIN.render(str(tile_val), True, C_BLACK)
                text_rect = text_surface.get_rect(center=r.center)
                surface.blit(text_surface, text_rect)

def ve_ui(
    surface: pygame.Surface,
    start_state: Tuple[int, ...],
    goal_state: Tuple[int, ...],
    current_algo: str,
    solution_info: dict,
    algorithms_list: List[str],
    dropdown_active: bool,
    mouse_pos: Tuple[int, int] 
    ) -> List[pygame.Rect]: 
    """Draws the entire UI (info panel, buttons, dropdown, path) onto the surface."""

    surface.blit(F_INFO.render(f"Start: {start_state}", True, C_BLACK), (INFO_X, INFO_Y))
    surface.blit(F_INFO.render(f"Goal:  {goal_state}", True, C_BLACK), (INFO_X, INFO_Y + 30))
    surface.blit(F_INFO.render(f"Algorithm: {current_algo}", True, C_BLACK), (INFO_X, INFO_Y + 60))

    time_label = "Processing Time"
    if current_algo == "Q-Learning":
        time_label = "Train+Solve Time"
    elif current_algo == "Genetic Algorithm":
         time_label = "GA+A* Time"

    surface.blit(F_INFO.render(f"{time_label}: {solution_info.get('solve_time', 0.0):.4f} s", True, C_BLACK), (INFO_X, INFO_Y + 90))
    surface.blit(F_INFO.render(f"Display Time: {solution_info.get('display_time', 0.0):.4f} s", True, C_BLACK), (INFO_X, INFO_Y + 120))

    pygame.draw.rect(surface, C_COMPARE_ORANGE, COMPARE_BUTTON_RECT, border_radius=5)
    pygame.draw.rect(surface, C_BLACK, COMPARE_BUTTON_RECT, 1, border_radius=5)
    compare_text_surf = F_BUTTON.render("Compare All", True, C_WHITE)
    compare_text_rect = compare_text_surf.get_rect(center=COMPARE_BUTTON_RECT.center)
    surface.blit(compare_text_surf, compare_text_rect)

    pygame.draw.rect(surface, C_BUTTON_BLUE, START_BUTTON_RECT, border_radius=5)
    pygame.draw.rect(surface, C_BLACK, START_BUTTON_RECT, 1, border_radius=5)
    start_text_surf = F_BUTTON.render("Start", True, C_WHITE)
    start_text_rect = start_text_surf.get_rect(center=START_BUTTON_RECT.center)
    surface.blit(start_text_surf, start_text_rect)

    pygame.draw.rect(surface, C_GREEN, DROPDOWN_RECT, border_radius=5)
    pygame.draw.rect(surface, C_DARK_GRAY, DROPDOWN_RECT, 1, border_radius=5)
    selected_text = current_algo if current_algo != "None" else "Select Algorithm"
    dropdown_text_surf = F_INFO.render(selected_text, True, C_WHITE)
    dropdown_text_rect = dropdown_text_surf.get_rect(center=DROPDOWN_RECT.center)
    surface.blit(dropdown_text_surf, dropdown_text_rect)

    arrow_points = [(DROPDOWN_RECT.right - 15, DROPDOWN_RECT.centery - 3),
                    (DROPDOWN_RECT.right - 5, DROPDOWN_RECT.centery - 3),
                    (DROPDOWN_RECT.right - 10, DROPDOWN_RECT.centery + 3)]
    pygame.draw.polygon(surface, C_WHITE, arrow_points)

    dropdown_item_rects = []
    if dropdown_active:
        base_y = DROPDOWN_RECT.bottom + 2
        max_items_display = (H - base_y - 10) // DROPDOWN_ITEM_HEIGHT 

        for i, algo_name in enumerate(algorithms_list):
            if i >= max_items_display: break 

            item_rect = pygame.Rect(DROPDOWN_RECT.left, base_y + i * DROPDOWN_ITEM_HEIGHT, DROPDOWN_RECT.width, DROPDOWN_ITEM_HEIGHT)
            dropdown_item_rects.append(item_rect) 

            bg_color = C_BLUE if item_rect.collidepoint(mouse_pos) else C_LIGHT_GRAY
            pygame.draw.rect(surface, bg_color, item_rect)
            pygame.draw.rect(surface, C_DARK_GRAY, item_rect, 1)

            item_text = F_DROPDOWN.render(algo_name, True, C_BLACK)
            surface.blit(item_text, (item_rect.x + 5, item_rect.y + 5))

    path_label_surf = F_INFO.render("Path:", True, C_BLACK)
    surface.blit(path_label_surf, (PATH_TEXT_X, PATH_AREA_Y))

    path_display = solution_info.get('path', '') 
    text_y = PATH_AREA_Y + F_INFO.get_height() + 5 

    if isinstance(path_display, str):
        display_string = path_display
        current_line = ""
        max_lines = (H - text_y) // (F_INFO.get_height() + 2) 
        line_count = 0

        words = display_string.replace('U',' U ').replace('D',' D ').replace('L',' L ').replace('R',' R ').split() 
        current_line_words = []

        for word in words:
            test_line_words = current_line_words + [word]
            test_line = " ".join(test_line_words)
            text_surf_test = F_INFO.render(test_line, True, C_BLACK)

            if text_surf_test.get_width() <= PATH_MAX_WIDTH:
                current_line_words.append(word)
            else:

                line_to_render = " ".join(current_line_words)
                if line_count < max_lines:
                    s = F_INFO.render(line_to_render, True, C_BLACK)
                    surface.blit(s, (PATH_TEXT_X, text_y))
                    text_y += F_INFO.get_height() + 2
                    line_count += 1
                    current_line_words = [word] 
                else:

                    last_line_surf = F_INFO.render(" ".join(current_line_words) + "...", True, C_BLACK)
                    surface.blit(last_line_surf, (PATH_TEXT_X, text_y))
                    current_line_words = [] 
                    break

        if current_line_words and line_count < max_lines:
             last_line = " ".join(current_line_words)
             s = F_INFO.render(last_line, True, C_BLACK)
             surface.blit(s, (PATH_TEXT_X, text_y))

    elif isinstance(path_display, list): 

         s = F_INFO.render(str(path_display)[:100], True, C_BLACK) 
         surface.blit(s, (PATH_TEXT_X, text_y))

    return dropdown_item_rects 