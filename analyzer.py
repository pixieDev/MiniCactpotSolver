# -*- coding: UTF-8 -*-

"""
Mini-Cactpot Game probabalistic solver - functions for Monte Carlo tests

default number of iterations is 300
"""
from cactpot import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from copy import deepcopy


def _monte_carlo_test(game_board, n_iters=300):
    sim_payouts = np.ndarray(shape=(n_iters, 8))
    n = 0
    while n != n_iters:
        monte_board = random_fill(game_board)
        solutions = board_solver(monte_board)
        payouts = find_payouts(solutions)
        for p, pay_tup in enumerate(payouts):
            sim_payouts[n, p] = pay_tup[-1]
        n += 1

    return sim_payouts


def count_permutation_payouts(permutation_array):
    line_names = ['Line %d' % (n+1) for n in range(permutation_array.shape[1])]
    payout_dict = create_payout_dict()
    payout_names = sorted(np.unique([v for k, v in payout_dict.items()]))
    payout_counts = {}
    for line in range(permutation_array.shape[1]):
        counts = []
        for payout_name in payout_names:
            count = 0
            for payout_possible in permutation_array[:, line]:
                if payout_possible == payout_name:
                    count += 1
            counts.append((payout_name, count))
        payout_counts[line_names[line]] = counts

    return payout_counts


def _extract_payout_names(payout_counts):
    # Resuable function for extracting names of payouts
    temp_line = list(payout_counts)[0]
    temp_y = payout_counts[temp_line]
    return [n[0] for n in temp_y]


def plot_counts(payout_counts):
    def _plot_bar(y, payout_names):
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(
            x=np.arange(len(payout_names)),
            height=y,
            tick_label=payout_names,
        )
        ax.tick_params(labelrotation=90, axis='x')
        ax.set_xlabel('MGP Payouts')
        ax.set_ylabel('Permutation frequency')

    payout_names = _extract_payout_names(payout_counts)
    for line_name in payout_counts:
        y = payout_counts[line_name]
        _plot_bar(y, payout_names)
        plt.show()
        break


def simple_stats(payout_counts):
    stats_to_calc = [
        'Average payout',
        'Most likely payout',
        'Most likely chance',
        'Highest payout',
        'Highest payout chance',
    ]
    payout_names = _extract_payout_names(payout_counts)
    results = pd.DataFrame(index=list(payout_counts), columns=stats_to_calc)
    for line_name in payout_counts:
        y = payout_counts[line_name]
        total = sum(b[1] for b in y)
        nonzero_avg = sum(b[0] *b[1] for b in y)/total
        results['Average payout'].loc[line_name] = nonzero_avg

        probabilities = [b[1]/total for b in y]
        prob_first = payout_names[np.argmax(probabilities)]
        results['Most likely payout'].loc[line_name] = prob_first
        results['Most likely chance'].loc[line_name] = np.max(probabilities)

        highest_pay = np.max([b[0] for b in y if b[1]> 1])
        highest_idx = [i for i,j in enumerate(y) if j[0]==highest_pay][-1]
        results['Highest payout'].loc[line_name] = highest_pay
        results['Highest payout chance'].loc[line_name] = probabilities[highest_idx]
    return results


def _analyzer_testing():
    seed_board = Board(by=4)
    true_board = random_fill(seed_board, seed=4)
    """
    # True board solution for seed=4
    2 8 7
    6 4 9
    1 3 5
    """
    # Simulating actual play
    game_board = Board(by=4)
    game_board.fill(ax=2)
    game_board.fill(cy=9)
    game_board.fill(bz=3)

    test_results = _monte_carlo_test(game_board)
    payout_counts = count_permutation_payouts(test_results)
    simple_stats(payout_counts)

if __name__ == "__main__":
    # debugging
    _analyzer_testing()
