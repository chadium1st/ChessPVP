class Square:
    def __init__(self, row, col, piece = None):
        self.row = row
        self.col = col
        self.piece = piece

    def has_piece(self):
        return self.piece != None
    
    def is_empty(self):
        return not self.has_piece()
    
    def has_ally_piece(self, color):
        return self.has_piece() and self.piece.color == color
    
    def has_rival_piece(self, color):
        '''
            Checking if it has a piece and whether it is a rival piece or not.
        '''
        return self.has_piece() and self.piece.color != color
    
    def isempty_or_rival(self, color):
        return self.is_empty() or self.has_rival_piece(color)

    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
            
        return True