"""1d_automaton.py
This file is part of He Sun's final paper for PHY196 at University of Toronto.
"""

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, Normalize
import numpy as np

class CellularAutomaton_1D:
    def __init__(self, array: list[int], rules: list[int]):
        self.size = len(array)
        self.array = array
        self.rules = rules

    def update(self) -> None:
        new_array = [0] * self.size
        for i in range(self.size):
            # if out of bounds, assume that the 'outside' bit to be the same as the boundary
            prev_value = 1 - self.array[i - 1] if i > 0 else 1 - self.array[i]
            curr_value = 1 - self.array[i]
            next_value = 1 - self.array[i + 1] if i < self.size - 1 else 1 - self.array[i]
            new_array[i] = self.rules[prev_value * 4 + curr_value * 2 + next_value]
        self.array = new_array

    def show(self, max_steps: int, savefile: str="") -> None:
        grid = []
        grid.append(self.array)
        for _ in range(max_steps):
            self.update()
            grid.append(self.array)

        grid = np.array(grid[::-1])
        cmap = ListedColormap(['white', 'black'])
        norm = Normalize(vmin=0, vmax=1)
        plt.figure(figsize=(6, 4), dpi=300)
        plt.pcolormesh(grid, edgecolors='k', linewidth=0.5, cmap=cmap, norm=norm)
        plt.axis('off')
        if savefile != "":
            plt.savefig(savefile, bbox_inches='tight', pad_inches=0.2)
        plt.show()


def runElementaryCA(rule: int, maxstep: int, size: int=1, initial_state: list[int]=[], savefile=""):
    if initial_state != []:
        array = initial_state
    else:
        array = [0] * (size//2) + [1] + [0] * (size//2)
    rules = []
    current_rule = 2 ** 7
    while current_rule > 0:
        if rule >= current_rule:
            rules.append(1)
            rule -= current_rule
        else:
            rules.append(0)
        current_rule //= 2
    automaton = CellularAutomaton_1D(array, rules)
    automaton.show(maxstep, savefile=savefile)

def show_rule_110(maxstep: int, plot_num: int):
    # the graph must be larger to plot thousands of rows & columns
    automaton = CellularAutomaton_1D([0] * maxstep + [0,1] + [0], [0,1,1,0,1,1,1,0])
    grid = []
    grid.append(automaton.array)
    for _ in range(maxstep):
        automaton.update()
        grid.append(automaton.array)

    grid = np.array(grid[::-1])
    cmap = ListedColormap(['white', 'black'])
    norm = Normalize(vmin=0, vmax=1)
    plt.figure(figsize=(40, 40), dpi=800)
    plt.pcolormesh(grid, edgecolors='k', linewidth=0.1, cmap=cmap, norm=norm)
    plt.axis('off')
    plt.savefig(f"plot_{plot_num}.png", bbox_inches='tight', pad_inches=0.2)


if __name__ == "__main__":
    # Introduction
    runElementaryCA(2, 11, size=21, savefile="plot_3.png")

    # Class 1
    runElementaryCA(0, 3, size=5, savefile="plot_4.png")
    runElementaryCA(32, 5, size=5, savefile="plot_5.png")
    runElementaryCA(251, 7, size=11, savefile="plot_6.png")

    # Class 2
    runElementaryCA(6, 15, size=31, savefile="plot_7.png")
    runElementaryCA(37, 15, size=31, savefile="plot_8.png")
    runElementaryCA(218, 31, size=63, savefile="plot_9.png")

    # Class 3
    runElementaryCA(30, 63, size=127, savefile="plot_10.png")
    runElementaryCA(89, 63, size=127, savefile="plot_11.png")

    # Class 4
    runElementaryCA(110, 128, initial_state=[0]*128+[1]+[0]*2, savefile="plot_12.png")
    show_rule_110(2000, 13)
