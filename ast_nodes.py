"""Araiwa Programming Language - Abstract Syntax Tree (AST) Nodes."""

from typing import List, Optional, Any


class ASTNode:
    """Base class for all AST nodes."""
    def __init__(self, line: int = 0):
        self.line = line


class ProgramNode(ASTNode):
    def __init__(self, imports: List['ImportNode'], entry_point: Optional['EntryPointNode'], line: int = 0):
        super().__init__(line)
        self.imports = imports
        self.entry_point = entry_point


class ImportNode(ASTNode):
    def __init__(self, module_name: str, ending: str, line: int = 0):
        super().__init__(line)
        self.module_name = module_name
        self.ending = ending


class EntryPointNode(ASTNode):
    def __init__(self, params: List[str], body: List[ASTNode], line: int = 0):
        super().__init__(line)
        self.params = params
        self.body = body


class VarDeclNode(ASTNode):
    def __init__(self, var_type: str, name: str, init_expr: ASTNode, line: int = 0):
        super().__init__(line)
        self.var_type = var_type
        self.name = name
        self.init_expr = init_expr


class AssignNode(ASTNode):
    def __init__(self, name: str, expr: ASTNode, line: int = 0):
        super().__init__(line)
        self.name = name
        self.expr = expr


class PrintNode(ASTNode):
    def __init__(self, expr: ASTNode, line: int = 0):
        super().__init__(line)
        self.expr = expr


class ReturnNode(ASTNode):
    def __init__(self, expr: Optional[ASTNode], line: int = 0):
        super().__init__(line)
        self.expr = expr


class BreakNode(ASTNode):
    def __init__(self, line: int = 0):
        super().__init__(line)


class ContinueNode(ASTNode):
    def __init__(self, line: int = 0):
        super().__init__(line)


class IfNode(ASTNode):
    def __init__(self, condition: ASTNode, then_body: List[ASTNode], else_body: Optional[List[ASTNode]] = None, line: int = 0):
        super().__init__(line)
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body


class WhileNode(ASTNode):
    def __init__(self, condition: ASTNode, body: List[ASTNode], line: int = 0):
        super().__init__(line)
        self.condition = condition
        self.body = body


class ForNode(ASTNode):
    def __init__(self, var_name: str, start_expr: ASTNode, end_expr: ASTNode, body: List[ASTNode], line: int = 0):
        super().__init__(line)
        self.var_name = var_name
        self.start_expr = start_expr
        self.end_expr = end_expr
        self.body = body


class BinaryOpNode(ASTNode):
    def __init__(self, left: ASTNode, op: str, right: ASTNode, line: int = 0):
        super().__init__(line)
        self.left = left
        self.op = op
        self.right = right


class UnaryOpNode(ASTNode):
    def __init__(self, op: str, expr: ASTNode, line: int = 0):
        super().__init__(line)
        self.op = op
        self.expr = expr


class LiteralNode(ASTNode):
    def __init__(self, value: Any, val_type: str, line: int = 0):
        super().__init__(line)
        self.value = value
        self.val_type = val_type


class IdentifierNode(ASTNode):
    def __init__(self, name: str, line: int = 0):
        super().__init__(line)
        self.name = name


class InputNode(ASTNode):
    def __init__(self, prompt_expr: Optional[ASTNode] = None, line: int = 0):
        super().__init__(line)
        self.prompt_expr = prompt_expr

