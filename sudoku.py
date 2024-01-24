from argparse import ArgumentParser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from copy import deepcopy
from os import devnull

top_left_complements = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2), (2, 1)]
top_mid_complements = [(1, 0), (2, 0), (0, -1), (0, 1), (1, 1), (1, -1), (2, -1), (2, 1)]
top_right_complements = [(1, 0), (2, 0), (0, -1), (0, -2), (1, -1), (1, -2), (2, -2), (2, -1)]
mid_left_complements = [(1, 0), (-1, 0), (0, 1), (0, 2), (1, 1), (1, 2), (-1, 2), (-1, 1)]
mid_mid_complements = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, -1), (-1, 1)]
mid_right_complements = [(-1, 0), (1, 0), (0, -1), (0, -2), (1, -1), (1, -2), (-1, -2), (-1, -1)]
bottom_left_complements = [(-1, 0), (-2, 0), (0, 1), (0, 2), (-1, 1), (-1, 2), (-2, 2), (-2, 1)]
bottom_mid_complements = [(-1, 0), (-2, 0), (0, 1), (0, -1), (-1, 1), (-1, -1), (-2, -1), (-2, 1)]
bottom_right_complements = [(-1, 0), (-2, 0), (0, -1), (0, -2), (-1, -1), (-1, -2), (-2, -2), (-2, -1)]
quadrant_beginning_corners = [(0, 0), (0, 3), (0, 6), (3, 0), (3, 3), (3, 6), (6, 0), (6, 3), (6, 6)]


def print_status(grid):
    grid_string = "\n\n  | 0  1  2 | 3  4  5 | 6  7  8 \n   ------------------------------"
    for row_idx, row in enumerate(grid):
        grid_string += "\n"
        grid_string += "%d |" % row_idx
        for col_idx, element in enumerate(row):
            grid_string += " %s " % str(element)
            if (col_idx + 1) % 3 == 0:
                grid_string += "|"
            if col_idx == 8:
                grid_string += " %d" % row_idx
        if (row_idx + 1) % 3 == 0:
            grid_string += "\n  -------------------------------"
    print(grid_string)


def already_in_quadrant(grid, i, j, offset_tuples, val):
    for offset_tuple in offset_tuples:
        if isinstance(grid[i + offset_tuple[0]][j + offset_tuple[1]], int):
            if grid[i + offset_tuple[0]][j + offset_tuple[1]] == val:
                return True
    return False


def could_go(grid, i, j, val):
    if isinstance(grid[i][j], int):
        return False
    for idx in range(9):
        if grid[i][idx] == val:
            return False
    for idx in range(9):
        if grid[idx][j] == val:
            return False
    if i % 3 == 0:
        if j % 3 == 0:
            if already_in_quadrant(grid, i, j, top_left_complements, val):
                return False
        elif j % 3 == 1:
            if already_in_quadrant(grid, i, j, top_mid_complements, val):
                return False
        elif j % 3 == 2:
            if already_in_quadrant(grid, i, j, top_right_complements, val):
                return False
    elif i % 3 == 1:
        if j % 3 == 0:
            if already_in_quadrant(grid, i, j, mid_left_complements, val):
                return False
        elif j % 3 == 1:
            if already_in_quadrant(grid, i, j, mid_mid_complements, val):
                return False
        elif j % 3 == 2:
            if already_in_quadrant(grid, i, j, mid_right_complements, val):
                return False
    elif i % 3 == 2:
        if j % 3 == 0:
            if already_in_quadrant(grid, i, j, bottom_left_complements, val):
                return False
        elif j % 3 == 1:
            if already_in_quadrant(grid, i, j, bottom_mid_complements, val):
                return False
        elif j % 3 == 2:
            if already_in_quadrant(grid, i, j, bottom_right_complements, val):
                return False
    return True


def is_good_board(grid):
    for row in grid:
        haves = []
        for element in row:
            if isinstance(element, int):
                if element in haves:
                    return False
                haves.append(element)
    for column in range(9):
        haves = []
        for row in range(9):
            element = grid[row][column]
            if isinstance(element, int):
                if element in haves:
                    return False
                haves.append(element)
    return True


def check_for_victory(grid):
    return sum(sum(1 for cell in row if isinstance(cell, int)) for row in grid) == 81 and is_good_board(grid)


