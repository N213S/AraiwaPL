"""Araiwa Programming Language - Lexer / Tokenizer.
Handles Thai keyword tokenization, spacebar checking, comments, and syntax traps.
"""

import sys
import re
from typing import List, Optional
from tokens import TokenType, Token
from errors import AraiwaSyntaxError

# Keyword mappings sorted by length descending to match longest prefixes first
KEYWORDS = [
    ("yo เริ่มละนะ", TokenType.ENTRY_POINT),
    ("นำเข้าจากแดนไกล", TokenType.IMPORT),
    ("วนแม่งเข้าไป", TokenType.WHILE),
    ("เอาตั้งแต่", TokenType.FOR),
    ("ไปจนถึง", TokenType.TO),
    ("พอเหอะ", TokenType.BREAK),
    ("ช่างมันรอบนี้", TokenType.CONTINUE),
    ("ช่างแม่ง", TokenType.ELSE),
    ("อยู่ในนี้", TokenType.LBRACE),
    ("เหรอวะ", TokenType.RBRACE),
    ("ตะโกน", TokenType.PRINT),
    ("บอกมา", TokenType.INPUT),
    ("พอละเหนื่อย", TokenType.RETURN),
    ("มากกว่าหรือเท่ากับ", TokenType.GTE),
    ("น้อยกว่าหรือเท่ากับ", TokenType.LTE),
    ("มากกว่า", TokenType.GT),
    ("น้อยกว่า", TokenType.LT),
    ("เท่ากับ", TokenType.EQ),
    ("ไม่เท่ากับ", TokenType.NEQ),
    ("ตัวเลข", TokenType.TYPE_NUMBER),
    ("ข้อความ", TokenType.TYPE_STRING),
    ("เรื่องโกหก", TokenType.TYPE_BOOL),
    ("จริง", TokenType.TRUE),
    ("ตอแหล", TokenType.FALSE),
    ("ถาม", TokenType.INPUT),
    ("ถ้า", TokenType.IF),
    ("ครับ", TokenType.KRUB),
    ("ค่ะ", TokenType.KA),
    ("นะ", TokenType.TERMINATOR),
]

SYMBOLS = [
    ("==", TokenType.EQ),
    ("!=", TokenType.NEQ),
    (">=", TokenType.GTE),
    ("<=", TokenType.LTE),
    (">", TokenType.GT),
    ("<", TokenType.LT),
    ("+", TokenType.PLUS),
    ("-", TokenType.MINUS),
    ("*", TokenType.STAR),
    ("฿", TokenType.CONCAT),
    ("=", TokenType.ASSIGN),
    ("|", TokenType.PIPE),
    (",", TokenType.COMMA),
    ("\\", TokenType.RPAREN),
]

# Thai + English identifier regex pattern
IDENTIFIER_PATTERN = re.compile(r"^[a-zA-Z_\u0e01-\u0e5b][a-zA-Z0-9_\u0e01-\u0e5b]*")
IS_IDENT_CHAR = re.compile(r"^[a-zA-Z0-9_\u0e01-\u0e5b]")


