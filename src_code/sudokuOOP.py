import sudokuboards
from copy import deepcopy

#the object has an attribute 'board' meaning the given board and methods solve & print_board
class SudokuBoard:

    def __init__(self, board, emptySpotChar=sudokuboards.emp, constMarker='$'):

        self.board = board

        #general checks if the board is valid for sudoku
        if len(self.board) % 3 != 0 or len(self.board) == 0:
            raise Exception("Board's size must be a positive multiple of 3")
        elif not(self.__is_board_square__(self.board)):
            raise Exception("Board's row count and row length must be uniform")

        #char meaning the spot is empty
        self.__emp__ = emptySpotChar

        #the constMarker is for constant values that CANNOT be changed by the algorithm
        self.__constMarker__ = constMarker

    #solves the board 
    def solve(self, copy_board=False):

        if copy_board:
            brd = deepcopy(self.board)
        else:
            brd = self.board

        brd = self.__mark_constants__(brd)

        maxBoardIndex = len(brd) - 1
        maxBoardRange = len(brd) + 1

        possibleNums = tuple([str(i)
                        for i in range(1, maxBoardRange)])

        rowI = elementI = 0
        while True:
            
            horizontals = self.__get_horizontal_nums__(brd)
            verticals = self.__get_vertical_nums__(brd)
            squares = self.__get_nums_in_squares__(brd)

            #if it isn't taken by a constant num
            if brd[rowI][elementI] == self.__emp__ or brd[rowI][elementI] in possibleNums:

                #if it had already reached 9 before and it cannot increment further
                if brd[rowI][elementI] == possibleNums[-1]:
                    
                    #reset the spot
                    brd[rowI][elementI] = self.__emp__

                    #backtrack to the last available spot
                    newCoords = self.__get_bactrack_coordinates__(rowI, elementI, brd)
                    if newCoords == None:

                        #the board cannot be solved
                        return

                    rowI     = newCoords[0]
                    elementI = newCoords[1]

                else:
                    
                    #go through all nums <the current one + 1; 9>
                    for num in range(self.__get_current_num_incremented__(rowI, elementI, brd), maxBoardRange):
                        
                        #if the num isn't already on the horizontal or vertical line or in a square
                        if ((str(num) not in horizontals[rowI])
                        and (str(num) not in verticals[elementI])
                        and (str(num) not in squares[self.__get_square_num__(rowI, elementI, len(brd))])):

                            #set the first available num on the spot
                            brd[rowI][elementI] = str(num)

                            #go forward a spot
                            newCoords = self.__get_forward_coordinates__(rowI, elementI, maxBoardIndex)
                            if newCoords == None:

                                #final return (with the markers deleted for good measure)
                                return self.__remove_constant_marks__(brd)

                            rowI     = newCoords[0]
                            elementI = newCoords[1]

                            break
                        
                        #if none of the spots are available 
                        elif (num == maxBoardRange - 1):

                            #reset the spot
                            brd[rowI][elementI] = self.__emp__

                            #backtrack to the last available spot
                            newCoords = self.__get_bactrack_coordinates__(rowI, elementI, brd)
                            if newCoords == None:

                                #the board cannot be solved
                                return

                            rowI     = newCoords[0]
                            elementI = newCoords[1]

            #if it's a constant num
            else:
                
                #go forward a spot
                newCoords = self.__get_forward_coordinates__(rowI, elementI, maxBoardIndex)
                if newCoords == None:

                    #final return (with the markers deleted for good measure)
                    return self.__remove_constant_marks__(brd)

                rowI     = newCoords[0]
                elementI = newCoords[1]
    
    #prints the board to the console
    def print_board(self):

        board = self.board

        if board == None:
            print('No Solution')
          
        for row in board:
            for element in row:
                if not(element):
                    print(self.__emp__, end='')
                print(element.replace(self.__constMarker__,'') + '  ', end='')
            print()


    #returns a tuple of the next coordinates on the board (0 = rowI, 1 = elementI)
    def __get_forward_coordinates__(self, rowI, elementI, maxBoardIndex):

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
    def __get_bactrack_coordinates__(self, rowI, elementI, board):

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
    def __get_current_num_incremented__(self, rowI, elementI, board):

        if board[rowI][elementI] == self.__emp__:

            return 1

        elif board[rowI][elementI] == str(len(board)):

            return int(board[rowI][elementI])

        else:

            return int(board[rowI][elementI]) + 1

    #returns the square's index, in which are the given coordinates 
    #squares are marked vertically (left corner square is index 0, and the one below it is index 1)
    def __get_square_num__(self, rowI, elementI, boardLen):

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

    #returns a list of nums in corresponding horizontal lines 
    def __get_horizontal_nums__(self, board):
        
        #pretty much copies the board without blank spaces and const markers
        horizontals = [{element.replace(self.__constMarker__, '')
                        for element in row
                        if element != self.__emp__}
                    for row in board]

        return horizontals

    #returns a list of nums in corresponding vertical lines 
    def __get_vertical_nums__(self, board):

        #empty list the same size as the board but filled with empty lists|
        verticals = [set()
                    for row in board]

        for elNum in range(len(board)):
            for rowNum in range(len(board)):
                #adds only nums to save time
                if board[rowNum][elNum] != self.__emp__:
                    verticals[elNum].add(board[rowNum][elNum].replace(self.__constMarker__, ''))

        return verticals

    #returns a list of nums in corresponding(check explanation above get_square_num) squares (3x3) 
    def __get_nums_in_squares__(self, board):

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
                    if board[x][y] != self.__emp__:
                        squares[squareNum].add(board[x][y].replace(self.__constMarker__, ''))

            squareX += squareSize
            if squareX > len(board):
                squareX = int(len(board)/3)
                squareY += 3

        return squares


    #checks whether the board's length is the same as each row's length 
    def __is_board_square__(self, board):

        try:

            for row in board:
                if len(board) != len(row):
                    return False

            return True

        except:
            raise Exception('Board must be two-dimensional')


    #returns a board with the nums coming pre-set marked with constMarker
    def __mark_constants__(self, board):
        
        for row in board:
            for element in row:
                if element != self.__emp__:
                    board[board.index(row)][row.index(element)] += self.__constMarker__

        return board

    #returns a board with the constMarkers removed if i'll ever need it
    def __remove_constant_marks__(self, board):

        for row in board:
            for element in row:
                if element != self.__emp__:
                    board[board.index(row)][row.index(element)] = board[board.index(row)][row.index(element)].replace(self.__constMarker__, '')

        return board
