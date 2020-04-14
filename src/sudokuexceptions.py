class ArgumentError(Exception):
    """
    Raised when an incorrect argument has been given
    """

    def __init__(self, *args):
        
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__ (self):
        print('Exception has occured: Argument Error')
        if self.message:
            return '{0}'.format(self.message)
        else:
            return 'ArgumentError has been raised'


class BoardError(Exception):
    """
    Raised when an incorrect board has been given
    """

    def __init__(self, *args):
        
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__ (self):
        print('Exception has occured: Board Error')
        if self.message:
            return '{0}'.format(self.message)
        else:
            return 'BoardError has been raised'

