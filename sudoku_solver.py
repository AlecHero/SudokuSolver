from sudoku_boards import *
from itertools import combinations
import numpy as np

GAME_N = 3
GAME_NUM = GAME_N**2
NUMBERS = range(GAME_NUM)
BOARD_SHAPE = (GAME_NUM, GAME_NUM)
UNIT_TYPES = ["row", "col", "box"]
HELPER_NAMING_DICT = {1: "Singles", 2: "Pairs", 3: "Triples", 4: "Quads"}
UNIT_IDX = np.repeat(np.arange(GAME_NUM),GAME_NUM).reshape(GAME_NUM,GAME_NUM)

def swap_unit(board, unit_type): # works as conversion from and to
    board = np.asarray(board)
    if unit_type=="row": return board
    if unit_type=="col": return board.swapaxes(-2,-1)
    if unit_type=="box" and len(board.shape) == 2: return np.concatenate([np.concatenate(board.reshape(3,3,3,3)[i], 1) for i in range(0,3)])
    if unit_type=="box" and len(board.shape) == 3: return np.asarray([swap_unit(i, "box") for i in board])
    raise ValueError("Invalid unit type")

def get_candidates(board: np.array) -> np.array:
    cands = []
    for n in range(1,10):
        mask_unit = (board == 0).astype(int)
        for unit_type in UNIT_TYPES:
            mask_unit *= swap_unit((np.ones_like(board)*(swap_unit(board, unit_type) != n).all(1)).T, unit_type)
        cands.append(mask_unit)
    return np.asarray(cands)

def where_sets(board, N):
    N_mask = (board <= N) * board.astype(bool)
    N_mask *= (N_mask.sum(1) >= N)[:,None]
    return np.where(N_mask)
def argwhere_sets(board, N):
    return np.transpose(where_sets(board, N))
def into(board, r, c): return board[:, r[:,None], c[:,None]].T.squeeze()
def comb(arr, N): return np.asarray(list(combinations(range(len(arr)), N)))

def bool_sum(board): return board.astype(bool).sum()

class GameState:
    def __init__(self, board = None, candidates = None, solver_name = "Initial", score = None):
        def sudokify(board_string):
            return [[int(j) for j in i.strip().split(" ")] for i in board_string[1:-1].replace("_", "0").replace("|"," ").split("\n")]
        
        if isinstance(board, str): self.board = np.array(sudokify(board))
        else: self.board = board
        
        if candidates is None: self.candidates = get_candidates(self.board)
        else: self.candidates = candidates
        
        if solver_name == "Initial": self.score = [bool_sum(self.board), bool_sum(self.candidates)]
        else: self.score = [bool_sum(self.board), bool_sum(self.candidates)]
        
        self.solver_name = solver_name

    def __str__(self):
        def board_stringer(board):
            stringer = "┌───────┬───────┬───────┐\n"
            for i, row in enumerate(board):
                if i%3 == 0 and i!=0: stringer += ("├───────┼───────┼───────┤\n")
                stringer += (
                    f'│ {str(row[0:3]).replace("0", " ").replace("[","").replace("]","")} ' +
                    f'│ {str(row[3:6]).replace("0", " ").replace("[","").replace("]","")} ' +
                    f'│ {str(row[6:9]).replace("0", " ").replace("[","").replace("]","")} │\n'
                    )
            stringer += ("└───────┴───────┴───────┘")
            return stringer
        
        return board_stringer(self.board)

    def as_string(self):
        return str(self.board).replace("\n ", "\n").replace("0", "_").replace("[[", "|").replace("[", "|").replace(" ", "|").replace("]]","]").replace("]", "|")
    
    def __iter__(self):
        return iter([self.board, self.candidates])
    
    def __eq__(self, other):
        return np.all(self.board == other.board) and np.all(self.candidates == other.candidates)
    
    def __copy__(self):
        return GameState(self.board.copy(), self.candidates.copy(), self.solver_name)

    def copy(self):
        return self.__copy__()

    def display(self):
        from sudoku_game import SudokuGame
        SudokuGame(self)
        
    def compare(self, other):
        from sudoku_game import SudokuGame
        SudokuGame(self, compare=other)


def SudokuLoop(board: np.array, EXECUTORS: list) -> list:
    gs = [GameState(board)]
    while True:
        older_gs = gs[-1].copy()
                
        for executor in EXECUTORS:
            old_gs = gs[-1].copy()
            new_gs = executor(gs[-1].copy())
            if new_gs == old_gs: continue
            else: gs.append(new_gs); break

        newer_gs = gs[-1].copy()
        if newer_gs == older_gs: break
    return gs


### SOLVERS ###



