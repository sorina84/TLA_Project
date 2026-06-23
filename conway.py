"""
The Game of Life (GoL) module named in honour of John Conway

This module defines the classes required for the GoL simulation.

"""
import numpy as np
import re
from scipy import signal, ndimage


def parse_pattern(filepath):

    cells = []
    w, h = 0, 0


    with open(filepath, 'r') as f:
        lines = f.readlines()

    # plaintex(.cells)
    if filepath.endswith('.cells') or filepath.endswith('.cells.txt'):
        r = 0 #roe
        max_c = 0 #max col
        for line in lines:
            line = line.strip('\n') 
            if line.startswith('!'):
                continue

            for c, char in enumerate(line):
                if char == 'O':
                    cells.append((r, c))
                max_c = max(max_c, c + 1)           
            r += 1           
        h = r
        w = max_c


   # (.rle)

    elif filepath.endswith('.rle'):
        r, c = 0, 0
        
        temp = ""
        
        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                continue

            if line.startswith('x'):
                parts = line.split(',')
                w = int(parts[0].split('=')[1].strip())
                h = int(parts[1].split('=')[1].strip())
                continue
            
            temp += line 

        num = ""
        for char in temp:
            if char.isdigit():
                num += char
            elif char in ('b', 'o'):
                count = int(num) if num else 1
                if char == 'o': 
                    for i in range(count):
                        cells.append((r, c + i))
                c += count
                num = ""
            elif char == '$': 
                count = int(num) if num else 1
                r += count
                c = 0
                num = ""
            elif char == '!': 
                break

    return w, h, cells
    



class GameOfLife:
    """
    Object for computing Conway's Game of Life (GoL) cellular machine/automata
    """

    def __init__(self, N=256, finite=False, fastMode=False):
        self.grid = np.zeros((N, N), np.uint)
        self.neighborhood = np.ones((3, 3), np.uint)  # 8 connected kernel
        self.neighborhood[1, 1] = 0  # do not count centre pixel
        self.finite = finite
        self.fastMode = fastMode
        self.aliveValue = 1
        self.deadValue = 0
        self.rows = N  # use for slow implementation of evolve
        self.cols = N  # use for slow implementation of evolve

    def getStates(self):
        """
        Returns the current states of the cells
        """
        return self.grid

    def getGrid(self):
        """
        Same as getStates()
        """
        return self.getStates()

    def update_grid_fast(self, grid):

        if self.finite:
            mode = 'fill'
        else:
            mode = 'wrap'           
        mcount = signal.convolve2d(grid, self.neighborhood, mode='same', boundary=mode, fillvalue=0)

        next_gen = np.zeros_like(grid)
        # rule for alive
        alive_mask = (grid == 1) & ((mcount == 2) | (mcount == 3))
        next_gen[alive_mask] = 1

        # rule for reproduction
        birth_mask = (grid == 0) & (mcount == 3)
        next_gen[birth_mask] = 1

        return next_gen
    


    def evolve(self):
        
        
        if self.fastMode:
            self.grid = self.update_grid_fast(self.grid)
        else:
            new_grid = np.zeros_like(self.grid)
            h, w = self.grid.shape
            for r in range(h):
                for c in range(w):
                    # (Toroidal/wrapping)
                    ncount = 0
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue

                            nr, nc = r + dr, c + dc

                            if self.finite:
                              
                                if 0 <= nr < h and 0 <= nc < w:
                                    ncount += self.grid[nr, nc]
                            else:

                                ncount += self.grid[nr % h, nc % w]

                    #  rule
                    cell = self.grid[r, c]

                    if cell == 1:
                        
                        if ncount < 2 or ncount > 3:
                            new_grid[r, c] = 0  
                        else:
                            new_grid[r, c] = 1  
                            
                    else:
                        if ncount == 3:
                            new_grid[r, c] = 1   

            self.grid = new_grid
            
            

    def insertBlinker(self, index=(0, 0)):
        '''
        Insert a blinker oscillator construct at the index position
        '''
        self.grid[index[0], index[1] + 1] = self.aliveValue
        self.grid[index[0] + 1, index[1] + 1] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 1] = self.aliveValue

    def insertGlider(self, index=(0, 0)):
        '''
        Insert a glider construct at the index position
        '''
        self.grid[index[0], index[1] + 1] = self.aliveValue
        self.grid[index[0] + 1, index[1] + 2] = self.aliveValue
        self.grid[index[0] + 2, index[1]] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 1] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 2] = self.aliveValue

    def insertGliderGun(self, index=(0, 0)):
        '''
        TODO: [Part 1c - Glider Gun Fix]
        The current glider gun pattern is broken. Leave the broken array in the code 
        and instruct the student to debug and fix the coordinates so it loops infinitely.
        '''
        self.grid[index[0] + 1, index[1] + 26] = self.aliveValue

        self.grid[index[0] + 2, index[1] + 24] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 26] = self.aliveValue

        self.grid[index[0] + 3, index[1] + 14] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 15] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 22] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 23] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 36] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 37] = self.aliveValue

        self.grid[index[0] + 4, index[1] + 13] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 17] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 22] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 23] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 36] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 37] = self.aliveValue

        self.grid[index[0] + 5, index[1] + 2] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 3] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 12] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 18] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 22] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 23] = self.aliveValue

        self.grid[index[0] + 6, index[1] + 2] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 3] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 12] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 16] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 18] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 19] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 24] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 26] = self.aliveValue

        self.grid[index[0] + 7, index[1] + 12] = self.aliveValue
        self.grid[index[0] + 7, index[1] + 18] = self.aliveValue
        self.grid[index[0] + 7, index[1] + 26] = self.aliveValue

        self.grid[index[0] + 8, index[1] + 13] = self.aliveValue
        self.grid[index[0] + 8, index[1] + 17] = self.aliveValue

        self.grid[index[0] + 9, index[1] + 14] = self.aliveValue
        self.grid[index[0] + 9, index[1] + 15] = self.aliveValue

    def insertFromFile(self, filename, index=((0, 0))):
        '''
        Insert cells from pattern file using parse_pattern
        '''
        width, height, live_cells = parse_pattern(filename)
        for r, c in live_cells:
            target_r = index[0] + r
            target_c = index[1] + c
            if 0 <= target_r < self.rows and 0 <= target_c < self.cols:
                self.grid[target_r, target_c] = self.aliveValue
