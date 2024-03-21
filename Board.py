import numpy as np
import pygame
import sys

HEIGHT = 5
WIDTH = 6
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

class Board():
    def __init__(self):
        self.board = np.zeros((HEIGHT,WIDTH))
        self.game_over = False
        self.turn = 0

         # Pygame initialization
        pygame.init()
        self.width = WIDTH * SQUARESIZE
        self.height = (HEIGHT) * SQUARESIZE
        self.size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.size)
        self.draw_board()

    # def draw_board(self):
    #     for c in range(WIDTH):
    #         for r in range(HEIGHT):
    #             pygame.draw.rect(self.screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE, SQUARESIZE, SQUARESIZE))
    #             pygame.draw.circle(self.screen, BLACK, (int(c*SQUARESIZE + SQUARESIZE/2), int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)
        
    #     for c in range(WIDTH):
    #         for r in range(HEIGHT):        
    #             if self.board[r][c] == 1:
    #                 pygame.draw.circle(self.screen, RED, (int(c*SQUARESIZE + SQUARESIZE/2),  int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)
    #             elif self.board[r][c] == 2:
    #                 pygame.draw.circle(self.screen, YELLOW, (int(c*SQUARESIZE + SQUARESIZE/2), int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)
    #     pygame.display.update()

    def draw_board(self):
        for c in range(WIDTH):
            pygame.draw.rect(self.screen, BLUE, (c * SQUARESIZE, 0, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(self.screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(SQUARESIZE / 2)), RADIUS)
            
        for c in range(WIDTH):
            for r in range(HEIGHT):
                pygame.draw.rect(self.screen, BLUE, (c*SQUARESIZE, (r)*SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(self.screen, BLACK, (int(c*SQUARESIZE + SQUARESIZE/2), int((r)*SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), RADIUS)
        
        for c in range(WIDTH):
            for r in range(HEIGHT):        
                if self.board[r][c] == 1:
                    pygame.draw.circle(self.screen, RED, (int(c*SQUARESIZE + SQUARESIZE/2),  int((r)*SQUARESIZE + SQUARESIZE/2)), RADIUS)
                elif self.board[r][c] == 2:
                    pygame.draw.circle(self.screen, YELLOW, (int(c*SQUARESIZE + SQUARESIZE/2), int((r)*SQUARESIZE + SQUARESIZE/2)), RADIUS)
        pygame.display.update()

    # def draw_board(self):
    #     for c in range(WIDTH):
    #         for r in range(HEIGHT+1):
    #             pygame.draw.rect(self.screen, (0,0,255), (c*SQUARESIZE, r*SQUARESIZE, SQUARESIZE, SQUARESIZE))
    #             pygame.draw.circle(self.screen, (0,0,0), (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
        
    #     for c in range(WIDTH):
    #         for r in range(HEIGHT):
    #             if self.board[r][c] == 1:
    #                 pygame.draw.circle(self.screen, (255,0,0), (int(c*SQUARESIZE+SQUARESIZE/2), int((r+2)*SQUARESIZE - SQUARESIZE/2)), RADIUS)

    #                 # pygame.draw.circle(self.screen, (255,0,0), (int(c*SQUARESIZE+SQUARESIZE/2), self.height-int((r+1)*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    #             elif self.board[r][c] == 2:
    #                 pygame.draw.circle(self.screen, (255,255,0), (int(c*SQUARESIZE+SQUARESIZE/2), int((r+2)*SQUARESIZE - SQUARESIZE/2)), RADIUS)
    #                 # pygame.draw.circle(self.screen, (255,255,0), (int(c*SQUARESIZE+SQUARESIZE/2), self.height-int((r+1)*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    #     pygame.display.update()

    def playerMove(self, y, player):
        for i in range(HEIGHT-1, -1, -1):
            if self.board[i,y]==0:
                self.board[i,y] = player
                self.draw_board()
                break
    
    def getBoard(self):
        return self.board

    # 0: no winner, go on #1: player1 win #2: player2 win #3: tied game
    def checkWinner(self):
        # check column
        for i in range(HEIGHT-3):
            for j in range(WIDTH):
                if self.board[i][j]!=0 and self.board[i+1][j]==self.board[i][j] and self.board[i+2][j]==self.board[i][j] and self.board[i+3][j]==self.board[i][j]:
                    return self.board[i][j]
        # check row
        for j in range(WIDTH-3):
            for i in range(HEIGHT):
                if self.board[i][j]!=0 and self.board[i][j+1]==self.board[i][j] and self.board[i][j+2]==self.board[i][j] and self.board[i][j+3]==self.board[i][j]:
                    return self.board[i][j]
        # check diagonal left
        for i in range(3,HEIGHT):
            for j in range(WIDTH-3):
                if self.board[i][j]!=0 and self.board[i-1][j+1]==self.board[i][j] and self.board[i-2][j+2]==self.board[i][j] and self.board[i-3][j+3]==self.board[i][j]:
                    return self.board[i][j]
        # check diagonal right
        for i in range(HEIGHT-3):
            for j in range(3):
                if self.board[i][j]!=0 and self.board[i+1][j+1]==self.board[i][j] and self.board[i+2][j+2]==self.board[i][j] and self.board[i+3][j+3]==self.board[i][j]:
                    return self.board[i][j]
        # not finished
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if self.board[i][j] == 0:
                    return 0
        # tied
        return 3

