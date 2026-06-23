# -*- coding: utf-8 -*-
"""
Langton's Ant Student Template Module.
"""
import numpy as np


class LangtonsAnt:
    """
    Generalized Langton's Ant simulator on a toroidal N x N grid.

    Classical (two‑colour) behaviour:
       - White cell (0) → change to black (1), turn right ('R'), move forward.
       - Black cell (1) → change to white (0), turn left  ('L'), move forward.

    Multi‑colour rules are supplied via a dictionary:
        {current_colour: (next_colour, turn_direction)}
    where turn_direction is either 'R' (90° clockwise) or 'L' (90° counter‑clockwise).
    The ant starts facing North and occupies the cell given by `ant_position`.
    Moving outside the grid wraps to the opposite edge (toroidal topology).
    """

    _DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    _DIR_NAMES = ['North', 'East', 'South', 'West']

    def __init__(self, N, ant_position, rules):
        """
        Initialize the Langton's Ant simulation.

        Args:
            N (int): The grid size (NxN).
            ant_position (tuple): Starting coordinate of the ant as (r, c).
            rules (dict): Dictionary defining transition rules.
                          Format: {current_color: (next_color, turn_direction)}
        """
        self.N = N
        self.grid = np.zeros((N, N), dtype=int)
        self.ant_pos = ant_position
        self.ant_dir = 0
        self.rules = rules
        
        for color, (next_color, turn) in rules.items():
            if turn not in ('R', 'L'):
                raise ValueError(f"Invalid turn direction '{turn}' for color {color}. Must be 'R' or 'L'.")

    def get_states(self):
        """
        Returns the current state grid of the cells.

        Returns:
            np.ndarray: The NxN cellular grid.
        """
        return self.grid

    def get_current_position(self):
        """
        Returns the ant's current position as a tuple (r, c).

        Returns:
            tuple: Current coordinates of the ant.
        """
        return self.ant_pos

    def step(self):
        """
        Perform a single simulation step following the ruleset.

        1. Read the colour of the cell under the ant.
        2. Change the cell to the new colour dictated by the rules.
        3. Turn the ant according to the rule's direction ('R' or 'L').
        4. Move the ant one step forward.
        5. Wrap around the grid boundaries (toroidal).
        """
        r, c = self.ant_pos
        current_color = self.grid[r, c]
        
        if current_color not in self.rules:
            raise ValueError(f"No rule defined for color {current_color}")
            
        next_color, turn = self.rules[current_color]
        
        self.grid[r, c] = next_color

        if turn == 'R':
            self.ant_dir = (self.ant_dir + 1) % 4

        elif turn == 'L':
            self.ant_dir = (self.ant_dir - 1) % 4

        else:
            raise ValueError(f"Invalid turn direction '{turn}'; must be 'R' or 'L'.")
        
        dr, dc = self._DIRECTIONS[self.ant_dir]
        new_r = (r + dr) % self.N
        new_c = (c + dc) % self.N
        self.ant_pos = (new_r, new_c)

    def update(self):
        """
        Alias for step() to support standard animation.
        """
        self.step()

    def get_current_direction(self):
        """
        Returns the current direction of the ant as a string.
        Useful for debugging and visualization.
        """
        return self._DIR_NAMES[self.ant_dir]

    def run_simulation(self, steps=10000):
        """
        Run the simulation for a specified number of steps.
        Useful for testing thehighway pattern behavior.
        
        Args:
            steps (int): Number of simulation steps to run.
        """
        for _ in range(steps):
            self.step()
