# Friendly Neighborhood Sudoku Bot

## About

Very simple and minimal 9x9 sudoku solver, designed to work with [Web Sudoku](https://www.websudoku.com/) puzzles and written mostly as an exercise.

The solver employs an ad hoc algorithm which iteratively:

1) Fills in all trivially-deducible digits in every row, column, and "quadrant" (square).
2) Ranks the remaining cells by ascending number of possible digits they could contain (topmost and leftmost taking priority when necessary).
3) Recursively fills these cells with (ascending-digit) guesses until a valid solution is found.

This is basically what I found my internal thought-process/algorithm to be doing as I tried to solve sudokus by hand.

While this is considerably more efficient than a [naive brute-force backtracking algorithm](https://en.wikipedia.org/wiki/Sudoku_solving_algorithms#Backtracking), it is not as elegant or efficient as a properly-implemented [Dancing Links](https://en.wikipedia.org/wiki/Dancing_Links) / [Algorithm X](https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X) approach would be.<sup>[[1](https://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html)] [[2](https://github.com/sraaphorst/dlx_python)]</sup>

## Usage

`python3 sudoku.py`