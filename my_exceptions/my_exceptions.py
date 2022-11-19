class MyException(Exception):
    def __init__(self, msg, where):
        self.msg = msg
        self.where = where


class OpenException(Exception):
    def __init__(self, msg):
        self.msg = msg


class EmptyField(MyException):
    pass


class IncorrectFormat(MyException):
    pass


class IntervalsIntersection(Exception):
    pass


class StartLatestThenEnd(Exception):
    pass


class EndAndEnteredDateBothEmpty(Exception):
    pass