class Lexer:
    """Scans Araiwa source code into tokens."""
    def __init__(self, source: str):
        self.source = source
        self.length = len(source)
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens: List[Token] = []

    def tokenize(self) -> List[Token]:
        last_non_ws_token: Optional[Token] = None
        consecutive_spaces = 0

        while self.pos < self.length:
            char = self.source[self.pos]

            # 1. Check for Trap Rule: "//"
            if self.source.startswith("//", self.pos):
                raise AraiwaSyntaxError(
                    "ใส่ขีดสองอันมาทำไมวะ จำไม่ได้เหรอว่าต้องพิมพ์ว่า อันนี้ไม่ใช้:",
                    line=self.line,
                    col=self.col,
                )

            # 2. Check for Single-line Comment: "อันนี้ไม่ใช้:"
            if self.source.startswith("อันนี้ไม่ใช้:", self.pos):
                self._skip_single_line_comment()
                consecutive_spaces = 0
                continue

            # 3. Check for Multi-line Comment: "อันนี้ไม่ใช้=\""
            if self.source.startswith("อันนี้ไม่ใช้=\"", self.pos):
                self._skip_multi_line_comment()
                consecutive_spaces = 0
                continue

            # 4. Handle Whitespace & Newlines
            if char == "\n":
                self.tokens.append(Token(TokenType.NEWLINE, "\n", self.line, self.col))
                self.pos += 1
                self.line += 1
                self.col = 1
                consecutive_spaces = 0
                continue
            elif char == "\r":
                self.pos += 1
                continue
            elif char == " ":
                consecutive_spaces += 1
                self.pos += 1
                self.col += 1
                continue
            elif char == "\t":
                self.pos += 1
                self.col += 4
                continue

            # 5. Check Keywords
            matched_keyword = False
            for kw, token_type in KEYWORDS:
                if self.source.startswith(kw, self.pos):
                    end_pos = self.pos + len(kw)
                    # For word keywords, check if followed by an identifier character
                    if end_pos < self.length and IS_IDENT_CHAR.match(self.source[end_pos]):
                        continue

                    leading_spaces = consecutive_spaces

                    if token_type == TokenType.TERMINATOR:
                        # Spacebar Linter Warning check
                        if leading_spaces > 10:
                            sys.stderr.write(
                                "[คำเตือน]: เว้นวรรคหาพ่อมึงเหรอ เคาะ Spacebar เยอะขนาดนี้แป้นพิมพ์มึงค้างเหรอวะ? (แต่ช่างแม่ง รันต่อให้ก็ได้)\n"
                            )
                        tok = Token(token_type, kw, self.line, self.col, leading_spaces=leading_spaces)
                        self.tokens.append(tok)
                        last_non_ws_token = tok
                        self._advance(len(kw))
                        matched_keyword = True
                        consecutive_spaces = 0
                        break

                    tok = Token(token_type, kw, self.line, self.col, leading_spaces=leading_spaces)
                    self.tokens.append(tok)
                    last_non_ws_token = tok
                    self._advance(len(kw))
                    matched_keyword = True
                    consecutive_spaces = 0
                    break

            if matched_keyword:
                continue

            # 6. Check Multi-character and Single-character Symbols
            matched_symbol = False
            for sym, token_type in SYMBOLS:
                if self.source.startswith(sym, self.pos):
                    tok = Token(token_type, sym, self.line, self.col, leading_spaces=consecutive_spaces)
                    self.tokens.append(tok)
                    last_non_ws_token = tok
                    self._advance(len(sym))
                    matched_symbol = True
                    consecutive_spaces = 0
                    break

            if matched_symbol:
                continue

            # 7. Check "/" (LPAREN vs SLASH / Division)
            if char == "/":
                # Disambiguate "/"
                # If preceding token is an operand (NUMBER, STRING, TRUE, FALSE, IDENTIFIER, RPAREN):
                # then it's division SLASH. Otherwise, it's open paren LPAREN.
                is_division = False
                if last_non_ws_token is not None:
                    if last_non_ws_token.type in (
                        TokenType.NUMBER,
                        TokenType.STRING,
                        TokenType.TRUE,
                        TokenType.FALSE,
                        TokenType.IDENTIFIER,
                        TokenType.RPAREN,
                    ):
                        is_division = True

                token_type = TokenType.SLASH if is_division else TokenType.LPAREN
                tok = Token(token_type, "/", self.line, self.col, leading_spaces=consecutive_spaces)
                self.tokens.append(tok)
                last_non_ws_token = tok
                self._advance(1)
                consecutive_spaces = 0
                continue

            # 8. Check String Literal
            if char == '"':
                tok = self._scan_string(consecutive_spaces)
                self.tokens.append(tok)
                last_non_ws_token = tok
                consecutive_spaces = 0
                continue

            # 9. Check Number Literal
            if char.isdigit():
                tok = self._scan_number(consecutive_spaces)
                self.tokens.append(tok)
                last_non_ws_token = tok
                consecutive_spaces = 0
                continue

            # 10. Check Identifier (Thai/Latin)
            match = IDENTIFIER_PATTERN.match(self.source[self.pos:])
            if match:
                ident = match.group(0)
                # Check if identifier ends with "นะ" without space (e.g. "ผู้เล่นนะ")
                if ident.endswith("นะ") and len(ident) > 2:
                    # Lookahead: is this at the end of statement/line or before a delimiter?
                    rest_pos = self.pos + len(ident)
                    is_at_statement_end = (
                        rest_pos >= self.length
                        or self.source[rest_pos] in ("\n", "\r")
                        or self.source.startswith("อันนี้ไม่ใช้:", rest_pos)
                    )
                    if is_at_statement_end:
                        # Split into identifier and trailing "นะ"
                        var_name = ident[:-2]
                        ident_tok = Token(
                            TokenType.IDENTIFIER, var_name, self.line, self.col, leading_spaces=consecutive_spaces
                        )
                        self.tokens.append(ident_tok)
                        self._advance(len(var_name))

                        term_tok = Token(TokenType.TERMINATOR, "นะ", self.line, self.col, leading_spaces=0)
                        self.tokens.append(term_tok)
                        last_non_ws_token = term_tok
                        self._advance(2)
                        consecutive_spaces = 0
                        continue

                tok = Token(TokenType.IDENTIFIER, ident, self.line, self.col, leading_spaces=consecutive_spaces)
                self.tokens.append(tok)
                last_non_ws_token = tok
                self._advance(len(ident))
                consecutive_spaces = 0
                continue

            # Unknown character
            raise AraiwaSyntaxError(
                f"ตัวอักษรเหี้ยไรวะ '{char}' (ไม่รู้จัก)",
                line=self.line,
                col=self.col,
            )

        self.tokens.append(Token(TokenType.EOF, "", self.line, self.col, leading_spaces=consecutive_spaces))
        return self.tokens

    def _advance(self, count: int = 1):
        self.pos += count
        self.col += count

    def _skip_single_line_comment(self):
        while self.pos < self.length and self.source[self.pos] != "\n":
            self.pos += 1
            self.col += 1

    def _skip_multi_line_comment(self):
        start_line = self.line
        start_col = self.col
        self._advance(len("อันนี้ไม่ใช้=\""))
        end_idx = self.source.find("\"=", self.pos)
        if end_idx == -1:
            raise AraiwaSyntaxError(
                "คอมเมนต์หลายบรรทัดยังไม่ได้ปิด \"=",
                line=start_line,
                col=start_col,
            )
        # Advance lines and cols
        comment_content = self.source[self.pos:end_idx]
        newlines = comment_content.count("\n")
        self.line += newlines
        if newlines > 0:
            last_nl = comment_content.rfind("\n")
            self.col = len(comment_content) - last_nl
        else:
            self.col += len(comment_content)

        self.pos = end_idx + 2
        self.col += 2

    def _scan_string(self, leading_spaces: int) -> Token:
        start_line = self.line
        start_col = self.col
        self._advance(1)  # Skip opening quote

        chars = []
        while self.pos < self.length:
            char = self.source[self.pos]
            if char == '"':
                self._advance(1)  # Skip closing quote
                return Token(
                    TokenType.STRING, "".join(chars), start_line, start_col, leading_spaces=leading_spaces
                )
            elif char == "\\":
                self._advance(1)
                if self.pos >= self.length:
                    break
                esc = self.source[self.pos]
                if esc == "n":
                    chars.append("\n")
                elif esc == "t":
                    chars.append("\t")
                elif esc == '"':
                    chars.append('"')
                elif esc == "\\":
                    chars.append("\\")
                else:
                    chars.append(esc)
                self._advance(1)
            elif char == "\n":
                chars.append("\n")
                self.pos += 1
                self.line += 1
                self.col = 1
            else:
                chars.append(char)
                self._advance(1)

        raise AraiwaSyntaxError("ข้อความยังไม่ปิดเครื่องหมายคำพูด", line=start_line, col=start_col)

    def _scan_number(self, leading_spaces: int) -> Token:
        start_line = self.line
        start_col = self.col
        start_pos = self.pos

        while self.pos < self.length and self.source[self.pos].isdigit():
            self._advance(1)

        if (
            self.pos < self.length
            and self.source[self.pos] == "."
            and (self.pos + 1 < self.length and self.source[self.pos + 1].isdigit())
        ):
            self._advance(1)  # Consume "."
            while self.pos < self.length and self.source[self.pos].isdigit():
                self._advance(1)
            num_str = self.source[start_pos:self.pos]
            num_val = float(num_str)
        else:
            num_str = self.source[start_pos:self.pos]
            num_val = int(num_str)

        return Token(TokenType.NUMBER, num_val, start_line, start_col, leading_spaces=leading_spaces)
