import random
from Board import Board
import MiniMax
from QLearning import PlayQlearning
import matplotlib.pyplot as plt

def trainQLearning(trainNum):
    playerQ1 = PlayQlearning(1)
    playerQ2 = PlayQlearning(2)
    cnt = 0
    while cnt < trainNum:
        print(cnt)
        cnt += 1
        # random first player
        Player1First = random.choice([True, False])
        # initialize board
        board = Board()
        playerQ1.newGame()
        playerQ2.newGame()
        # play game to finish
        while board.checkWinner() == 0:
            # First Player
            playerQ = playerQ1 if Player1First else playerQ2
            y1 = playerQ.findBestMove(board.getBoard())
            board.playerMove(y1, 1 if Player1First else 2)
            # game finish
            if board.checkWinner() != 0:
                playerQ1.finalResult(board.checkWinner())
                playerQ2.finalResult(board.checkWinner())
                break
            else:
                # second player
                playerQ = playerQ2 if Player1First else playerQ1
                y2 = playerQ.findBestMove(board.getBoard())
                board.playerMove(y2, 2 if Player1First else 1)
                # game finish
                if board.checkWinner() != 0:
                    playerQ1.finalResult(board.checkWinner())
                    playerQ2.finalResult(board.checkWinner())
                    break
    return playerQ1, playerQ2

def play(player1, player2, loopNum, trainNum, useAlphaBeta):
    player1WinCount = 0
    player2WinCount = 0
    tiedCount = 0
    # if q-learning player
    if player1 == 2 or player2 == 2:
        playerQ1, playerQ2 = trainQLearning(trainNum)
    cnt = 0
    # for the image
    x = []
    player1Win = []
    player2Win = []
    tied = []
    while cnt < loopNum:
        print(cnt)
        cnt += 1
        # random first player
        Player1First = random.choice([True, False])
        # initialize board
        board = Board()
        if player1 == 2 or player2 == 2:
            playerQ1.newGame()
            playerQ2.newGame()
        # play game to finish
        while board.checkWinner() == 0:
            # First Player
            player = player1 if Player1First else player2
            if player1 == 2 or player2 == 2:
                playerQ = playerQ1 if Player1First else playerQ2
        
            if player == 1:
                y1 = MiniMax.miniMaxAlgo(1 if Player1First else 2, board.getBoard(), useAlphaBeta) 
            elif player == 2:
                y1 = playerQ.findBestMove(board.getBoard())

            board.playerMove(y1, 1 if Player1First else 2)
            # game finish
            if board.checkWinner() != 0:
                if board.checkWinner() == 3:
                    tiedCount += 1
                elif board.checkWinner() == 1:
                    player1WinCount += 1
                elif board.checkWinner() == 2:
                    player2WinCount += 1

                if player1 == 2:
                    playerQ1.finalResult(board.checkWinner())
                if player2 == 2:
                    playerQ2.finalResult(board.checkWinner())

                x.append(cnt)
                player1Win.append(player1WinCount/cnt)
                player2Win.append(player2WinCount/cnt)
                tied.append(tiedCount/cnt)
                break
            else:
                # second player
                player = player2 if Player1First else player1
                if player1 == 2 or player2 == 2:
                    playerQ = playerQ2 if Player1First else playerQ1

                if player == 1:
                    y2 = MiniMax.miniMaxAlgo(2 if Player1First else 1, board.getBoard(), useAlphaBeta) 
                elif player == 2:
                    y2 = playerQ.findBestMove(board.getBoard())

                board.playerMove(y2, 2 if Player1First else 1)
                # game finish
                if board.checkWinner() != 0:
                    if board.checkWinner() == 3:
                        tiedCount += 1
                    elif board.checkWinner() == 1:
                        player1WinCount += 1
                    elif board.checkWinner() == 2:
                        player2WinCount += 1

                    if player1 == 2:
                        playerQ1.finalResult(board.checkWinner())
                    if player2 == 2:
                        playerQ2.finalResult(board.checkWinner())

                    x.append(cnt)
                    player1Win.append(player1WinCount/cnt)
                    player2Win.append(player2WinCount/cnt)
                    tied.append(tiedCount/cnt)
                    break
    
    plt.plot(x,player1Win,color = 'r',label=["Default Win", "Minimax Win", "Q-Learning Win"][player1])
    plt.plot(x,player2Win,color = 'g',label=["Default Win", "Minimax Win", "Q-Learning Win"][player2])
    plt.plot(x,tied,color = 'b',label="Tied")

    plt.xlabel("Game count")
    plt.ylabel("Probability")
    plt.legend(loc = "upper right")
    plt.show()

def configure_and_play():
    trainNum = 50  # Número de juegos de entrenamiento para Q-learning
    gameNum = 50   # Número de juegos para jugar
    
    # Juega Q-learning vs. Minimax sin poda alfa-beta
    print("Q-learning vs. Minimax (Sin Poda Alfa-Beta)")
    play(2, 1, gameNum, trainNum, useAlphaBeta=False) 
    
    # Juega Q-learning vs. Minimax con poda alfa-beta
    print("Q-learning vs. Minimax (Con Poda Alfa-Beta)")
    play(2, 1, gameNum, trainNum, useAlphaBeta=True)

configure_and_play()


# # 0: defalt  1: minimax  2:q learning
# play(2, 1, 1000000, 0)