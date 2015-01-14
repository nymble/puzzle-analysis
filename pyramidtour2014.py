#!/usr/bin/env python
"""
    Pyramid Tour Puzzle Analysis - Version 2
    Cryptographic Research Winter Holiday Puzzle 2014
    wwww.cryptography.com/puzzle2014
    
    Copyright Paul A. Lambert 2014
"""
from copy import deepcopy

directions = { 'N': ( 0, 1), # pieces are oriented in a direction
               'S': ( 0,-1),
               'E': ( 1, 0),
               'W': (-1, 0) }

class Piece:
    """ Pieces have a type and a direction (N, S, E, W) """
    def __init__(self, ptype, direction):
        self.type = ptype
        self.direction = direction
    
    def next_location(self, (x,y), size):
        """ Next location indicated by piece starting at location """
        dir_x, dir_y = directions[self.direction]
        next = (x + self.type*dir_x, y + self.type*dir_y)
        if ( 0 <= next[0] < size ) and ( 0 <= next[1] < size ):
            return next
        else:
            return None   # next is off the tray
        
    def __str__(self):
        return '{}{} '.format(self.type, self.direction)

class TrayIllegalMove(Exception):
    """ Use exceptions for illegal positions in a tray """
    def __init__(self, value):
        self.value = value

class Tray:
    """ The Pyramid Tour Puzzle has a 4x4 tray holding 16 pieces """  
    size = 4
    piece_types = (1,2,3) # type indicates hops
    piece_types_available = (0, 1, 8, 7 )  # index is type (8 available of 3)

    def __init__(self, piece=None, tray=None):
        """ A Tray is created by adding a piece to prior legal tray,
            or starting with a blank tray (None).
        """
        if not tray: # new empty tray, no pieces used
            self.array = [[ None for y in range(self.size)] for x in range(self.size)] 
            self.types_used = [ 0 for num_types in range(self.size) ]
            self.location = (0, 0)
            self.piece_count = 0
            self.path = ''  # string path of pieces
        else:  # clone prior tray and put new piece in tray at next location
            # check that the piece type is available
            if tray.types_used[piece.type] >= self.piece_types_available[piece.type]:
                raise TrayIllegalMove( 'no pieces of type {} available'.format(piece.type) )
            
            next = piece.next_location(tray.location, self.size)
            if not next:
                raise TrayIllegalMove( 'Next location not in tray' )
            next_x, next_y = next
            if tray.array[next_x][next_y]: # not empty
                if tray.piece_count < (self.size*self.size - 1): # not last piece
                    raise TrayIllegalMove ( 'Next location not empty' )
            # place piece and update tray
            x, y = tray.location
            self.array = deepcopy(tray.array)
            self.array[x][y] = piece
            self.types_used = [ used for used in tray.types_used ]
            self.types_used[piece.type] += 1 
            self.location = (next_x, next_y)
            self.piece_count = tray.piece_count + 1
            self.path = tray.path + '{}'.format(piece)
            
    def new_tray(self, piece):
        tray = Tray(piece, self)
        return tray
        
    def __repr__(self):
        """ Display tray using array indexes as x, y coordinates"""
        tray_string = '  '
        for y in reversed(range(self.size)): 
            for x in range(self.size):  
                if self.array[x][y]:
                    tray_string += self.array[x][y].__str__()
                else:
                    tray_string += '__ '   # no piece at location
            tray_string += '\n  '
        return tray_string
    
    def solve(self):
        """ Find all solutions.  Includes symmetric dupplicates """
        # print self.path
        if self.piece_count >= self.size*self.size:
            print "--- solution ---"
            print self
            return
        # Step through each piece type and orientation
        for ptype in self.piece_types: 
            for direction in directions: # try all orientations
                piece = Piece(ptype, direction)
                try:
                    new_tray = Tray(piece, self) # exception raised for illegal moves
                    new_tray.solve()  
                except TrayIllegalMove:
                    pass

if __name__ == "__main__":
    tray = Tray()
    tray.solve()

    
  