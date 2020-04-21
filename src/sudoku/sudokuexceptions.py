"""
Exceptions used in the sudoku module
"""


class ArgumentError(Exception):
    """
    Raised when an incorrect argument has been given
    """

    def __init__(self, *args):
        super().__init__(args)
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        print('Exception has ocurred: Argument Error')
        if self.message:
            return '{0}'.format(self.message)
        else:
            return 'ArgumentError has been raised'


class BoardError(Exception):
    """
    Raised when an incorrect board has been given
    """
    def __init__(self, *args):
        super().__init__(args)

        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        print('Exception has ocurred: Board Error')
        if self.message:
            return '{0}'.format(self.message)
        else:
            return 'BoardError has been raised'
