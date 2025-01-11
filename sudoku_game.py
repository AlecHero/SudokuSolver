import pygame
import numpy as np

# Constants
CELL_SIZE = 60
GRID_SIZE = 9

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
top_offset = 2*CELL_SIZE
bot_offset = 2*CELL_SIZE
SCREEN_WIDTH,SCREEN_HEIGHT = (CELL_SIZE*GRID_SIZE, CELL_SIZE*GRID_SIZE+(top_offset+bot_offset))


def draw_grid(screen):
    for i in range(GRID_SIZE + 1):
        if i % 3 == 0:
            pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE + top_offset), (SCREEN_WIDTH, i * CELL_SIZE + top_offset), 3)   
            pygame.draw.line(screen, BLACK, (i * CELL_SIZE, top_offset), (i * CELL_SIZE, SCREEN_HEIGHT - bot_offset), 3)
        else:
            pygame.draw.line(screen, GRAY, (0, i * CELL_SIZE + top_offset), (SCREEN_WIDTH, i * CELL_SIZE + top_offset), 1)
            pygame.draw.line(screen, GRAY, (i * CELL_SIZE, top_offset), (i * CELL_SIZE, SCREEN_HEIGHT - bot_offset), 1)

def draw_numbers(screen, init_board, board, candidates, show_candidates=True, red_coordinates=[]):
    font = pygame.font.SysFont('Arial', 36)
    small_font = pygame.font.SysFont('Arial', 16)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] != 0:
                text = font.render(str(board[i][j]), True, BLUE if init_board[i][j] == 0 else BLACK)
                text_rect = text.get_rect(center=(j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2 + top_offset))
                screen.blit(text, text_rect)
            elif show_candidates:
                for k in range(9):
                    if candidates[k][i][j] != 0:
                        try: small_font.strikethrough = False
                        except: pass
                        text = small_font.render(str(k + 1), True, GRAY)
                        text_rect = text.get_rect(center=(j * CELL_SIZE + (k % 3 + 0.5) * (CELL_SIZE // 3), i * CELL_SIZE + (k // 3 + 0.5) * (CELL_SIZE // 3) + top_offset))
                        screen.blit(text, text_rect)
                    
                    elif (len(red_coordinates) != 0) and ([k,i,j] == red_coordinates).all(1).any():
                        try: small_font.strikethrough = True
                        except: pass
                        text = small_font.render(str(k + 1), True, RED)
                        text_rect = text.get_rect(center=(j * CELL_SIZE + (k % 3 + 0.5) * (CELL_SIZE // 3), i * CELL_SIZE + (k // 3 + 0.5) * (CELL_SIZE // 3) + top_offset))
                        screen.blit(text, text_rect)


def SudokuGame(list_game_states, compare=None, board_names=None):
    if compare is not None: red_coordinates = np.argwhere(list_game_states.candidates != compare.candidates)
    else: red_coordinates = []
    
    if isinstance(list_game_states, list):
        if not isinstance(list_game_states[0], list): list_game_states = [list_game_states]
    else: list_game_states = [[list_game_states]]
    
    
    pygame.init()
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Sudoku Board')
    
    board_idx = 0
    show_candidates = True
    
    def loader(board_idx): return list_game_states[board_idx], len(list_game_states[board_idx])-1
    game_states, game_state_idx = loader(board_idx)
    
    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    game_state_idx = max(0, game_state_idx-1)
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    game_state_idx = min(len(game_states)-1, game_state_idx+1)
                if event.key == pygame.K_c:
                    show_candidates = not show_candidates
                if event.key == pygame.K_r  or event.key == pygame.K_0:
                    game_state_idx = 0
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    board_idx += min(1, len(list_game_states)-1-board_idx)
                    game_states, game_state_idx = loader(board_idx)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    board_idx = max(0, board_idx-1)
                    game_states, game_state_idx = loader(board_idx)

        screen.fill(WHITE)
        board_i = game_states[game_state_idx].board
        candidates_i = game_states[game_state_idx].candidates
        draw_grid(screen)
        draw_numbers(screen, game_states[0].board, board_i, candidates_i, show_candidates, red_coordinates)
        
        font = pygame.font.SysFont('Consolas', 28)
        text_render = lambda text: font.render(text, True, BLACK)
        
        if board_names is not None: board_name = text_render(board_names[board_idx])
        else: board_name = text_render(f"Board: {board_idx+1:>1}")
        solver_text = text_render(game_states[game_state_idx].solver_name)
        solver_step = text_render(f"Step: {game_state_idx+1:>2}/{len(game_states)}")
        score_placed = text_render(f"Placed: {game_states[game_state_idx].score[0]:>2}")
        score_removed = text_render(f"Changed: {game_states[game_state_idx].score[1]:>3}")
        
        screen.blit(board_name, (SCREEN_WIDTH/2 - board_name.get_width()/2, CELL_SIZE/2 - board_name.get_height()/2))
        screen.blit(solver_text, (CELL_SIZE/2, CELL_SIZE+CELL_SIZE/2 - solver_text.get_height()/2))
        screen.blit(solver_step, (SCREEN_WIDTH - solver_step.get_width() - CELL_SIZE/2, CELL_SIZE+CELL_SIZE/2 - solver_step.get_height()/2))
        
        screen.blit(text_render("Numbers"), (CELL_SIZE/2, SCREEN_HEIGHT - 55-35))
        screen.blit(score_placed, (CELL_SIZE/2, SCREEN_HEIGHT - 55))
        screen.blit(text_render("Candidates"), (SCREEN_WIDTH - score_removed.get_width() - CELL_SIZE/2, SCREEN_HEIGHT - 55-35))
        screen.blit(score_removed, (SCREEN_WIDTH - score_removed.get_width() - CELL_SIZE/2, SCREEN_HEIGHT - 55))
        
        pygame.display.flip()
    pygame.quit()