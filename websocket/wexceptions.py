

class MalformedMessage(Exception):

    def __init__(self):
        pass

    def __str__(self):
        return self.__class__.__name__
