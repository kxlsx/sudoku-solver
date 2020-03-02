import sudokuboards as sb
import performance_test as perf

#char meaning the spot is empty 
emp = sb.emp

#the constMarker is for constant values that CANNOT be changed by the algorithm
constMarker = '$'

#main 
def sudokuSolve(board):

    #general checks if the board is valid for sudoku
    if len(board) % 3 != 0 or len(board) == 0:
        raise Exception("Board's size must be a positive multiple of 3")
    elif not(isBoardSquare(board)):
        raise Exception("Board's row count and row length must be uniform")

    board = markConstants(board)

    maxBoardIndex = len(board) - 1
    maxBoardRange = len(board) + 1

    possibleNums = tuple([str(i)
                     for i in range(1, maxBoardRange)])

    rowI = elementI = 0
    while True:
        
        horizontals = pullNumHorizontals(board)
        verticals = pullNumVerticals(board)
        squares = pullNumSquares(board)

        #if it isn't taken by a constant num
        if board[rowI][elementI] == emp or board[rowI][elementI] in possibleNums:

            #if it had already reached 9 before and it cannot increment further
            if board[rowI][elementI] == possibleNums[-1]:
                
                #reset the spot
                board[rowI][elementI] = emp

                #backtrack to the last available spot
                newCoords = bactrackCoordinates(rowI,elementI,board)
                if newCoords == None:

                    #the board cannot be solved
                    return

                rowI     = newCoords[0]
                elementI = newCoords[1]

            else:
                
                #go through all nums <the current one + 1; 9>
                for num in range(currentNumIncremented(rowI, elementI, board), maxBoardRange):
                    
                    #if the num isn't already on the horizontal or vertical line or in a square
                    if ((str(num) not in horizontals[rowI])
                    and (str(num) not in verticals[elementI])
                    and (str(num) not in squares[squareNum(rowI, elementI, len(board))])):

                        #set the first available num on the spot
                        board[rowI][elementI] = str(num)

                        #go forward a spot
                        newCoords = forwardCoordinates(rowI, elementI, maxBoardIndex)
                        if newCoords == None:

                            #final return (with the markers deleted for good measure)
                            return removeConstantMarks(board)

                        rowI     = newCoords[0]
                        elementI = newCoords[1]

                        break
                    
                    #if none of the spots are available 
                    elif (num == maxBoardRange - 1):

                        #reset the spot
                        board[rowI][elementI] = emp

                        #backtrack to the last available spot
                        newCoords = bactrackCoordinates(rowI,elementI,board)
                        if newCoords == None:

                            #the board cannot be solved
                            return

                        rowI     = newCoords[0]
                        elementI = newCoords[1]

        #if it's a constant num
        else:
            
            #go forward a spot
            newCoords = forwardCoordinates(rowI, elementI, maxBoardIndex)
            if newCoords == None:

                #final return (with the markers deleted for good measure)
                return removeConstantMarks(board)

            rowI     = newCoords[0]
            elementI = newCoords[1]


#returns a tuple of the next coordinates on the board (0 = rowI, 1 = elementI)
def forwardCoordinates(rowI, elementI, maxBoardIndex):

    #go to the next spot (if it's the last one, go down a row)
    elementI += 1
    if elementI > maxBoardIndex:
        elementI = 0
        rowI += 1

        #if it tries to go past the last item on the board
        if rowI > maxBoardIndex:
            return 

    return (rowI, elementI)

