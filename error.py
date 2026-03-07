class SyntaxError(Exception):
    def __init__(self, lineno, message):
        super().__init__(f"Syntax error at line {lineno}: {message}")
        self.lineno = lineno
        self.message = message