def naked_sets(gs: GameState, N: int) -> GameState:
    board, candidates = gs
    if N == 1:
        sets_into = into(candidates, *where_sets(candidates.sum(0), N))
        board[where_sets(candidates.sum(0), 1)] = np.where(sets_into)[-1]+1
        candidates *= get_candidates(board)
        
    elif N > 1:
        for unit_type in UNIT_TYPES:
            unit_candidates = swap_unit(candidates, unit_type).copy()
            N_row, N_col = where_sets(unit_candidates.sum(0), N)
            N_into = into(unit_candidates, N_row, N_col)

            for row in NUMBERS:
                combs = comb(N_into[N_row == row], N)
                if combs.size == 0: continue # print("No Combinations")

                valid_combs = combs[(N_into[N_row == row][combs].sum(1).astype(bool).sum(1) <= N)]
                if valid_combs.size == 0: continue # print("No Valid Combinations")
                    
                for valid_comb in valid_combs:
                    N_nums = np.where(N_into[N_row == row][valid_comb.squeeze()].sum(0))[0]
                    mask_col = np.isin(np.arange(9), N_col[N_row == row][valid_comb.squeeze()])
                    unit_candidates[N_nums, row] *= mask_col
            candidates = swap_unit(unit_candidates, unit_type)
        
    return GameState(board, candidates, f"Naked {HELPER_NAMING_DICT[N]}")

def hidden_sets(gs: GameState, N: int) -> GameState:
    board, candidates = gs.copy()
    
    for unit_type in UNIT_TYPES:
        unit_board = swap_unit(board, unit_type)
        unit_candidates = swap_unit(candidates, unit_type)
        N_row, N_num = where_sets(unit_candidates.sum(2).T, N)
        
        if N == 1:
            N_col = np.where(into(unit_candidates.T, N_row, N_num))[-1]
            unit_board[N_row, N_col] = N_num+1
            board = swap_unit(unit_board, unit_type)
            candidates *= get_candidates(board)
    
        elif N > 1:
            for row in NUMBERS:
                combs = comb(N_num[N_row == row], N)
                if combs.size == 0: continue # print("No Combinations")
                
                valid_combs = combs[unit_candidates[N_num[N_row == row][combs], row].sum(1).astype(bool).sum(1) <= N]
                if valid_combs.size == 0: continue # print("No Valid Combinations")
                
                for valid_comb in valid_combs:
                    row_col = np.where(unit_candidates[N_num[N_row == row][valid_comb.squeeze()], row].sum(0))[0]
                    mask_num = np.isin(np.arange(9), N_num[N_row == row][valid_combs.squeeze()])[:,None]
                    unit_candidates[:, row, row_col] *= mask_num
            candidates = swap_unit(unit_candidates, unit_type)

    return GameState(board, candidates, f"Hidden {HELPER_NAMING_DICT[N]}")

def intersection_removal(gs: GameState) -> GameState:
    board, candidates = gs.copy()
    
    for unit_type1, unit_type2 in [["box", "row"], ["box", "col"], ["row", "box"], ["col", "box"]]:
        for k in range(9):
            for i in range(9):
                for j in range(9):
                    row_unit     = (swap_unit(UNIT_IDX, unit_type1) == i) * (swap_unit(UNIT_IDX, unit_type2) == j)
                    row_unit_not = (swap_unit(UNIT_IDX, unit_type1) == i) * (swap_unit(UNIT_IDX, unit_type2) != j)
                    
                    if (candidates[k][row_unit].any()) and (not candidates[k][row_unit_not].any()):
                        candidates[k] *= ~((swap_unit(UNIT_IDX, unit_type1) != i) * (swap_unit(UNIT_IDX, unit_type2) == j))

    return GameState(board, candidates, "Intersection Removal")

naked_singles = lambda gs: naked_sets(gs, 1)
naked_pairs = lambda gs: naked_sets(gs, 2)
naked_triples = lambda gs: naked_sets(gs, 3)
naked_quads = lambda gs: naked_sets(gs, 4)

hidden_singles = lambda gs: hidden_sets(gs, 1)
hidden_pairs = lambda gs: hidden_sets(gs, 2)
hidden_triples = lambda gs: hidden_sets(gs, 3)
hidden_quads = lambda gs: hidden_sets(gs, 4)



### BOARD IMPORTING ###

def html_to_sudoku(html_sudoku):
    # https://www.sudokuwiki.org/sudoku.htm
    from bs4 import BeautifulSoup
    bs_html = BeautifulSoup(html_sudoku)
    board = np.asarray([[int(bs_html.find("td", id=f"a{i}{j}").text.replace("123456789", "0")) for i in range(9)] for j in range(9)]).T
    print(GameState(board).as_string() )

def sudoku_to_import(board): return "".join([str(i) for i in list(board.reshape(-1).astype(int))]) # for importing on sudokuwiki.org