#returns a tuple of the last, previous, available coordinates (0 = rowI, 1 = elementI)
def bactrackCoordinates(rowI, elementI, board):

    maxBoardIndex = len(board) - 1

    #go back a spot (if it's the first one, go up a row)
    elementI -= 1
    if elementI < 0:
        rowI -= 1

        #if it tried to backtrack from the first spot
        if rowI < 0:
            return

        #it goes to the last spot of the previous row (it moves through the board like a snake)
        else:
            elementI = maxBoardIndex
                                               
    #while the current element it's checking is a constant
    #DOESN'T WORK PROPERLY i.e. doesn't work at all
    #UPDATE: i think it does now
    while '$' in board[rowI][elementI]:

        elementI -= 1
        if elementI < 0:
            rowI -= 1

            #if it tried to backtrack from the first spot
            if rowI < 0:
                return

            #it goes to the last spot of the previous row (it moves through the board like a snake)
            else:
                elementI = maxBoardIndex
    
    return (rowI, elementI)


#it's to set the lower bound to check for nums
def currentNumIncremented(rowI, elementI, board):

    if board[rowI][elementI] == emp:

        return 1

    elif board[rowI][elementI] == str(len(board)):

        return int(board[rowI][elementI])

    else:

        return int(board[rowI][elementI]) + 1

#returns the square's index (check pullNumSquares), in which are the given coordinates, number (currently works only with board 9x9)
def squareNum(rowI, elementI, boardLen):

    squareSize = int(boardLen / 3)
    squareMaxYs = tuple(filter(lambda x: x % 3 == 0, range(3, boardLen + 1)))
    squareMaxXs = tuple(filter(lambda x: x % squareSize == 0, range(squareSize, boardLen + 1)))

    base = 0
    for maxY in squareMaxYs:

        if rowI < maxY:
            
            mod = 0
            for maxX in squareMaxXs:

                if elementI < maxX:
                    return base + mod

                mod += squareSize

        base+=1

#returns all nums in corresponding horizontal lines 
def pullNumHorizontals(board):
    
    #pretty much copies the board without blank spaces and const markers
    horizontals = [{element.replace(constMarker, '')
                    for element in row
                    if element != emp}
                   for row in board]

    return horizontals

#returns all nums in corresponding vertical lines 
def pullNumVerticals(board):

    #empty list the same size as the board but filled with empty lists|
    verticals = [set()
                 for row in board]

    for elNum in range(len(board)):
        for rowNum in range(len(board)):
            #adds only nums to save time
            if board[rowNum][elNum] != emp:
                verticals[elNum].add(board[rowNum][elNum].replace(constMarker, ''))

    return verticals

#returns all nums in corresponding squares (3x3) 
def pullNumSquares(board):

    squareSize = int(len(board) / 3)
    squareY = 3
    squareX = squareSize

    #empty list the same size as the board but filled with empty sets
    squares = [set()
               for row in board]

    for squareNum in range(len(board)):
        for y in range(squareY - 3, squareY):
            for x in range(squareX - squareSize, squareX):
                #adds only nums to save time
                if board[x][y] != emp:
                    squares[squareNum].add(board[x][y].replace(constMarker, ''))

        squareX += squareSize
        if squareX > len(board):
            squareX = int(len(board)/3)
            squareY += 3

    return squares


#checks whether the board's length is the same as each row's length 
def isBoardSquare(board):

    try:

        for row in board:
           if len(board) != len(row):
                return False

        return True

    except:
        raise Exception('Board must be two-dimensional')


#returns a board with the nums coming pre-set marked with constMarker
def markConstants(board):
    
    for row in board:
        for element in row:
            if element != emp:
                board[board.index(row)][row.index(element)] += constMarker

    return board

#returns a board with the constMarkers removed if i'll ever need it
def removeConstantMarks(board):

    for row in board:
        for element in row:
            if element != emp:
                board[board.index(row)][row.index(element)] = board[board.index(row)][row.index(element)].replace(constMarker, '')

    return board

def printBoard(*boards, empty_spot_char='-'):

    i = 0
    for board in boards:

        if i != 0:
            print()
        
        if board == None:
            return None

        for row in board:
            for element in row:
                if not(element):
                    print(empty_spot_char, end='')
                print(element.replace(constMarker,'') + '  ', end='')
            print()
            
        i+=1
