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
from itertools import permutations


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

    def auto_fill(self):
        # utility function for filling in empty squares
        attr = self.__dict__.keys()
        fill_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for k in attr:  # check if board has some filled in spaces
            val = getattr(self, k)
            if val in fill_values:
                fill_values.remove(val)
        for k in attr:  # fill in blanks
            val = getattr(self, k)
            if val == 0:
                setattr(self, k, fill_values[-1])
                del fill_values[-1]


def get_possible_positions(board):
    # Note: if the board is completely filled in this function won't work
    def _check_iter(iter, filled_indices):
        nonzero_indices = [i for i,a in enumerate(filled_indices) if a != 0]
        for idx in nonzero_indices:
            if iter[idx] != filled_indices[idx]:
                return False
        return True

    grid = board.__dict__.keys()

    filled_indices = [0]*len(grid)
    for i, k in enumerate(grid): # get already-filled spaces
        val = getattr(board, k)
        if val != 0:
            filled_indices[i] = val

    board.auto_fill()
    value_array = [getattr(board, k) for k in grid]

    # get every permutation of board fill
    perms = permutations(value_array)

    # filter permutations by known spaces
    valid_perms = []
    for i in list(perms):
        if _check_iter(i, filled_indices):
            valid_perms.append(i)

    return valid_perms


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
    # from pprint import pprint
    # test_board = Board(by=4)
    # pprint(vars(test_board))
    # filled_board = random_fill(test_board, seed=4)
    # pprint(vars(filled_board))
    #
    # payouts = board_solver(filled_board)
    # print(payouts)

    b = Board(ax=4, cz=2, ay=1, bx=3)
    perms = get_possible_positions(b)
    print(len(perms))
