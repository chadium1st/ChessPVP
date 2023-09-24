from imports import *

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        self.game = Game()



    def mainLoop(self):
        game = self.game
        screen = self.screen
        dragger = self.game.dragger
        board = self.game.board

        while True:
            # Show methods:
            game.showBG(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                # The click:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    
                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    # print("Clicked row and col in main.py: ")
                    # print(clicked_row)
                    # print(clicked_col)

                    # If the clicked square has a piece:
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # valid piece (color)?
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row,  clicked_col)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)

                            # Show methods:
                            game.showBG(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                # The drag:
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE

                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.showBG(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)
                
                # The click release:
                elif event.type == pygame.MOUSEBUTTONUP:

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        # create possiblem move:
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)

                        move = Move(initial, final)

                        # valid move:
                        if board.valid_move(dragger.piece, move):

                            captured = board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece, move)
                            #sounds:
                            game.play_sound(captured)
                            # show methods:
                            game.showBG(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)

                            # next turn:
                            game.next_turn()

                    dragger.undrag_piece()

                # key press:
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        # changing themes:
                        game.change_theme()

                    elif event.key == pygame.K_r:
                        # restarting:
                        game.reset()
                        game = self.game
                        dragger = self.game.dragger
                        board = self.game.board

                # quit application:
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


main = Main()   
main.mainLoop()