from copy import deepcopy
from itertools import *
from functools import reduce


def get_divisors(n):
    for i in range(1, n+1):
        if n % i == 0:
            yield i, n//i


def get_rectangles(num, available, i, j):
    """
    Returns all possible rectangles as lists for this num depending on board, filled rectangles and i, j
    """
    size = len(available)
    for w, h in get_divisors(num):
        for k in range(-size+1, size):
            for m in range(-size+1, size):
                start_i = i+k
                end_i = start_i + h-1
                start_j = j+m
                end_j = start_j + w-1

                if 0 <= start_i <= i <= end_i <= size-1 and 0 <= start_j <= j <= end_j <= size-1:
                    current_available = deepcopy(available)
                    for _i in range(start_i, end_i+1):
                        for _j in range(start_j, end_j+1):
                            current_available[_i][_j] += 0 if _i == i and _j == j else 1
                    yield current_available


def count_cell_intersect(value, available, cell_rect, i, j, pos_intersect, num_rect):
    """
    Counts cells intersect with all possible rectangles
    """
    cur_cell_rect = deepcopy(cell_rect)  # count of intersects
    for rect in get_rectangles(value, available, i, j):
        can_add = True
        _i = 0
        for a, b in zip(rect, cur_cell_rect):  # we can add only if cell is free
            for _j, val in enumerate(a):
                if (a[_i] > 0 and b[_i] > 0) and _i != i and _j != j:
                    can_add = False
                    break
            _i += 1
        if can_add:
            # update count of intersects
            cur_cell_rect \
                = list(map(lambda row1, row2:
                           list(map(lambda cell1, cell2: cell1 + cell2, row1, row2)), rect, cur_cell_rect))

            # remember pos of intersect rectangle with cell
            for y, row in enumerate(rect):
                for x, val in enumerate(row):
                    if val:
                        if not pos_intersect.get(y):
                            pos_intersect[y] = {}
                        if not pos_intersect[y].get(x):
                            pos_intersect[y][x] = {}
                        if not pos_intersect[y][x].get(i):
                            pos_intersect[y][x][i] = set()
                        pos_intersect[y][x][i] = pos_intersect[y][x][i] | {j}

            num_rect[i][j].append(rect)  # remember rectangle of number
    return cur_cell_rect, pos_intersect, num_rect


def solve_helper(nums, available, pos_intersect, num_rect):
    cell_rect = [[0 for i in range(len(nums))] for j in range(len(nums[0]))]
    cell_rects = []

    for i, row in enumerate(nums):
        for j, value in enumerate(row):
            if value:
                cur_cell_rect, pos_intersect, num_rect = count_cell_intersect(value, available, cell_rect, i, j, pos_intersect, num_rect)
                cell_rects.append(cur_cell_rect)

    raise Exception('Implement sum all cell_rects together')

    min_val = min([c for row in cell_rect for c in row])

    for i, row in enumerate(cell_rect):
        for j, val in enumerate(row):
            if val == min_val:
                if pos_intersect.get(i) and pos_intersect.get(i).get(j):
                    for rect in num_rect[i][j]:
                        if rect[i][j] > 0:
                            available = fill_rectangle(rect, available)
                            solve_helper(nums, available, pos_intersect, num_rect)


def fill_rectangle(rect, available):
    return list(map(lambda row1, row2: list(map(lambda cell1, cell2: 1 if cell1 or cell2 else 0, row1, row2)), rect, available))


def solve(shik):
    available = list(map(lambda row: list(map(lambda x: 1 if x > 0 else 0, row)), shik))
    num_rect = [[[] for i in range(len(shik))] for j in range(len(shik[0]))]
    pos_intersect = {}
    solve_helper(shik, available, pos_intersect, num_rect)

if __name__ == '__main__':
    # The algorithm of solving this task

    # For each cell in the board:
    #          Count the number of rectangles touching the cell
    #      While (there is no cell that is touched by only one rectangle):
    #          For each cell:
    #              If (there is only one rectangle touching the cell):
    #              Get the corresponding rectangle and fill the board

    l = [
        # for debug
        # [2, 0],
        # [2, 0]

        # for debug
        # [0, 6, 0, 0, 0, 0, 0],
        # [0, 0, 0, 0, 0, 0, 0],
        # [0, 0, 0, 0, 0, 0, 0],
        # [0, 0, 0, 0, 0, 0, 0],
        # [0, 0, 0, 0, 0, 0, 0],
        # [0, 0, 0, 0, 0, 0, 0],
        # [0, 0, 0, 0, 0, 0, 0],

        [0, 6, 0, 0, 0, 3, 0],
        [0, 0, 0, 0, 0, 2, 0],
        [0, 2, 0, 3, 0, 2, 0],
        [2, 0, 0, 0, 5, 0, 0],
        [0, 0, 6, 0, 0, 0, 4],
        [0, 0, 0, 0, 0, 0, 7],
        [0, 3, 0, 0, 4, 0, 0],
    ]
    solve(l)