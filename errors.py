"""Araiwa Programming Language - Error Definitions.
Strict compliance with rules.txt specification.
"""

class AraiwaError(Exception):
    """Base exception for all Araiwa language errors."""
    def __init__(self, message: str, line: int = None, col: int = None):
        super().__init__(message)
        self.message = message
        self.line = line
        self.col = col

    def __str__(self) -> str:
        prefix = self.__class__.__name__.replace("Araiwa", "")
        return f"{prefix}: {self.message}"


class AraiwaSyntaxError(AraiwaError):
    """Raised for syntax errors such as missing 'นะ' or using '//'."""
    pass


class AraiwaRuntimeError(AraiwaError):
    """Raised for runtime exceptions such as type errors, customs check, or alpha trap."""
    pass


class AraiwaFatalError(AraiwaError):
    """Raised when a loop exceeds 6967 iterations."""
    pass


# Internal control flow signals
class ReturnSignal(Exception):
    """Signal used to return a value from entry point."""
    def __init__(self, value):
        self.value = value


class BreakSignal(Exception):
    """Signal used to break out of a loop."""
    pass


class ContinueSignal(Exception):
    """Signal used to continue to next iteration of a loop."""
    pass
