# -*- coding: UTF-8 -*-

"""
Mini-Cactpot Game probabalistic solver - board generation functions

Assign the values 1-9 to a 3x3 grid

# 3x3 variable grid
        a   b   c
    x   ax  bx  cx
    y   ay  by  cy
    z   az  bz  cz

# 8 possible solutions
ax + bx + cx
ay + by + cy
az + bz + cz
ax + ay + az
bx + by + bz
cx + cy + cz
ax + by + cz
cx + by + az

# Use probabalistic methods to maximize payout
# See "payout.txt" for associated payouts associated with each sum of values
"""
import random

class Board:
    def __init__(self, **kwargs):
        # defaults
        board = dict(
            ax=0,
            bx=0,
            cx=0,
            ay=0,
            by=0,
            cy=0,
            az=0,
            bz=0,
            cz=0
        )

        # these lines allow the board to be filled upon creation
        attr = list(board.keys())
        board.update(kwargs)
        self.__dict__.update((k, v) for k, v in board.items() if k in attr)

    def fill(self, **kwargs):
        # function for filling in the board one at a time
        for k, v in kwargs.items():
            setattr(self, k, v)

    def fill_multiple(self, fill_dict):
        # function for filling in multiple spots of the board at once
        self.__dict__.update((k, v) for k, v in fill_dict.items())

    def reset(self):
        # function for resetting the board to null values
        attr = self.__dict__.keys()
        self.__dict__.update((k, 0) for k in attr)


def random_fill(board=None, return_copy=True, seed=None):
     # seed is for debugging, leave at None
    if board is None: # for debugging/testing, please use a filled board
        board = Board()  # by=4)
    attributes = vars(board)

    # check which spaces have been filled, grab values
    spaces_filled, spaces_empty = [], []
    for k, v in attributes.items():
        if v != 0:
            spaces_filled.append((k, v))
        else:
            spaces_empty.append((k, v))

    # instance board to return if copying
    if return_copy is True:
        return_board = Board()
    else:
        return_board = board
    return_board.fill_multiple(dict(spaces_filled))

    # get list of possible values to fill in the board with
    values_possible = list(range(1, 10))
    for tup in spaces_filled:
        values_possible.remove(tup[-1])

    # fill in remainin spaces randomly
    random.Random(seed).shuffle(values_possible)
    spaces_to_fill = []
    for i, tup in enumerate(spaces_empty):
        spaces_to_fill.append((tup[0], values_possible[i]))
    return_board.fill_multiple(dict(spaces_to_fill))

    return return_board


def create_solution_grid():
    """
    # Function for creating list of possible solutions, used in other places
    ax + bx + cx
    ay + by + cy
    az + bz + cz
    ax + ay + az
    bx + by + bz
    cx + cy + cz
    ax + by + cz
    cx + by + az
    """
    solution_grid = [
        ('ax', 'bx', 'cx'),
        ('ay', 'by', 'cy'),
        ('az', 'bz', 'cz'),
        ('ax', 'ay', 'az'),
        ('bx', 'by', 'bz'),
        ('cx', 'cy', 'cz'),
        ('ax', 'by', 'cz'),
        ('cx', 'by', 'az')
    ]
    return solution_grid


def board_solver(board):
    checker = 0
    for _, v in vars(board).items():
        checker += v
    if checker != 45:
        raise ValueError("Board did not fill correctly")

    solution_grid = create_solution_grid()
    solutions = []
    for sol_tuple in solution_grid:
        summator = []
        for position in sol_tuple:
            summator.append(vars(board)[position])
        value = sum(summator)
        solutions.append((sol_tuple, value))

    return solutions


def create_payout_dict():
    payout_dict = {}
    with open('payout.txt', 'r') as file:
        for line in file:
            (key, val) = line.split()
            payout_dict[int(key)] = int(val)
    return payout_dict


def find_payouts(solutions):
    payout_reference = create_payout_dict()
    payouts = []
    for sol_tuple in solutions:
        sol = sol_tuple[0]
        val = sol_tuple[-1]
        payouts.append((sol, payout_reference[val]))
    return payouts


if __name__ == "__main__":
    # debugging
    from pprint import pprint
    test_board = Board(by=4)
    pprint(vars(test_board))
    filled_board = random_fill(test_board, seed=4)
    pprint(vars(filled_board))

    payouts = board_solver(filled_board)
    print(payouts)
