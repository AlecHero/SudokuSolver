# EASY:
SUDOKU_EASY = """
|5|_|2|9|_|_|_|_|4|
|_|8|_|_|_|_|5|_|_|
|_|_|_|_|_|1|9|7|_|
|_|7|5|4|1|_|_|_|_|
|1|_|_|3|_|9|_|_|8|
|_|_|_|_|7|2|6|5|_|
|_|4|8|7|_|_|_|_|_|
|_|_|3|_|_|_|_|8|_|
|2|_|_|_|_|8|3|_|7|
"""
# MEDIUM:
SUDOKU_MEDIUM = """
|_|_|3|_|_|_|_|9|_|
|6|_|_|_|8|_|_|1|5|
|2|_|_|_|_|_|_|_|7|
|_|_|6|_|7|_|3|_|4|
|_|_|_|6|_|_|_|_|8|
|_|_|2|5|_|_|_|_|_|
|_|_|9|_|_|2|_|_|_|
|8|_|_|_|_|_|_|_|_|
|4|5|1|_|_|_|_|6|_|
"""
# HARD:
SUDOKU_HARD = """
|_|_|6|_|1|_|_|_|_|
|_|2|_|_|_|9|_|_|_|
|5|7|_|_|_|_|_|_|_|
|_|_|1|2|6|_|_|4|8|
|_|_|_|_|_|3|_|7|_|
|_|_|_|_|_|_|_|_|_|
|6|_|_|_|4|1|_|8|_|
|_|_|_|3|_|_|_|_|2|
|_|3|4|_|9|_|_|_|6|
"""
# EXPERT:
SUDOKU_EXPERT = """
|8|_|5|_|_|9|3|_|4|
|2|_|_|_|_|_|_|_|_|
|_|_|_|6|_|_|_|_|9|
|_|4|_|_|_|_|_|_|_|
|9|_|3|_|_|6|8|_|_|
|_|_|_|_|1|_|_|7|_|
|_|2|_|_|_|5|_|_|_|
|5|_|4|7|_|_|_|8|_|
|_|6|_|_|_|_|4|_|_|
"""
# DIABOLICAL
SUDOKU_DIABOLICAL = """
|_|7|4|3|_|2|_|_|_|
|_|_|_|_|_|5|_|4|_|
|_|_|_|6|_|7|9|_|_|
|_|5|6|_|_|_|7|9|_|
|3|_|_|_|_|_|_|_|5|
|_|2|7|_|_|_|6|8|_|
|_|_|5|7|_|1|_|_|_|
|_|1|_|2|_|_|_|_|_|
|_|_|_|4|_|8|1|6|_|
"""

SUDOKU_DIABOLICAL2 = """
|_|_|_|7|_|4|_|_|5|
|_|2|_|_|1|_|_|7|_|
|_|_|_|_|8|_|_|_|2|
|_|9|_|_|_|6|2|5|_|
|6|_|_|_|7|_|_|_|8|
|_|5|3|2|_|_|_|1|_|
|4|_|_|_|9|_|_|_|_|
|_|3|_|_|6|_|_|9|_|
|2|_|_|4|_|7|_|_|_|
"""

#-----------------#
#  SPECIAL CASES  #

SUDOKU_NAKED_PAIR = """
|4|_|_|_|_|_|9|3|8|
|_|3|2|_|9|4|1|_|_|
|_|9|5|3|_|_|2|4|_|
|3|7|_|6|_|9|_|_|4|
|5|2|9|_|_|1|6|7|3|
|6|_|4|7|_|3|_|9|_|
|9|5|7|_|_|8|3|_|_|
|_|_|3|9|_|_|4|_|_|
|2|4|_|_|3|_|7|_|9|
"""

SUDOKU_HIDDEN_PAIR = """
|_|_|_|_|_|_|_|_|_|
|9|_|4|6|_|7|_|_|_|
|_|7|6|8|_|4|1|_|_|
|3|_|9|7|_|1|_|8|_|
|7|_|8|_|_|_|3|_|1|
|_|5|1|3|_|8|7|_|2|
|_|_|7|5|_|2|6|1|_|
|_|_|5|4|_|3|2|_|8|
|_|_|_|_|_|_|_|_|_|
"""

SUDOKU_HIDDEN_TRIPLES = """
|_|_|_|_|_|1|_|3|_|
|2|3|1|_|9|_|_|_|_|
|_|6|5|_|_|3|1|_|_|
|6|7|8|9|2|4|3|_|_|
|1|_|3|_|5|_|_|_|6|
|_|_|_|1|3|6|7|_|_|
|_|_|9|3|6|_|5|7|_|
|_|_|6|_|1|9|8|4|3|
|3|_|_|_|_|_|_|_|_|
"""

SUDOKU_INTERSECTION_REMOVAL = """
|_|1|6|_|_|7|8|_|3|
|_|9|_|8|_|_|_|_|_|
|8|7|_|_|_|1|2|6|_|
|_|4|8|_|_|_|3|_|_|
|6|5|_|_|_|9|_|8|2|
|_|3|9|_|_|_|6|5|_|
|_|6|_|9|_|_|_|2|_|
|_|8|_|_|_|2|9|3|6|
|9|2|4|6|_|_|5|1|_|
"""