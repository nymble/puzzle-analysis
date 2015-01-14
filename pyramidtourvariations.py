#!/usr/bin/env python
"""
    Pyramid Tour Puzzle Analysis
    Cryptographic Research Winter Holiday Puzzle 2014
    wwww.cryptography.com/puzzle2014
    
    Analysis of all variations of piece types for 4x4 puzzle
    
        All combinations of pieces with solutions
             1   2    3  Solutions
         --------------------------
        (0,  0, 10,  6)     8
        (0,  0, 12,  4)     4
        (0,  1,  8,  7)    16   <- Pyrimid Tour Puzzle
        (0,  1, 10,  5)    40
        (0,  1, 12,  3)    16
        (0,  2,  8,  6)   184
        (0,  2, 10,  4)   448
        (0,  2, 12,  2)   120
        (0,  3,  6,  7)   176
        (0,  3,  8,  5)  1736
        (0,  3, 10,  3)  1712
        (0,  3, 12,  1)   208
        (0,  4,  6,  6)  1720
        (0,  4,  8,  4)  7452
        (0,  4, 10,  2)  3912
        (0,  4, 12,  0)   164
        (0,  5,  4,  7)   704
        (0,  5,  6,  5) 10208
        (0,  5,  8,  3) 18720
        (0,  5, 10,  1)  4584
        (0,  6,  4,  6)  4424
        (0,  6,  6,  4) 32840
        (0,  6,  8,  2) 28784
        (0,  6, 10,  0)  2352
        (0,  7,  2,  7)   688
        (0,  7,  4,  5) 17952
        (0,  7,  6,  3) 61792
        (0,  7,  8,  1) 23400
        (0,  8,  2,  6)  2976
        (0,  8,  4,  4) 41076
        (0,  8,  6,  2) 67320
        (0,  8,  8,  0)  8124
        (0,  9,  0,  7)    80
        (0,  9,  2,  5)  8760
        (0,  9,  4,  3) 56960
        (0,  9,  6,  1) 38032
        (0, 10,  0,  6)   288
        (0, 10,  2,  4) 15000
        (0, 10,  4,  2) 44400
        (0, 10,  6,  0)  8712
        (0, 11,  0,  5)   600
        (0, 11,  2,  3) 14544
        (0, 11,  4,  1) 19072
        (0, 12,  0,  4)   748
        (0, 12,  2,  2)  8992
        (0, 12,  4,  0)  3508
        (0, 13,  0,  3)   624
        (0, 13,  2,  1)  3208
        (0, 14,  0,  2)   264
        (0, 14,  2,  0)   488
        (0, 15,  0,  1)    72
        (0, 16,  0,  0)    12
    
    Paul A. Lambert 2014
"""
from copy import deepcopy

# Pyramid Tour Puzzle is a 4x4 tray holding 16 pieces
size = 4
tray = [[ None for y in range(size)] for x in range(size)]  # an empty array 

# There are different types of pieces that have values indicating the 'hop'
# distance to the next location 
piece_types = (1, 2, 3)

# There are different numbers of each type (1 of hop 1, 8 of hop 2, 7 of hop 3)
# piece_types_available = (0, 1, 8, 7 )

# Each piece may be oriented in one of four directions
piece_directions = { 'N': ( 0, 1),
                     'S': ( 0,-1),
                     'E': ( 1, 0),
                     'W': (-1, 0) }

""" search and assign inspired by http://norvig.com/sudoku.html """

def search(tray, location, piece_count, types_used, path):
    """ Using depth-first search, try all possible values."""
    global solution_count   
    if tray is False:
        return False            # Failed on earlier search
    if piece_count >= size*size:
        solution_count = solution_count + 1
        #print_tray(tray)
        return tray           ## Solved!
    # Step through each piece type and orientation
    for ptype in piece_types:
        # only use pieces that are available
        if types_used[ptype] < piece_types_available[ptype]:
            for direction in piece_directions:   # try all orientations of piece               
                new_tray, new_location, new_types_used, new_path = assign(tray,
                      location, ptype, direction, types_used, piece_count, path)
                if new_tray:
                    search(new_tray, new_location, piece_count + 1, new_types_used, new_path)

def assign(tray, location, ptype, direction, types_used, piece_count, path):
    """ Add next piece if it works, assumes location is empty """
    dx, dy = piece_directions[direction]
    x, y = location
    new_x = x + dx*ptype
    new_y = y + dy*ptype
    # check that next location lands in tray
    if ( 0 <= new_x < size ) and ( 0 <= new_y < size ):
        if (not tray[new_x][new_y]) or ((piece_count == 15) and
                                         new_x == 0 and new_y == 0):
            new_tray = deepcopy(tray)
            new_tray[x][y] = "{}{}".format(ptype, direction)
            new_types_used = deepcopy(types_used)
            new_types_used[ptype] = types_used[ptype] + 1
            new_path = path + "{}{}".format(ptype, direction) + ' '
            return new_tray, (new_x, new_y), new_types_used, new_path
                
    new_tray = False
    return new_tray, location, types_used, path

if __name__ == "__main__":
    """ Find solutions for all variations of pieces """
    start_location = (0,0)  # bottom left corner 
    init_piece_count = 0
    max_num_of_pieces = size*size
    for num_of_1s in range(max_num_of_pieces + 1): 
        for num_of_2s in range(max_num_of_pieces - num_of_1s + 1):
            num_of_3s = max_num_of_pieces - num_of_1s - num_of_2s
            solution_count = 0
            init_piece_count = 0
            piece_types_available = (0, num_of_1s, num_of_2s, num_of_3s)
            piece_types_used = [0 for i in range(size)]
            
            search(tray, start_location, init_piece_count, piece_types_used, '')
            if solution_count > 0 :
                print piece_types_available, solution_count