def fill_website(grid, driver):
    print_status(grid)
    driver.find_element("id", "f00").send_keys(Keys.BACKSPACE)
    for j in range(9):
        for i in range(9):
            action_chain = ActionChains(driver)
            action_chain.send_keys(str(grid[j][i]))
            action_chain.perform()
            action_chain.send_keys(Keys.TAB)
            action_chain.perform()


def fill_obvious_rows(grid):
    for j in range(9):
        needed_digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for digit in grid[j]:
            if isinstance(digit, int):
                try:
                    needed_digits.remove(digit)
                except ValueError:
                    pass
        if len(needed_digits) == 1:
            for i in range(len(grid[j])):
                if isinstance(grid[j][i], str):
                    grid[j][i] = needed_digits[0]
                    print_status(grid)


def fill_obvious_columns(grid):
    for j in range(9):
        needed_digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for column_idx in range(9):
            digit = grid[column_idx][j]
            if isinstance(digit, int):
                try:
                    needed_digits.remove(digit)
                except ValueError:
                    pass
        if len(needed_digits) == 1:
            for column_idx in range(9):
                if isinstance(grid[column_idx][j], str):
                    grid[column_idx][j] = needed_digits[0]
                    print_status(grid)


def fill_obvious_quadrants(grid):
    for horizontal_offset in range(3):
        for vertical_offset in range(3):
            needed_digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for i in range(3):
                for column_idx in range(3):
                    digit = grid[column_idx + (horizontal_offset * 3)][i + (vertical_offset * 3)]
                    if isinstance(digit, int):
                        try:
                            needed_digits.remove(digit)
                        except ValueError:
                            pass
            if len(needed_digits) == 1:
                for i in range(3):
                    for column_idx in range(3):
                        if isinstance(grid[column_idx + (horizontal_offset * 3)][i + (vertical_offset * 3)], str):
                            grid[column_idx + (horizontal_offset * 3)][i + (vertical_offset * 3)] = needed_digits[0]
                            print_status(grid)


def quadrant_brute(grid, i, j, offset_tuples, possible_values):
    for offset_tuple in offset_tuples:
        if isinstance(grid[i + offset_tuple[0]][j + offset_tuple[1]], int):
            try:
                possible_values.remove(grid[i + offset_tuple[0]][j + offset_tuple[1]])
            except ValueError:
                pass
    return possible_values


def elimination_brute(grid):
    for i in range(9):
        for j in range(9):
            cell_under_consideration = grid[i][j]
            if isinstance(cell_under_consideration, str):
                possible_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                for line_val in grid[i]:
                    if isinstance(line_val, int):
                        if line_val in possible_values:
                            possible_values.remove(line_val)
                for column_idx in range(9):
                    if isinstance(grid[i][column_idx], int):
                        if grid[i][column_idx] in possible_values:
                            possible_values.remove(grid[i][column_idx])
                if i % 3 == 0:
                    if j % 3 == 0:
                        possible_values = quadrant_brute(grid, i, j, top_left_complements, possible_values)
                    elif j % 3 == 1:
                        possible_values = quadrant_brute(grid, i, j, top_mid_complements, possible_values)
                    elif j % 3 == 2:
                        possible_values = quadrant_brute(grid, i, j, top_right_complements, possible_values)
                elif i % 3 == 1:
                    if j % 3 == 0:
                        possible_values = quadrant_brute(grid, i, j, mid_left_complements, possible_values)
                    elif j % 3 == 1:
                        possible_values = quadrant_brute(grid, i, j, mid_mid_complements, possible_values)
                    elif j % 3 == 2:
                        possible_values = quadrant_brute(grid, i, j, mid_right_complements, possible_values)
                elif i % 3 == 2:
                    if j % 3 == 0:
                        possible_values = quadrant_brute(grid, i, j, bottom_left_complements, possible_values)
                    elif j % 3 == 1:
                        possible_values = quadrant_brute(grid, i, j, bottom_mid_complements, possible_values)
                    elif j % 3 == 2:
                        possible_values = quadrant_brute(grid, i, j, bottom_right_complements, possible_values)
                if len(possible_values) == 1:
                    grid[i][j] = possible_values[0]
                    print_status(grid)
                    return


