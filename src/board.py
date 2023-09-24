from imports import *
from square import *
from move import *
from const import *
import copy

class Board:
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces("white")
        self._add_pieces("black")

    def move(self, piece, move):
        initial = move.initial
        final = move.final

        # console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # pawn promotion:
        if isinstance(piece, Pawn):
            self.check_promotion(piece, final)

        # king castling:
        if isinstance(piece, King):
            if self.castling(initial, final):
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])

        # move
        piece.moved = True

        # clear valid moves
        piece.clear_moves()
        
        # set last move
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move)

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_enemy_piece(piece.color):
                    # p = piece, m = move
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col)

                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True
            return False

    def calc_moves(self, piece, row, col):
        '''
            Calculate all the possible/valid moves of a specific piece 
        '''

        def new_move(move_row, move_col):
            # Create squares for the new move:
            initial = Square(row, col)
            final = Square(move_row, move_col)

            # Creating new move:
            move = Move(initial, final)
                        
            # Append new valid move:
            piece.add_move(move)

        # Possible Moves: 
        def pawn_moves():
            steps = 1 if piece.moved else 2

            # Vertical moves:
            start = row + piece.direction
            end = row + (piece.direction * (1 + steps))

            for move_row in range(start, end, piece.direction):
                # "move_row" is the possible move row, and same with the cols
                if Square.in_range(move_row):
                    if self.squares[move_row][col].is_empty():
                        new_move(move_row, col)

                    # If square isn't empty, its blocked
                    else: break 
                         
                # Not in range
                else: break 
                              
            #Diagonal moves:
            move_row = row + piece.direction
            move_cols = [col - 1, col + 1]
            for move_col in move_cols:
                if Square.in_range(move_row, move_col):
                    if self.squares[move_row][move_col].has_rival_piece(piece.color):
                        # create initial and final move squares:
                        initial = Square(row, col)
                        final_piece = self.squares[move_row, move_col].piece
                        final = Square(move_row, move_col, final_piece)

                        # create a new move:
                        new_move(initial, final)

                        # a

        def knight_moves():
            # 8 maximum possible moves for a knight
            possible_moves = [
                (row - 2, col + 1),
                (row - 1, col + 2),
                (row + 1, col + 2),
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row + 1, col - 2),
                (row - 1, col - 2),
                (row - 2, col - 1)
            ]

            for move in possible_moves:
                move_row, move_col = move
                # print("Clicked row and col in board.py")
                # print(f'move row: {move_row}, move col: {move_col}' )
            
                if Square.in_range(move_row, move_col):
                    # Checking if the square is empty or not:
                    if self.squares[move_row][move_col].isempty_or_rival(piece.color):
                        # create initial and final move squares:
                        initial = Square(row, col)
                        final_piece = self.squares[move_row][move_col].piece
                        final = Square(move_row, move_col, final_piece)

                        # create a new move:
                        new_move(initial, final)

        def straightline_moves(incrs):
            for inc in incrs:
                row_inc, col_inc = inc

                # Possible moves for rows and cols
                move_row = row + row_inc
                move_col = col + col_inc

                while True:
                    if Square.in_range(move_row, move_col):
                        # Create initial and final move squares:
                        # create initial and final move squares:
                        initial = Square(row, col)
                        final_piece = self.squares[move_row, move_col].piece
                        final = Square(move_row, move_col, final_piece)

                        # Create a possible new move:
                        move = Move(initial, final)

                        # Empty
                        if self.squares[move_row][move_col].is_empty():
                            # Append move
                            piece.add_move(move)
                        
                        # Has rival piece:
                        elif self.squares[move_row][move_col].has_rival_piece(piece.color):
                            # Append move
                            piece.add_move(move)
                            break

                        # Has team piece:
                        elif self.squares[move_row][move_col].has_ally_piece(piece.color):
                            break

                    # If not in range
                    else: break

                    # Incrementing through incrs:
                    move_row = move_row + row_inc
                    move_col =  move_col + col_inc

        def king_moves():
            adjs = [
                (row - 1, col + 0), # Up
                (row - 1, col + 1), # Up right
                (row + 0, col + 1), # Right
                (row + 1, col + 1), # Down right
                (row + 1, col + 0), # Down
                (row + 1, col - 1), # Down left
                (row + 0, col - 1), # Left
                (row - 1, col - 1)  # Up left
            ]

            for move in adjs:
                move_row, move_col = move

                if Square.in_range(move_row, move_col):
                    if self.squares[move_row][move_col].isempty_or_rival(piece.color):
                        new_move(move_row, move_col)

            # castling moves:
            if not piece.moved:

                # short castle:
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            if self.squares[row][c].has_piece():
                                # castling not possible
                                break
                        
                            elif c == 6:
                                # adds right rook to king
                                piece.right_rook = right_rook

                                # rook move:
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                move = Move(initial, final)
                                right_rook.add_move(move)

                                # king move:
                                initial = Square(row, col)
                                final = Square(row, 6)
                                move = Move(initial, final)
                                piece.add_move(move)

                # long castle:
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            if self.squares[row][c].has_piece():
                                # castling not possible
                                break
                        
                            elif c == 3:
                                # adds left rook to king
                                piece.left_rook = left_rook

                                # rook move:
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                move = Move(initial, final)
                                left_rook.add_move(move)

                                # king move:
                                initial = Square(row, col)
                                final = Square(row, 2)
                                move = Move(initial, final)
                                piece.add_move(move)


        if isinstance(piece, Pawn): pawn_moves()
        elif isinstance(piece, Knight): knight_moves()
        elif isinstance(piece, Bishop): 
            straightline_moves(
                [
                    (-1, 1), # Up-right
                    (-1, -1), # Up-left
                    (1, 1), # Down-right
                    (1, -1) # Down-left
                ]
        )
            
        elif isinstance(piece, Rook): 
            straightline_moves(
                [
                    (-1, 0), # Up
                    (0, 1), # Right
                    (1, 0), # Down
                    (0, -1) # Left
                ]
        )
            
        elif isinstance(piece, Queen): 
            straightline_moves(
                [
                    (-1, 1), # Up-right
                    (-1, -1), # Up-left
                    (1, 1), # Down-right
                    (1, -1), # Down-left
                    (-1, 0), # Up
                    (0, 1), # Right
                    (1, 0), # Down
                    (0, -1) # Left
                ]
        )
            
        elif isinstance(piece, King): king_moves()

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == "white" else (1, 0)

        # Creating pawns:
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
                    
        # Creating Knights:
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # Creating Bishops:
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # Creating Rooks:
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # Creating Queen:
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # Creating King:
        self.squares[row_other][4] = Square(row_other, 4, King(color))
