"""Araiwa Programming Language - Parser.
Parses tokens into an Abstract Syntax Tree (AST).
"""

from typing import List, Optional
from tokens import TokenType, Token
from ast_nodes import (
    ASTNode,
    ProgramNode,
    ImportNode,
    EntryPointNode,
    VarDeclNode,
    AssignNode,
    PrintNode,
    ReturnNode,
    BreakNode,
    ContinueNode,
    IfNode,
    WhileNode,
    ForNode,
    BinaryOpNode,
    UnaryOpNode,
    LiteralNode,
    IdentifierNode,
    InputNode,
)
from errors import AraiwaSyntaxError, AraiwaRuntimeError


class Parser:
    """Parses a sequence of tokens into an AST."""
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def parse(self) -> ProgramNode:
        imports: List[ImportNode] = []
        entry_point: Optional[EntryPointNode] = None

        self._skip_newlines()

        # 1. Parse imports
        while self._check(TokenType.IMPORT):
            imports.append(self._parse_import())
            self._skip_newlines()

        # 2. Parse Entry Point
        if self._check(TokenType.ENTRY_POINT):
            entry_point = self._parse_entry_point()
        else:
            if not self._check(TokenType.EOF):
                cur = self._current()
                raise AraiwaSyntaxError(
                    f"ไม่พบจุดเริ่มต้นโปรแกรม (yo เริ่มละนะ) เจอ '{cur.value}' แทน",
                    line=cur.line,
                    col=cur.col,
                )

        self._skip_newlines()
        if not self._check(TokenType.EOF):
            cur = self._current()
            raise AraiwaSyntaxError(
                f"คำสั่งอยู่นอกจุดเริ่มต้นโปรแกรม: '{cur.value}'",
                line=cur.line,
                col=cur.col,
            )

        return ProgramNode(imports=imports, entry_point=entry_point)

    # -------------------------------------------------------------------------
    # Import Parsing
    # -------------------------------------------------------------------------
    def _parse_import(self) -> ImportNode:
        start_tok = self._consume(TokenType.IMPORT, "คาดหวังคำสั่ง นำเข้าจากแดนไกล")

        # Module name can be identifier or string or keywords
        if self._check(TokenType.IDENTIFIER) or self._check(TokenType.STRING):
            mod_tok = self._advance()
            mod_name = mod_tok.value
        elif not self._is_at_end() and self._current().type not in (TokenType.KRUB, TokenType.KA, TokenType.NEWLINE):
            mod_tok = self._advance()
            mod_name = str(mod_tok.value)
        else:
            raise AraiwaRuntimeError(
                "ศุลกากรปฏิเสธพัสดุ พูดจาห้วนเกินไป กรุณาลงท้ายด้วย ครับ หรือ ค่ะ ให้เรียบร้อย",
                line=start_tok.line,
                col=start_tok.col,
            )

        # Customs Rule: Must end with ครับ or ค่ะ
        if self._match(TokenType.KRUB):
            ending = "ครับ"
        elif self._match(TokenType.KA):
            ending = "ค่ะ"
        else:
            raise AraiwaRuntimeError(
                "ศุลกากรปฏิเสธพัสดุ พูดจาห้วนเกินไป กรุณาลงท้ายด้วย ครับ หรือ ค่ะ ให้เรียบร้อย",
                line=start_tok.line,
                col=start_tok.col,
            )

        return ImportNode(module_name=mod_name, ending=ending, line=start_tok.line)

    # -------------------------------------------------------------------------
    # Entry Point Parsing
    # -------------------------------------------------------------------------
    def _parse_entry_point(self) -> EntryPointNode:
        start_tok = self._consume(TokenType.ENTRY_POINT, "คาดหวัง yo เริ่มละนะ")

        # Arguments pipeline: |arg1, arg2|
        self._consume(TokenType.PIPE, "คาดหวังเครื่องหมาย | หลัง yo เริ่มละนะ")
        params: List[str] = []
        if not self._check(TokenType.PIPE):
            param_tok = self._consume(TokenType.IDENTIFIER, "คาดหวังชื่อตัวแปรรับเข้า")
            params.append(param_tok.value)
            while self._match(TokenType.COMMA):
                param_tok = self._consume(TokenType.IDENTIFIER, "คาดหวังชื่อตัวแปรรับเข้า")
                params.append(param_tok.value)
        self._consume(TokenType.PIPE, "คาดหวังเครื่องหมาย | ปิดรายการตัวแปรรับเข้า")

        # Open block: อยู่ในนี้
        self._consume(TokenType.LBRACE, "คาดหวัง อยู่ในนี้")
        body = self._parse_block_body()
        self._consume(TokenType.RBRACE, "คาดหวัง เหรอวะ ปิดบล็อกจุดเริ่มต้นโปรแกรม")

        return EntryPointNode(params=params, body=body, line=start_tok.line)

    # -------------------------------------------------------------------------
    # Block & Statement Parsing
    # -------------------------------------------------------------------------
    def _parse_block_body(self) -> List[ASTNode]:
        statements: List[ASTNode] = []
        while not self._check(TokenType.RBRACE) and not self._is_at_end():
            self._skip_newlines()
            if self._check(TokenType.RBRACE) or self._is_at_end():
                break
            stmt = self._parse_statement()
            statements.append(stmt)
            self._skip_newlines()
        return statements

    def _parse_statement(self) -> ASTNode:
        cur = self._current()

        # Variable Declaration: ตัวเลข / ข้อความ / เรื่องโกหก
        if cur.type in (TokenType.TYPE_NUMBER, TokenType.TYPE_STRING, TokenType.TYPE_BOOL):
            return self._parse_var_decl()

        # Print: ตะโกน
        if cur.type == TokenType.PRINT:
            return self._parse_print()

        # Return: พอละเหนื่อย
        if cur.type == TokenType.RETURN:
            return self._parse_return()

        # Break: พอเหอะ
        if cur.type == TokenType.BREAK:
            return self._parse_break()

        # Continue: ช่างมันรอบนี้
        if cur.type == TokenType.CONTINUE:
            return self._parse_continue()

        # If: ถ้า
        if cur.type == TokenType.IF:
            return self._parse_if()

        # While: วนแม่งเข้าไป
        if cur.type == TokenType.WHILE:
            return self._parse_while()

        # For: เอาตั้งแต่
        if cur.type == TokenType.FOR:
            return self._parse_for()

        # Input statement: ถาม / บอกมา
        if cur.type == TokenType.INPUT:
            return self._parse_input_statement()

        # Reassignment: <name> = <expr> นะ
        if cur.type == TokenType.IDENTIFIER and self._peek_type(1) == TokenType.ASSIGN:
            return self._parse_assignment()

        raise AraiwaSyntaxError(
            f"คำสั่งไม่ถูกต้องหรือไม่มีหางเสียง กรุณาลงท้ายด้วย นะ (พบ '{cur.value}')",
            line=cur.line,
            col=cur.col,
        )

    def _consume_terminator(self, context_line: int):
        """Enforces that statements end with 'นะ'."""
        if not self._match(TokenType.TERMINATOR):
            raise AraiwaSyntaxError(
                "คำสั่งไม่มีหางเสียง กรุณาลงท้ายด้วย นะ",
                line=context_line,
                col=self._previous().col,
            )

    def _parse_var_decl(self) -> VarDeclNode:
        type_tok = self._advance()
        name_tok = self._consume(TokenType.IDENTIFIER, "คาดหวังชื่อตัวแปร")
        self._consume(TokenType.ASSIGN, "คาดหวังเครื่องหมาย = ในการกำหนดค่าตัวแปร")
        init_expr = self._parse_expression()
        self._consume_terminator(type_tok.line)
        return VarDeclNode(
            var_type=type_tok.value,
            name=name_tok.value,
            init_expr=init_expr,
            line=type_tok.line,
        )

    def _parse_assignment(self) -> AssignNode:
        name_tok = self._advance()
        self._consume(TokenType.ASSIGN, "คาดหวังเครื่องหมาย =")
        expr = self._parse_expression()
        self._consume_terminator(name_tok.line)
        return AssignNode(name=name_tok.value, expr=expr, line=name_tok.line)

    def _parse_print(self) -> PrintNode:
        start_tok = self._advance()
        self._consume(TokenType.LPAREN, "คาดหวัง / เปิดหลังคำสั่ง ตะโกน")
        expr = self._parse_expression()
        self._consume(TokenType.RPAREN, "คาดหวัง \\ ปิดหลังคำสั่ง ตะโกน")
        self._consume_terminator(start_tok.line)
        return PrintNode(expr=expr, line=start_tok.line)

    def _parse_return(self) -> ReturnNode:
        start_tok = self._advance()
        expr: Optional[ASTNode] = None
        if not self._check(TokenType.TERMINATOR):
            expr = self._parse_expression()
        self._consume_terminator(start_tok.line)
        return ReturnNode(expr=expr, line=start_tok.line)

    def _parse_break(self) -> BreakNode:
        start_tok = self._advance()
        self._consume_terminator(start_tok.line)
        return BreakNode(line=start_tok.line)

    def _parse_continue(self) -> ContinueNode:
        start_tok = self._advance()
        self._consume_terminator(start_tok.line)
        return ContinueNode(line=start_tok.line)

    def _parse_input_statement(self) -> InputNode:
        node = self._parse_input_expr()
        self._consume_terminator(node.line)
        return node

    def _parse_input_expr(self) -> InputNode:
        start_tok = self._advance()
        self._consume(TokenType.LPAREN, "คาดหวัง / เปิดหลังคำสั่ง ถาม หรือ บอกมา")
        prompt_expr: Optional[ASTNode] = None
        if not self._check(TokenType.RPAREN):
            prompt_expr = self._parse_expression()
        self._consume(TokenType.RPAREN, "คาดหวัง \\ ปิดหลังคำสั่ง ถาม หรือ บอกมา")
        return InputNode(prompt_expr=prompt_expr, line=start_tok.line)

    def _parse_if(self) -> IfNode:
        start_tok = self._advance()
        self._consume(TokenType.LPAREN, "คาดหวัง / เปิดเงื่อนไขคำสั่ง ถ้า")
        condition = self._parse_expression()
        self._consume(TokenType.RPAREN, "คาดหวัง \\ ปิดเงื่อนไขคำสั่ง ถ้า")
        self._consume(TokenType.LBRACE, "คาดหวัง อยู่ในนี้ หลังเงื่อนไข ถ้า")

        then_body = self._parse_block_body()
        self._consume(TokenType.RBRACE, "คาดหวัง เหรอวะ ปิดบล็อก ถ้า")

        else_body: Optional[List[ASTNode]] = None
        # Check for else: ช่างแม่ง อยู่ในนี้ ... เหรอวะ
        if self._match(TokenType.ELSE):
            self._consume(TokenType.LBRACE, "คาดหวัง อยู่ในนี้ หลัง ช่างแม่ง")
            else_body = self._parse_block_body()
            self._consume(TokenType.RBRACE, "คาดหวัง เหรอวะ ปิดบล็อก ช่างแม่ง")

        return IfNode(
            condition=condition,
            then_body=then_body,
            else_body=else_body,
            line=start_tok.line,
        )

    def _parse_while(self) -> WhileNode:
        start_tok = self._advance()
        self._consume(TokenType.LPAREN, "คาดหวัง / เปิดเงื่อนไข วนแม่งเข้าไป")
        condition = self._parse_expression()
        self._consume(TokenType.RPAREN, "คาดหวัง \\ ปิดเงื่อนไข วนแม่งเข้าไป")
        self._consume(TokenType.LBRACE, "คาดหวัง อยู่ในนี้")
        body = self._parse_block_body()
        self._consume(TokenType.RBRACE, "คาดหวัง เหรอวะ ปิดบล็อก วนแม่งเข้าไป")
        return WhileNode(condition=condition, body=body, line=start_tok.line)

    def _parse_for(self) -> ForNode:
        start_tok = self._advance()
        self._consume(TokenType.LPAREN, "คาดหวัง / เปิดช่วงตัวเลข เอาตั้งแต่")

        # Optional "ตัวเลข" keyword
        if self._check(TokenType.TYPE_NUMBER):
            self._advance()

        var_tok = self._consume(TokenType.IDENTIFIER, "คาดหวังชื่อตัวแปรนับลูป")
        self._consume(TokenType.ASSIGN, "คาดหวัง = ในการกำหนดค่าเริ่มต้นลูป")
        start_expr = self._parse_expression()
        self._consume(TokenType.TO, "คาดหวัง ไปจนถึง คั่นช่วงตัวเลขใน For loop")
        end_expr = self._parse_expression()
        self._consume(TokenType.RPAREN, "คาดหวัง \\ ปิดช่วงตัวเลข เอาตั้งแต่")
        self._consume(TokenType.LBRACE, "คาดหวัง อยู่ในนี้")
        body = self._parse_block_body()
        self._consume(TokenType.RBRACE, "คาดหวัง เหรอวะ ปิดบล็อก เอาตั้งแต่")

        return ForNode(
            var_name=var_tok.value,
            start_expr=start_expr,
            end_expr=end_expr,
            body=body,
            line=start_tok.line,
        )

    # -------------------------------------------------------------------------
    # Expressions & Precedence Parsing
    # -------------------------------------------------------------------------
    def _parse_expression(self) -> ASTNode:
        return self._parse_comparison()

    def _parse_comparison(self) -> ASTNode:
        node = self._parse_concat()
        while self._check_any(
            TokenType.EQ,
            TokenType.NEQ,
            TokenType.GTE,
            TokenType.LTE,
            TokenType.GT,
            TokenType.LT,
        ):
            op_tok = self._advance()
            right = self._parse_concat()
            node = BinaryOpNode(left=node, op=op_tok.value, right=right, line=op_tok.line)
        return node

    def _parse_concat(self) -> ASTNode:
        node = self._parse_addition()
        while self._check(TokenType.CONCAT):
            op_tok = self._advance()
            right = self._parse_addition()
            node = BinaryOpNode(left=node, op="฿", right=right, line=op_tok.line)
        return node

    def _parse_addition(self) -> ASTNode:
        node = self._parse_multiplication()
        while self._check_any(TokenType.PLUS, TokenType.MINUS):
            op_tok = self._advance()
            right = self._parse_multiplication()
            node = BinaryOpNode(left=node, op=op_tok.value, right=right, line=op_tok.line)
        return node

    def _parse_multiplication(self) -> ASTNode:
        node = self._parse_unary()
        while self._check_any(TokenType.STAR, TokenType.SLASH):
            op_tok = self._advance()
            right = self._parse_unary()
            node = BinaryOpNode(left=node, op=op_tok.value, right=right, line=op_tok.line)
        return node

    def _parse_unary(self) -> ASTNode:
        if self._check(TokenType.MINUS):
            op_tok = self._advance()
            expr = self._parse_unary()
            return UnaryOpNode(op="-", expr=expr, line=op_tok.line)
        return self._parse_primary()

    def _parse_primary(self) -> ASTNode:
        cur = self._current()

        if cur.type == TokenType.NUMBER:
            tok = self._advance()
            return LiteralNode(value=tok.value, val_type="ตัวเลข", line=tok.line)

        if cur.type == TokenType.STRING:
            tok = self._advance()
            return LiteralNode(value=tok.value, val_type="ข้อความ", line=tok.line)

        if cur.type == TokenType.TRUE:
            tok = self._advance()
            return LiteralNode(value=True, val_type="เรื่องโกหก", line=tok.line)

        if cur.type == TokenType.FALSE:
            tok = self._advance()
            return LiteralNode(value=False, val_type="เรื่องโกหก", line=tok.line)

        if cur.type == TokenType.IDENTIFIER:
            tok = self._advance()
            return IdentifierNode(name=tok.value, line=tok.line)

        # Input expression: ถาม / บอกมา
        if cur.type == TokenType.INPUT:
            return self._parse_input_expr()

        # Parenthesized expression: / <expr> \
        if cur.type == TokenType.LPAREN:
            self._advance()  # Consume "/"
            expr = self._parse_expression()
            self._consume(TokenType.RPAREN, "คาดหวัง \\ ปิดวงเล็บ")
            return expr

        raise AraiwaSyntaxError(
            f"พบไวยากรณ์ที่ไม่ถูกต้องในนิพจน์: '{cur.value}'",
            line=cur.line,
            col=cur.col,
        )

    # -------------------------------------------------------------------------
    # Helper methods
    # -------------------------------------------------------------------------
    def _current(self) -> Token:
        if self._is_at_end():
            return self.tokens[-1]
        return self.tokens[self.pos]

    def _previous(self) -> Token:
        return self.tokens[self.pos - 1]

    def _peek_type(self, offset: int = 1) -> Optional[TokenType]:
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx].type
        return None

    def _is_at_end(self) -> bool:
        return self.pos >= len(self.tokens) or self.tokens[self.pos].type == TokenType.EOF

    def _check(self, type_: TokenType) -> bool:
        if self.pos >= len(self.tokens):
            return type_ == TokenType.EOF
        return self.tokens[self.pos].type == type_

    def _check_any(self, *types: TokenType) -> bool:
        if self.pos >= len(self.tokens):
            return TokenType.EOF in types
        return self.tokens[self.pos].type in types

    def _match(self, type_: TokenType) -> bool:
        if self._check(type_):
            self.pos += 1
            return True
        return False

    def _advance(self) -> Token:
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def _consume(self, type_: TokenType, error_msg: str) -> Token:
        if self._check(type_):
            return self._advance()
        cur = self._current()
        raise AraiwaSyntaxError(
            f"{error_msg} (พบ '{cur.value}')",
            line=cur.line,
            col=cur.col,
        )

    def _skip_newlines(self):
        while not self._is_at_end() and self.tokens[self.pos].type == TokenType.NEWLINE:
            self.pos += 1
