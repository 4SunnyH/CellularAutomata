"""2d_automaton.py
This file is part of He Sun's final paper for PHY196 at University of Toronto.
Author: He Sun
"""

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, Normalize
import numpy as np

dx = [0, 1, 0, -1, 1, 1, -1, -1]
dy = [1, 0, -1, 0, 1, -1, 1, -1]
# default order of 8 neighbours
# note that first 4 stand for 'immediate' neighbours with a shared edge

class Rule:
    def __init__(self, current_state: int, neighbour_states: list[int], target_state: int):
        # neighbour_states has a length of 8, in the order described in dx and dy
        # in states, -1 means no change / any state
        # target state cannot be -1 (would make the rule meaningless)
        self.current_state = current_state
        self.neighbour_states = neighbour_states.copy()
        self.target_state = target_state


class CellularAutomaton_2D:
    def __init__(self, grid: list[list[int]]):
        # Assume grid is a square
        self.size = len(grid)
        self.grid = grid
        self.rules: list[Rule] = []

    def normalize_position(self, pos: int) -> int:
        # Convert the apparent location (-size/2 to size/2) to grid location (0 to size-1)
        return pos + self.size // 2
    def normalize_position(self, x: int, y: int) -> tuple[int, int]:
        return (self.normalize_position(x), self.normalize_position(y))
    
    def is_valid_position(self, x: int, y: int) -> bool:
        return 0 <= x < self.size and 0 <= y < self.size
    
    def get_value(self, x: int, y: int) -> int:
        # Returns grid[x][y], or 0 if out of range
        if not self.is_valid_position(x, y):
            return 0
        return self.grid[x][y]
    
    def add_rule(self, rule: Rule) -> None:
        self.rules.append(rule)
    
    def check_rule(self, x: int, y: int, rule: Rule) -> bool:
        # returns whether the rule matches
        if rule.current_state != -1 and rule.current_state != self.grid[x][y]:
            # current state not matched
            return False
        for k in range(8):
            nx = x + dx[k]
            ny = y + dy[k]
            value = self.get_value(nx, ny)
            if rule.neighbour_states[k] != -1 and rule.neighbour_states[k] != value:
                # neighbour state not matched
                return False
        # all neighbour states match
        return True

    def update(self) -> None:
        new_grid = [[0] * self.size for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                new_grid[i][j] = self.get_value(i, j)
                for rule in self.rules:
                    if self.check_rule(i, j, rule):
                        # Assume rules do not conflict
                        new_grid[i][j] = rule.target_state
        self.grid = new_grid

    def show(self, axis, index) -> None:
        grid = np.array(self.grid[::-1]) # Reverse the rows
        cmap = ListedColormap(['white', 'black'])
        norm = Normalize(vmin=0, vmax=1)
        axis.pcolormesh(grid, edgecolors='k', linewidth=1, cmap=cmap, norm=norm)
        axis.set_title(index)
        axis.set_aspect('equal')
        axis.axis('off')


def show_fig_1():
    grid = [[0] * 5 for _ in range(5)]
    grid[1][2] = 1
    grid[2][2] = 1
    automaton = CellularAutomaton_2D(grid)
    for i in range(4):
        new_list = [-1] * 8
        new_list[i] = 1
        automaton.add_rule(Rule(0, new_list, 1)) # spread from adjacent cells to an empty location
    automaton.add_rule(Rule(1, [-1]*8, 0)) # cells die every tick
    
    fig, axes = plt.subplots(1, 4)
    automaton.show(axes[0], 0)
    for i in range(1, 4):
        automaton.update()
        automaton.show(axes[i], i)
    plt.savefig('plot_1.png', dpi=300)
    plt.show()


if __name__ == "__main__":
    show_fig_1()
