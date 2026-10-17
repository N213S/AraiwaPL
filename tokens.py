"""Araiwa Programming Language - Token Definitions."""

from enum import Enum, auto
from typing import Any


class TokenType(Enum):
    # Delimiters
    LPAREN = auto()       # / (open paren)
    RPAREN = auto()       # \ (close paren)
    LBRACE = auto()       # อยู่ในนี้
    RBRACE = auto()       # เหรอวะ
    PIPE = auto()         # |
    COMMA = auto()        # ,
    ASSIGN = auto()       # =

    # Operators
    PLUS = auto()         # +
    MINUS = auto()        # -
    STAR = auto()         # *
    SLASH = auto()        # / (division)
    CONCAT = auto()       # ฿ (string concatenation)
    EQ = auto()           # == หรือ เท่ากับ
    NEQ = auto()          # != หรือ ไม่เท่ากับ
    GTE = auto()          # >= หรือ มากกว่าหรือเท่ากับ
    LTE = auto()          # <= หรือ น้อยกว่าหรือเท่ากับ
    GT = auto()           # > หรือ มากกว่า
    LT = auto()           # < หรือ น้อยกว่า

    # Keywords
    IMPORT = auto()       # นำเข้าจากแดนไกล
    KRUB = auto()         # ครับ
    KA = auto()           # ค่ะ
    ENTRY_POINT = auto()  # yo เริ่มละนะ
    TYPE_NUMBER = auto()  # ตัวเลข
    TYPE_STRING = auto()  # ข้อความ
    TYPE_BOOL = auto()    # เรื่องโกหก
    TRUE = auto()         # จริง
    FALSE = auto()        # ตอแหล
    IF = auto()           # ถ้า
    ELSE = auto()         # ช่างแม่ง
    WHILE = auto()        # วนแม่งเข้าไป
    FOR = auto()          # เอาตั้งแต่
    TO = auto()           # ไปจนถึง
    BREAK = auto()        # พอเหอะ
    CONTINUE = auto()     # ช่างมันรอบนี้
    PRINT = auto()        # ตะโกน
    INPUT = auto()        # ถาม / บอกมา
    RETURN = auto()       # พอละเหนื่อย
    TERMINATOR = auto()   # นะ

    # Literals
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()

    # Special
    NEWLINE = auto()
    EOF = auto()


class Token:
    """Represents a single lexical token in Araiwa."""
    def __init__(self, type_: TokenType, value: Any, line: int, col: int, leading_spaces: int = 0):
        self.type = type_
        self.value = value
        self.line = line
        self.col = col
        self.leading_spaces = leading_spaces

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {repr(self.value)}, line={self.line}, col={self.col}, spaces={self.leading_spaces})"
