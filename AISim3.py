# Reversegam: a clone of Othello/Reversi
import random
import sys
WIDTH = 8 # Board is 8 spaces wide.
HEIGHT = 8 # Board is 8 spaces tall.
def drawBoard(board):
    # Print the board passed to this function. Return None.
    print('  12345678')
    print(' +--------+')
    for y in range(HEIGHT):
        print('{}|'.format(y+1), end='')
        for x in range(WIDTH):
            print(board[x][y], end ='')
        print('|{}'.format(y+1))
    print(' +--------+')
    print('  12345678')

def getNewBoard():
    # Creates a brand-new, blank board data structure.
    board = []
    for i in range(WIDTH):
        board.append([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])
    return board

def isValidMove(board, tile, xStart, yStart):
    # Returns False if the player's move on space xstart, ystart is invalid.
    # If it is a valid move, return a list of spaces that would become the player's if they made a move here.
    if board[xStart][yStart] != ' ' or not isOnBoard(xStart, yStart):
        return False

    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'

    tilesToFlip = []
    for xDirection, yDirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xStart, yStart
        x += xDirection # First step in the X direction
        y += yDirection # First step in the Y direction
        while isOnBoard(x, y) and board[x][y] == otherTile:
            # Keep moving in this x & y direction.
            x += xDirection
            y += yDirection
            if isOnBoard(x, y) and board[x][y] == tile:
                # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way
                while True:
                    x -= xDirection
                    y -= yDirection
                    if x == xStart and y == yStart:
                        break
                    tilesToFlip.append([x,y])

    if len(tilesToFlip) == 0: # If no tiles were flipped, this is not a valid move.
        return False
    return tilesToFlip

def isOnBoard(x, y):
    # Return True if the coordinates are located on the board.
    return x >= 0 and x <= WIDTH - 1 and y >= 0 and y <= HEIGHT - 1

def getBoardWithValidMoves(board, tile):
    # Return a new board with periods marking the valid moves the player can make.
    boardCopy = getBoardCopy(board)

    for x, y in getValidMoves(boardCopy, tile):
        boardCopy[x][y] = '.'
    return boardCopy

def getValidMoves(board, tile):
    # Returns a list of [x,y] lists of valid moves for the given player on the given board.
    validMoves = []
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x,y])
    return validMoves

def getScoreOfBoard(board):
    # Determine the score by counting the tiles. Returns a dictionary with keys 'X' and 'O'.
    xScore = 0
    oScore = 0
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if board[x][y] == 'X':
                xScore += 1
            if board[x][y] == 'O':
                oScore += 1
    return {'X': xScore, 'O': oScore}

def enterPlayerTile():
    # Let the player enter which tile they want to be.
    # Return a list with the player's tile as the first item and the computer's tile as the second.
    tile = ''
    while not (tile == 'X' or tile == 'O'):
        print('Do you want to be X or O?')
        tile = input().upper()

    # The first item in the list is the player's tile, and the second is the computer's tile
    if tile == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']

def whoGoesFirst():
    # Randomly choose who goes first.
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'

def makeMove(board, tile, xStart, yStart):
    # Place the tile on the board at xStart, yStart and flip any of the opponent's pieces.
    # Return False if this is an invalid move; True if it is valid.
    tilesToFlip = isValidMove(board, tile, xStart, yStart)

    if tilesToFlip == False:
        return False

    board[xStart][yStart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True

def getBoardCopy(board):
    # Make a duplicate of the board list and return it.
    boardCopy = getNewBoard()
    for x in range(WIDTH):
        for y in range(HEIGHT):
            boardCopy[x][y] = board[x][y]

    return boardCopy

def isOnCorner(x, y):
    # Return True if the position is one of the four corners.
    return (x == 0 or x == WIDTH - 1) and (y == 0 and y == HEIGHT - 1)

def getPlayerMove(board, playerTile):
    # Let the player enter their move.
    # Return the move as [x, y] (or return the strings 'hints' or 'quit').
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
    while True:
        print('Enter your move, "quit" to quit the game, or "hints" to toggle hints.')
        move = input().lower()
        if move == 'quit' or move == 'hints':
            return move

        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isValidMove(board, playerTile, x, y) == False:
                continue
            else:
                break
        else:
            print('That is not a valid. Enter the column (1-8) and then the row (1-8).')
            print('For example, 81 will move on the top right corner.')

    return [x, y]

def getCornerBestMove(board, computerTile):
    # Given a board and the computer's tile, determine where to
    # move and return that move as an [x, y] list.
    possibleMoves = getValidMoves(board, computerTile)
    random.shuffle(possibleMoves) # Randomise the order of the moves

    # Always go for a corner if available.
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]

    # Find the highest-scoring move possible.
    bestScore = -1
    for x, y in possibleMoves:
        boardCopy = getBoardCopy(board)
        makeMove(boardCopy, computerTile, x, y)
        score = getScoreOfBoard(boardCopy)[computerTile]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove

def getWorstMove(board, computerTile):
    # Return the move that flips the least number of tiles.
    possibleMoves = getValidMoves(board, computerTile)
    random.shuffle(possibleMoves) # Randomise the order of the moves.

    # Find the lowest scoring move possible
    worstScore = 64
    for x, y in possibleMoves:
        boardCopy = getBoardCopy(board)
        makeMove(boardCopy, computerTile, x, y)
        score = getScoreOfBoard(boardCopy)[computerTile]
        if score < worstScore:
            worstScore = score
            worstMove = [x, y]

    return worstMove

def getRandomMove(board, computerTile):
    possibleMoves = getValidMoves(board, computerTile)
    return random.choice(possibleMoves)

def isOnSide(x, y):
    return x == 0 or x == WIDTH - 1 or y == 0 or y == HEIGHT - 1

def getCornerSideBestMove(board, computerTile):
    # Return a corner move, a side move, or the best move.
    possibleMoves = getValidMoves(board, computerTile)
    random.shuffle(possibleMoves) # Randomise the order of the moves

    # Always go for a corner if available.
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]

    # If there is no corner move to take return a side move.
    for x, y in possibleMoves:
        if isOnSide(x, y):
            return [x, y]

    return getCornerBestMove(board, computerTile) # Do what the normal AI would do

def printScore(board, playerTile, computerTile):
    scores = getScoreOfBoard(board)
    print('You: {} points. Computer: {} points.'.format(scores[playerTile], scores[computerTile]))

def playGame(playerTile, computerTile):
    showHints = False
    turn = whoGoesFirst()
    #print('The {} will go first'.format(turn))

    # Clear the board and place starting pieces.
    board = getNewBoard()
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'

    while True:
        playerValidMoves = getValidMoves(board, playerTile)
        computerValidMoves = getValidMoves(board, computerTile)

        if playerValidMoves == [] and computerValidMoves == []:
            return board # No one can move, so end the game.

        elif turn == 'player': # Player's turn
            if playerValidMoves != []:
                # if showHints:
                #     validMovesBoard = getBoardWithValidMoves(board, playerTile)
                #     drawBoard(validMovesBoard)
                # else:
                #     drawBoard(board)
                # printScore(board, playerTile, computerTile)
                #
                move = getCornerSideBestMove(board, playerTile)
                # if move == 'quit':
                #     print('Thanks for playing!')
                #     sys.exit() # Terminate the program
                # elif move == 'hints':
                #     showHints = not showHints
                #     continue
                # else:
                makeMove(board, playerTile, move[0], move[1])
            turn = 'computer'

        elif turn == 'computer': # Computer's turn
            if computerValidMoves != []:
                # drawBoard(board)
                # printScore(board, playerTile, computerTile)
                #
                # input('Press enter to see the computer\'s move.')
                move = getRandomMove(board, computerTile)
                makeMove(board, computerTile, move[0], move[1])
            turn = 'player'


NUM_GAMES = 250
xWins = oWins = ties = 0
print('Welcome to Reversegam!')

playerTile, computerTile = ['X', 'O'] # enterPlayerTile()

for i in range(NUM_GAMES): #while True:
    finalBoard = playGame(playerTile, computerTile)

    # Display the final score.
    #d rawBoard(finalBoard)
    scores = getScoreOfBoard(finalBoard)
    print('X scored {} points. O scored {} points'.format(scores['X'], scores['O']))
    if scores[playerTile] > scores[computerTile]:
        xWins += 1 #print('You beat the computer by {} points! Congratulations!'.format(scores[playerTile] - scores[computerTile]))
    elif scores[playerTile] < scores[computerTile]:
        oWins += 1 #print('You lost. The computer beat you by {} points.'.format(scores[computerTile] - scores[playerTile]))
    else:
        ties += 1 #print('The game was a tie!')

    #print('Do you want to play again? (yes or no)')
    #if not input().lower().startswith('y'):
    #    break

print('X wins : {} ({}%)'.format(xWins, round(xWins / NUM_GAMES * 100, 1)))
print('O wins : {} ({}%)'.format(oWins, round(oWins / NUM_GAMES * 100, 1)))
print('Ties : {} ({}%)'.format(ties, round(ties / NUM_GAMES * 100, 1)))