def row_filler(grid):
    for row_num in range(9):
        this_row = grid[row_num]
        possible_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for val in this_row:
            if isinstance(val, int):
                try:
                    possible_values.remove(val)
                except ValueError:
                    pass
        # Now possible_values only has what is left to be filled on this row
        if len(possible_values) > 1:
            for digit_attempt in possible_values:
                num_of_places_digit_could_go = 0
                for idx in range(9):
                    if isinstance(grid[row_num][idx], str):
                        if could_go(grid, row_num, idx, digit_attempt):
                            num_of_places_digit_could_go += 1
                if num_of_places_digit_could_go == 1:
                    for idx in range(9):
                        if isinstance(grid[row_num][idx], str):
                            if could_go(grid, row_num, idx, digit_attempt):
                                grid[row_num][idx] = digit_attempt
                                print_status(grid)


def column_filler(grid):
    for column_num in range(9):
        this_column = []
        for row_num in range(9):
            this_column.append(grid[row_num][column_num])

        possible_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for val in this_column:
            if isinstance(val, int):
                try:
                    possible_values.remove(val)
                except ValueError:
                    pass
        # Now possible_values only has what is left to be filled on this column
        if len(possible_values) > 1:
            for digit_attempt in possible_values:
                num_of_places_digit_could_go = 0
                for idx in range(9):
                    if isinstance(grid[idx][column_num], str):
                        if could_go(grid, idx, column_num, digit_attempt):
                            num_of_places_digit_could_go += 1
                if num_of_places_digit_could_go == 1:
                    for idx in range(9):
                        if isinstance(grid[row_num][idx], str):
                            if could_go(grid, idx, column_num, digit_attempt):
                                grid[idx][column_num] = digit_attempt
                                print_status(grid)


def already_in_quadrant(grid, i, j, offset_tuples, val):
    for offset_tuple in offset_tuples:
        if isinstance(grid[i + offset_tuple[0]][j + offset_tuple[1]], int):
            if grid[i + offset_tuple[0]][j + offset_tuple[1]] == val:
                return True
    return False


def do_the_obvious(grid):
    fill_obvious_rows(grid)
    fill_obvious_columns(grid)
    fill_obvious_quadrants(grid)
    elimination_brute(grid)
    row_filler(grid)
    column_filler(grid)


def recursive_solve(original_grid, driver):
    grid = deepcopy(original_grid)
    if check_for_victory(grid):
        fill_website(grid, driver)
        return True
    if not is_good_board(grid):
        return False
    remaining_possibilities = []
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            could_go_here = []
            for i in range(1, 10):
                if could_go(grid, row_idx, col_idx, i):
                    could_go_here.append(i)
            remaining_possibilities.append(could_go_here)
    for possibility_idx, possibility in enumerate(remaining_possibilities):
        if len(possibility) == 1:
            grid[int(possibility_idx / 9)][possibility_idx % 9] = possibility[0]
    do_the_obvious(grid)
    if check_for_victory(grid):
        fill_website(grid, driver)
        return True
    if not is_good_board(grid):
        return False
    for guess_minimizer in range(2, 9):
        for possibility_idx, possibility in enumerate(remaining_possibilities):
            if len(possibility) == guess_minimizer:
                for poss in possibility:
                    grid[int(possibility_idx / 9)][possibility_idx % 9] = poss
                    if recursive_solve(grid, driver):
                        return True

    return False


def main():
    parser = ArgumentParser()
    parser.add_argument("-d", "--difficulty", type=int, help="Difficulty (1-4, 1=Easy, 4=Evil); default 4", default=4)
    args = parser.parse_args()

    if args.difficulty < 1 or args.difficulty > 4:
        args.difficulty = 4

    # First, start a browser up and load WebSudoku
    service = Service(
        service_log_path=devnull
    )
    driver = webdriver.Firefox(service=service)
    driver.implicitly_wait(2)  # wait a couple of seconds
    driver.get(f"https://www.websudoku.com/?level={args.difficulty}")

    # Focus attention on the actual puzzle/grid
    frame = driver.find_element("xpath", "//frame[contains(@src,'websudoku.com/')]")
    driver.switch_to.frame(frame)

    # Load the initial grid state
    puzzle = []
    for i in range(9):
        puzzle.append([])
        for j in range(9):
            this_id = "f%s%s" % (j, i)
            this_val = (
                int(driver.find_element("id", this_id).get_attribute("value"))
                if len(driver.find_element("id", this_id).get_attribute("value")) > 0
                else " "
            )
            puzzle[i].append(this_val)

    # Kick things off
    recursive_solve(puzzle, driver)

    # Now wait for user input before shutting down the browser
    input("Press enter to exit and close browser window.")
    try:
        # Wrap this in a try-block in case the user exited the browser manually already.
        driver.close()
    except:
        return


if __name__ == "__main__":
    main()
