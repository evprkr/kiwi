# BASE ERROR CLASS
class Error:
    def __init__(self, pos_start, pos_end, error, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error = error
        self.details = details

    def as_string(self):
        error_msg = f"{self.error}: {self.details}"
        return error_msg

# LEXER/PARSER ERRORS
class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)

# RUNTIME ERRORS
