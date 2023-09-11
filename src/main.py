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
            game.show_moves(screen)
            game.show_pieces(screen)

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
                        board.calc_moves(piece, clicked_row,  clicked_col)
                        dragger.save_initial(event.pos)
                        dragger.drag_piece(piece)

                        # Show methods:
                        game.showBG(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)

                # The drag:
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.showBG(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        dragger.update_blit(screen)
                
                # The click release:
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragger.undrag_piece()

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()



main = Main()
main.mainLoop()