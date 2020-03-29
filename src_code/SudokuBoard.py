"""
Module containing the class SudokuBoard used to store, solve or print the given board
"""

from copy import deepcopy
from requestsJson import get_data_from_json_site
from exceptions import *
import sudokuboards


class SudokuBoard:
    """
    Object used to store and solve a given board (can also print it to the console).
        
        Arguments:
            board {a tuple of lists} -- the tuple contains lists(rows), and the lists contain the actual elements
            or
            if board equals 'random' or 'rand' or 'r' it generates a random board from an api 
            (https://sugoku.herokuapp.com/board)
        
        Keyword Arguments:
            difficulty {string} -- easy, medium or hard; used to generate an appropriate board (default: {'N/A'} (interpreted as medium in random)
            emptySpotChar {char} -- char meaning the spot is empty in the given board (default: {'0'})
            constMarker {char} -- char used for marking spots the algorithm mustn't change (default: {'$'})
            correctWrongChars {bool} -- if True, every unknown char will be marked as emp
        
        Raises:
            ArgumentError: Incorrect difficulty ('easy', 'medium' or 'hard').
            ArgumentError: Incorrect board command (Try 'random', 'rand' or 'r' to generate a random board.
            ArgumentError: constMarker cannot be empty.
            ArgumentError: correctWrongChars must be boolean.
            BoardError: Board's size must be a multiple of 3.
            BoardError: Board's row count and row length must be uniform.
    """

    def __init__(self, board, difficulty='N/A', emptySpotChar='0', correctWrongChars=False, constMarker='$'):

        #char meaning the spot is empty
        self.__emp__ = emptySpotChar


        #is the given difficulty valid
        if difficulty.lower() in ('n/a', 'easy', 'medium', 'hard'):
            self.difficulty = difficulty
        else:
            raise ArgumentError("Incorrect difficulty ('N/A', 'easy', 'medium' or 'hard').")


        #check if they tried to generate a board
        try:
            #board is set to be random

            board = board.lower()

        except AttributeError:
            #board is a board

            #general checks if the board is valid for sudoku
            if len(board) % 3 != 0 or len(board) == 0:
                raise BoardError("Board's size must be a multiple of 3.")
            elif not(self.__is_board_square__(board)):
                raise BoardError("Board's row count and row length must be uniform.")

            self.board = board
        else:
            #generating random board

            if board in ('r', 'rand', 'random'):
                
                #N/A is interpreted as medium
                if difficulty.lower() == 'n/a':
                    self.difficulty = 'medium'

                self.board = self._generate_board_from_api_(self.difficulty)
            else:
                raise ArgumentError("Incorrect board command (Try 'random', 'rand' or 'r' to generate a random board).")
        finally:
            #board backup is used to reset the board if needed
            self.__boardBackup__ = deepcopy(self.board)


        #numbers that can be used in the board
        self.__possibleNums__ = tuple([str(i)
                                for i in range(1, len(self.board) + 1)])


        if not(isinstance(correctWrongChars, bool)):
            raise ArgumentError('correctWrongChars must be boolean.')
        
        self.__correctWrongChars__ = correctWrongChars


        #ensuring the board elements types
        self.board = self.__ensure_board_types__(self.board, self.__correctWrongChars__)
        self.__boardBackup__ = self.__ensure_board_types__(self.__boardBackup__, self.__correctWrongChars__)


        if constMarker == '':
            raise ArgumentError('constMarker cannot be empty.')
        
        #the constMarker is for constant values that CANNOT be changed by the algorithm
        self.__constMarker__ = constMarker



    def solve(self, copyBoard=False):
        """
        Solves the stored board.
        
        Keyword Arguments:
            copyBoard {bool} -- should the method work on a copied board and just return it (True)
            or just work with the original (False) (default: {False})
        
        Returns:
            {a tuple of lists} -- the solved board
            or
            {None} -- if the board is unsolvable
        """


        if copyBoard:
            brd = deepcopy(self.board)
        else:
            brd = self.board

        brd = self.__mark_constants__(brd)

        maxBoardIndex = len(brd) - 1
        maxBoardRange = len(brd) + 1

        

        rowI = elementI = 0
        while True:

            #if it isn't taken by a constant num
            if brd[rowI][elementI] == self.__emp__ or brd[rowI][elementI] in self.__possibleNums__:

                #if it had already reached 9 before and it cannot increment further
                if brd[rowI][elementI] == self.__possibleNums__[-1]:
                    
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
                    currentHorizontalNums = self.__get_horizontal_nums__(brd)[rowI]
                    currentVerticalNums = self.__get_vertical_nums__(brd)[elementI]
                    currentSquareNums = self.__get_nums_in_squares__(brd)[self.__get_square_num__(rowI, elementI, len(brd))]

                    bannedNums = currentHorizontalNums | currentVerticalNums | currentSquareNums

                    validNums = [num 
                                 for num in range(self.__get_current_num_incremented__(rowI, elementI, brd), maxBoardRange)
                                 if num not in bannedNums]

                    #go through all nums valid nums
                    for num in validNums:
                        
                        #if the num isn't already on the horizontal or vertical line or in a square
                        if str(num) not in bannedNums:

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
    
    def solve_step_by_step(self, copyBoard=False):
        """
        solve but it yields the board every time it places or removes a num.
        
        Keyword Arguments:
            copyBoard {bool} -- should the method work on a copied board and just return it (True)
            or just work with the original (False) (default: {False})
        
        Yields:
            {a tuple containing a tuple of lists and a bool} -- board in the current step with the information if it went forward(True) or backtracked(False)
            or
            {None} -- if the board is unsolvable
        """


        if copyBoard:
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
            
            #if it isn't taken by a constant num
            if brd[rowI][elementI] == self.__emp__ or brd[rowI][elementI] in possibleNums:

                #if it had already reached 9 before and it cannot increment further
                if brd[rowI][elementI] == possibleNums[-1]:
                    
                    #reset the spot
                    brd[rowI][elementI] = self.__emp__
                    yield (self.__remove_constant_marks__(brd), False)

                    #backtrack to the last available spot
                    newCoords = self.__get_bactrack_coordinates__(rowI, elementI, brd)
                    if newCoords == None:

                        #the board cannot be solved
                        yield None
                        return

                    rowI     = newCoords[0]
                    elementI = newCoords[1]

                else:
                    
                    currentHorizontalNums = self.__get_horizontal_nums__(brd)[rowI]
                    currentVerticalNums = self.__get_vertical_nums__(brd)[elementI]
                    currentSquareNums = self.__get_nums_in_squares__(brd)[self.__get_square_num__(rowI, elementI, len(brd))]

                    bannedNums = currentHorizontalNums | currentVerticalNums | currentSquareNums

                    validNums = [num 
                                 for num in range(self.__get_current_num_incremented__(rowI, elementI, brd), maxBoardRange)
                                 if num not in bannedNums]

                    #go through all valid nums
                    for num in validNums:
                        
                        #if the num isn't already on the horizontal or vertical line or in a square
                        if str(num) not in bannedNums:

                            #set the first available num on the spot
                            brd[rowI][elementI] = str(num)
                            yield (self.__remove_constant_marks__(brd), True)

                            #go forward a spot
                            newCoords = self.__get_forward_coordinates__(rowI, elementI, maxBoardIndex)
                            if newCoords == None:

                                #board solved
                                return

                            rowI     = newCoords[0]
                            elementI = newCoords[1]

                            break
                        
                        #if none of the spots are available 
                        elif (num == maxBoardRange - 1):

                            #reset the spot
                            brd[rowI][elementI] = self.__emp__
                            yield (self.__remove_constant_marks__(brd), False)

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

                    #board solved
                    yield (self.__remove_constant_marks__(brd), False)
                    return

                rowI     = newCoords[0]
                elementI = newCoords[1]

    def print_board(self):
        """
        Prints the stored board to the console
        """

        self.__print_any_board__(self.board)

    def print_solving_step_by_step(self, copyBoard=False):
        """
        Prints every step (board) of the algorithm solving the board.
        
        Keyword Arguments:
            copyBoard {bool} -- should the method work on a copied board and just return it (True)
            or just work with the original (False) (default: {False})
        """

        board = self.board

        self.__print_any_board__(board)
        print('Going forward...')

        solveStepByStep = self.solve_step_by_step(copyBoard)

        while True:
            try:
                step  = next(solveStepByStep)
            except StopIteration:
                print('Done!')
                break
            else:
                try:
                    self.__print_any_board__(step[0])
                except TypeError:
                    print('No solution!')
                    break
                else:
                    if step[1]:
                        print('Went forward.')
                    else:
                        print('Went back.')
                    
                    print() 

    def reset_board(self):
        """
        Resets the board to the initial state
        
        Returns:
            {tuple of lists} -- board given while creating SudokuBoard
        """
        self.board = deepcopy(self.__boardBackup__)
        return self.board


    def _generate_board_from_api_(self, difficulty='medium'):
        """
        Generates a board (9x9) from berto's API (https://sugoku.herokuapp.com/board)
            His emptySpotChars are '0'!
        
    
        Keyword Arguments:
            difficulty {str} -- easy, medium or hard (default: {'medium'})
    
        Returns:
            {tuple of lists} -- board converted to my format (9 lists in a tuple, each containing 9 elements)
        """

        #https://github.com/berto/sugoku - thanks berto!
        boardGeneratorApiURL = 'https://sugoku.herokuapp.com/board'

        generatedBoard = get_data_from_json_site(boardGeneratorApiURL, params={'difficulty': difficulty})['board']

        return tuple(generatedBoard)

    def __print_any_board__(self, board):
        """
        Prints the given board.
        
        Arguments:
            board {tuple of lists} -- the tuple contains lists(rows), and the lists contain the actual elements

        If board is None it prints No solution
        """

        if board == None:
            print('No Solution')
          
        for row in board:
            i = 0
            for element in row:
                                
                pelement = element 

                if len(board) > 9:
                    if i == 0 and len(element) == 1:
                        pelement = ' ' + pelement

                try:
                    if ((len(element) == 1 and len(row[i + 1]) == 1) or 
                        (len(element) == 2 and len(row[i + 1]) == 1)):
                        gap = 2 * ' '
                    elif ((len(element) == 2 and len(row[i + 1]) == 2) or 
                          (len(element) == 1 and len(row[i + 1]) == 2)):
                        gap = ' '
                except IndexError:
                    gap = ''
                
                print(pelement.replace(self.__constMarker__,'') + gap, end='')

                i+=1
            print()


    def __get_forward_coordinates__(self, rowI, elementI, maxBoardIndex):
        """
        Returns the next coordinates (as a tuple) or None
    
        Arguments:
            rowI {int} -- index of the current row
            elementI {int} -- index of the current element
            maxBoardIndex {int} -- max index of the current board
        
        Returns:
            {tuple} -- next coordinates on the board (row index, element index)
            or
            {None} -- the board is solved (the algorithm tried to go past the last element of the board)
        """

        #go to the next spot (if it's the last one, go down a row)
        elementI += 1
        if elementI > maxBoardIndex:
            elementI = 0
            rowI += 1

            #if it tries to go past the last item on the board
            if rowI > maxBoardIndex:
                return 

        return (rowI, elementI)

    def __get_bactrack_coordinates__(self, rowI, elementI, board):
        """
        Returns the last available coordinates or None.

        Arguments:
            rowI {int} -- current row index
            elementI {int} -- current element index
            board {tuple of lists} -- current board
        
        Returns:
            {tuple} -- last available coordinates (row index, element index)
            or
            {None} -- the board is unsolvable (the algorithm tried to backtrack past the first element)
        """
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

    def __get_current_num_incremented__(self, rowI, elementI, board):
        """
        It's used to set the lower bound to check for nums
        
         Arguments:
            rowI {int} -- current row index
            elementI {int} -- current element index
            board {tuple of lists} -- current board
        
        Returns:
            {int} -- num placed in the current element + 1 or 1 (if the element is empty) or max num of the board (if the num is equal to the max num) 
        """

        if board[rowI][elementI] == self.__emp__:

            return 1

        elif board[rowI][elementI] == str(len(board)):

            return int(board[rowI][elementI])

        else:

            return int(board[rowI][elementI]) + 1

    def __get_square_num__(self, rowI, elementI, boardLen):
        """
        Returns the square's index, in which are the given coordinates. 
        Squares are marked horizontally starting at the leftmost corner, heading rightwards
            
        Arguments:
            rowI {int} -- index of the current row
            elementI {int} -- index of the current element
            boardLen {int} -- length of the board
            
        Returns:
            {int} -- index used to mark the squares in get_nums_in_squares
        """

        squareSize = int(boardLen / 3)
        squareMaxYs = tuple(filter(lambda x: x % 3 == 0, range(3, boardLen + 1)))
        squareMaxXs = tuple(filter(lambda x: x % squareSize == 0, range(squareSize, boardLen + 1)))

        index = 0
        for maxY in squareMaxYs:
            if rowI < maxY:
                for maxX in squareMaxXs:
                    if elementI < maxX:
                        return index
                    else:
                        index += 1
            else:
                index += 3

    def __get_horizontal_nums__(self, board):
        """
        Returns a list of nums in corresponding horizontal lines.
        
        Arguments:
            board {tuple of lists} -- current board
        
        Returns:
            {tuple of sets} -- tuple contains sets of nums in corresponding rows
        """

        #pretty much copies the board without blank spaces and const markers
        horizontals = [{element.replace(self.__constMarker__, '')
                        for element in row
                        if element != self.__emp__}
                    for row in board]

        return tuple(horizontals)

    def __get_vertical_nums__(self, board):
        """
        Returns a list of nums in corresponding vertical lines.
        
        Arguments:
            board {tuple of lists} -- current board
        
        Returns:
            {tuple of sets} -- tuple contains sets of nums in corresponding columns
        """

        #empty list the same size as the board but filled with empty lists|
        verticals = [set()
                    for row in board]

        for elNum in range(len(board)):
            for rowNum in range(len(board)):
                #adds only nums to save time
                if board[rowNum][elNum] != self.__emp__:
                    verticals[elNum].add(board[rowNum][elNum].replace(self.__constMarker__, ''))

        return tuple(verticals)

    def __get_nums_in_squares__(self, board):
        """
        Returns a list of nums in corresponding squares 
        (they're marked horizontally starting at the leftmost corner, heading rightwards). 
        
        Arguments:
            board {tuple of lists} -- current board
        
        Returns:
            {tuple of sets} -- tuple contains sets of nums in corresponding squares
        """
    
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
                    if board[y][x] != self.__emp__:
                        squares[squareNum].add(board[y][x].replace(self.__constMarker__, ''))

            squareX += squareSize
            if squareX > len(board):
                squareX = int(len(board)/3)
                squareY += 3

        return tuple(squares)


    def __is_board_square__(self, board):
        """
        Checks whether the board's length is the same as each row's length.
        
        Arguments:
            board {a tuple of lists} -- the tuple contains lists(rows), and the lists contain the actual elements
        
        Raises:
            BoardError: Board must be two-dimensional.
        
        Returns:
            {bool}
        """
        
        try:

            for row in board:
                if len(board) != len(row):
                    return False

            return True

        except:
            raise BoardError('Board must be two-dimensional.')

    def __mark_constants__(self, board):
        """
        Returns a board with the nums coming pre-set marked with constMarker.
        
        Arguments:
            board {a tuple of lists} -- the tuple contains lists(rows), and the lists contain the actual elements
        
        Returns:
            {tuple of lists} -- board but the nums in it were marked
        """

        for row in board:
            for element in row:
                if element != self.__emp__:
                    board[board.index(row)][row.index(element)] += self.__constMarker__

        return board

    def __remove_constant_marks__(self, board):
        """
        Returns a board with the constMarkers removed if i'll ever need it.
        
        Arguments:
            board {a tuple of lists} -- the tuple contains lists(rows), and the lists contain the actual elements
        
        Returns:
            {tuple of lists} -- board but the marked nums are unmarked 
        """

        for row in board:
            for element in row:
                if element != self.__emp__:
                    board[board.index(row)][row.index(element)] = board[board.index(row)][row.index(element)].replace(self.__constMarker__, '')

        return board

    def __ensure_board_types__(self, board, correctWrongChars=False):
        """
        Ensures the board and its contents contain correct types of elements, if the element isn't a num
        and isn't recognised as an empty char, it interprets it a empty char.
        
        Arguments:
            board {a tuple of lists} -- the tuple contains lists(rows), and the lists contain the actual elements
        
        Raises:
            BoardError: Unknown char in board. (if it encountered it while correctWrongChars is False)

        Returns:
            {a tuple of lists} -- corrected board
        """

        ensuredBoard = []
        rowI = 0
        elementI = 0
        for row in board:

            ensuredBoard.append(list(row))
            for _ in row:

                char = str(ensuredBoard[rowI][elementI])

                if char not in self.__possibleNums__ and char != self.__emp__:
                    if correctWrongChars:
                        char = self.__emp__
                    else:
                        raise BoardError('Unknown char in board')

                ensuredBoard[rowI][elementI] = char
                
                elementI += 1

            rowI +=1
            elementI = 0

        
        return tuple(ensuredBoard)