"""Araiwa Programming Language - Interpreter.
Executes the AST and handles scopes, operators, loops, and runtime traps.
"""

import sys
from typing import List, Any, Optional
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
from runtime import Scope, check_number, format_value
from errors import (
    AraiwaRuntimeError,
    AraiwaFatalError,
    ReturnSignal,
    BreakSignal,
    ContinueSignal,
)


class Interpreter:
    """Evaluates the Araiwa AST."""
    def __init__(self):
        self.global_scope = Scope()
        self.imported_modules: set = set()

    def interpret(self, program: ProgramNode, args: Optional[List[Any]] = None) -> Any:
        if args is None:
            args = []

        # 1. Process Imports
        for imp in program.imports:
            self._execute_import(imp)

        # 2. Execute Entry Point
        if program.entry_point is not None:
            return self._execute_entry_point(program.entry_point, args)

        return 0

    def _execute_import(self, node: ImportNode):
        # Customs rule: Must end with ครับ or ค่ะ
        if node.ending not in ("ครับ", "ค่ะ"):
            raise AraiwaRuntimeError(
                "ศุลกากรปฏิเสธพัสดุ พูดจาห้วนเกินไป กรุณาลงท้ายด้วย ครับ หรือ ค่ะ ให้เรียบร้อย",
                line=node.line,
            )
        self.imported_modules.add(node.module_name)

    def _execute_entry_point(self, node: EntryPointNode, args: List[Any]) -> Any:
        entry_scope = Scope(parent=self.global_scope)

        # Bind parameters
        for idx, param_name in enumerate(node.params):
            if idx < len(args):
                arg_val = args[idx]
                check_number(arg_val)
                entry_scope.declare(param_name, arg_val)
            else:
                entry_scope.declare(param_name, "")

        try:
            self._execute_block(node.body, entry_scope)
        except ReturnSignal as ret:
            return ret.value

        return 0

    def _execute_block(self, statements: List[ASTNode], scope: Scope):
        for stmt in statements:
            self._execute_statement(stmt, scope)

    def _execute_statement(self, stmt: ASTNode, scope: Scope):
        if isinstance(stmt, VarDeclNode):
            val = self._evaluate_expression(stmt.init_expr, scope, expected_type=stmt.var_type)
            check_number(val)
            scope.declare(stmt.name, val, stmt.var_type)

        elif isinstance(stmt, AssignNode):
            expected_type = scope.get_type(stmt.name)
            val = self._evaluate_expression(stmt.expr, scope, expected_type=expected_type)
            check_number(val)
            scope.assign(stmt.name, val)

        elif isinstance(stmt, PrintNode):
            val = self._evaluate_expression(stmt.expr, scope)
            print(format_value(val))

        elif isinstance(stmt, InputNode):
            self._evaluate_input(stmt, scope)

        elif isinstance(stmt, ReturnNode):
            val = 0
            if stmt.expr is not None:
                val = self._evaluate_expression(stmt.expr, scope)
                check_number(val)
            raise ReturnSignal(val)

        elif isinstance(stmt, BreakNode):
            raise BreakSignal()

        elif isinstance(stmt, ContinueNode):
            raise ContinueSignal()

        elif isinstance(stmt, IfNode):
            self._execute_if(stmt, scope)

        elif isinstance(stmt, WhileNode):
            self._execute_while(stmt, scope)

        elif isinstance(stmt, ForNode):
            self._execute_for(stmt, scope)

        else:
            raise AraiwaRuntimeError(f"ไม่รู้จักคำสั่ง: {type(stmt).__name__}", line=stmt.line)

    def _execute_if(self, node: IfNode, scope: Scope):
        cond_val = self._evaluate_expression(node.condition, scope)
        if self._is_truthy(cond_val):
            then_scope = Scope(parent=scope)
            self._execute_block(node.then_body, then_scope)
        elif node.else_body is not None:
            else_scope = Scope(parent=scope)
            self._execute_block(node.else_body, else_scope)

    def _execute_while(self, node: WhileNode, scope: Scope):
        loop_scope = Scope(parent=scope)
        iterations = 0

        while True:
            cond_val = self._evaluate_expression(node.condition, loop_scope)
            if not self._is_truthy(cond_val):
                break

            iterations += 1
            if iterations > 6967:
                raise AraiwaFatalError("วนเหี้ยไรเกิน 6967 รอบ อะไรวะ จำไม่ได้ เหนื่อยโว้ย!", line=node.line)

            try:
                body_scope = Scope(parent=loop_scope)
                self._execute_block(node.body, body_scope)
            except BreakSignal:
                break
            except ContinueSignal:
                continue

    def _execute_for(self, node: ForNode, scope: Scope):
        start_val = self._evaluate_expression(node.start_expr, scope)
        end_val = self._evaluate_expression(node.end_expr, scope)

        if not isinstance(start_val, (int, float)) or isinstance(start_val, bool):
            raise AraiwaRuntimeError("ค่าเริ่มต้นของ For Loop ต้องเป็นตัวเลขนะ", line=node.line)
        if not isinstance(end_val, (int, float)) or isinstance(end_val, bool):
            raise AraiwaRuntimeError("ค่าสิ้นสุดของ For Loop ต้องเป็นตัวเลขนะ", line=node.line)

        check_number(start_val)
        check_number(end_val)

        start_int = int(start_val)
        end_int = int(end_val)
        step = 1 if start_int <= end_int else -1

        loop_scope = Scope(parent=scope)
        loop_scope.declare(node.var_name, start_int, "ตัวเลข")

        iterations = 0
        current_i = start_int
        while (step > 0 and current_i <= end_int) or (step < 0 and current_i >= end_int):
            iterations += 1
            if iterations > 6967:
                raise AraiwaFatalError("วนเหี้ยไรเกิน 6967 รอบ อะไรวะ จำไม่ได้ เหนื่อยโว้ย!", line=node.line)

            check_number(current_i)
            loop_scope.assign(node.var_name, current_i)

            try:
                body_scope = Scope(parent=loop_scope)
                self._execute_block(node.body, body_scope)
            except BreakSignal:
                break
            except ContinueSignal:
                pass

            current_i += step

    def _evaluate_expression(self, expr: ASTNode, scope: Scope, expected_type: Optional[str] = None) -> Any:
        if isinstance(expr, LiteralNode):
            if expr.val_type == "ตัวเลข":
                check_number(expr.value)
            return expr.value

        if isinstance(expr, IdentifierNode):
            return scope.lookup(expr.name)

        if isinstance(expr, InputNode):
            return self._evaluate_input(expr, scope, expected_type=expected_type)

        if isinstance(expr, UnaryOpNode):
            val = self._evaluate_expression(expr.expr, scope)
            if expr.op == "-":
                if isinstance(val, bool):
                    val = 1 if val else 0
                if isinstance(val, (int, float)):
                    res = -val
                    return check_number(res)
                raise AraiwaRuntimeError("เอาข้อความมาติดลบไม่ได้นะ", line=expr.line)

        if isinstance(expr, BinaryOpNode):
            left = self._evaluate_expression(expr.left, scope)
            right = self._evaluate_expression(expr.right, scope)
            return self._evaluate_binary_op(left, expr.op, right, expr.line)

        raise AraiwaRuntimeError(f"ไม่รู้จักนิพจน์: {type(expr).__name__}", line=expr.line)

    def _evaluate_input(self, node: InputNode, scope: Scope, expected_type: Optional[str] = None) -> Any:
        prompt = ""
        if node.prompt_expr is not None:
            prompt_val = self._evaluate_expression(node.prompt_expr, scope)
            prompt = format_value(prompt_val)

        sys.stdout.write(prompt)
        sys.stdout.flush()

        try:
            line = sys.stdin.readline()
        except (KeyboardInterrupt, EOFError):
            line = ""

        if line is None:
            line = ""
        else:
            line = line.rstrip("\r\n")

        if expected_type == "ตัวเลข":
            try:
                if "." in line:
                    val = float(line)
                else:
                    val = int(line)
            except ValueError:
                raise AraiwaRuntimeError("ข้อมูลที่กรอกไม่ใช่ตัวเลขนะ", line=node.line)
            return check_number(val)

        if expected_type == "เรื่องโกหก":
            if line == "จริง":
                return True
            elif line == "ตอแหล":
                return False
            else:
                raise AraiwaRuntimeError("ข้อมูลที่กรอกไม่ใช่เรื่องโกหก (ต้องตอบ 'จริง' หรือ 'ตอแหล')", line=node.line)

        if expected_type == "ข้อความ":
            return line

        # Auto-detect if expected_type is None
        try:
            if "." in line:
                val = float(line)
            else:
                val = int(line)
            return check_number(val)
        except ValueError:
            return line

    def _evaluate_binary_op(self, left: Any, op: str, right: Any, line: int) -> Any:
        is_l_str = isinstance(left, str)
        is_r_str = isinstance(right, str)
        is_l_bool = isinstance(left, bool)
        is_r_bool = isinstance(right, bool)
        is_l_num = isinstance(left, (int, float)) and not is_l_bool
        is_r_num = isinstance(right, (int, float)) and not is_r_bool

        # ---------------------------------------------------------------------
        # String Concatenation Operator: ฿
        # ---------------------------------------------------------------------
        if op == "฿":
            return format_value(left) + format_value(right)

        # ---------------------------------------------------------------------
        # Addition Operator: +
        # ---------------------------------------------------------------------
        if op == "+":
            # Rule 1: Text + Number or Number + Text -> RuntimeError: ลองไปถามพ่อมึง
            if (is_l_str and is_r_num) or (is_l_num and is_r_str):
                raise AraiwaRuntimeError("ลองไปถามพ่อมึง", line=line)

            # Rule 2: Boolean + Number -> จริง=1, ตอแหล=0
            if is_l_bool and is_r_num:
                res = (1 if left else 0) + right
                return check_number(res)
            if is_l_num and is_r_bool:
                res = left + (1 if right else 0)
                return check_number(res)

            # Rule 3: Boolean + Text -> coerce boolean to "จริง"/"ตอแหล"
            if is_l_bool and is_r_str:
                return ("จริง" if left else "ตอแหล") + right
            if is_l_str and is_r_bool:
                return left + ("จริง" if right else "ตอแหล")

            # Boolean + Boolean
            if is_l_bool and is_r_bool:
                res = (1 if left else 0) + (1 if right else 0)
                return check_number(res)

            # Number + Number
            if is_l_num and is_r_num:
                res = left + right
                return check_number(res)

            # Text + Text
            if is_l_str and is_r_str:
                return left + right

        # ---------------------------------------------------------------------
        # Subtraction Operator: -
        # ---------------------------------------------------------------------
        if op == "-":
            if is_l_str or is_r_str:
                raise AraiwaRuntimeError("เอาข้อความมาลบกันไม่ได้นะ", line=line)
            l_val = (1 if left else 0) if is_l_bool else left
            r_val = (1 if right else 0) if is_r_bool else right
            res = l_val - r_val
            return check_number(res)

        # ---------------------------------------------------------------------
        # Multiplication Operator: *
        # ---------------------------------------------------------------------
        if op == "*":
            if is_l_str or is_r_str:
                raise AraiwaRuntimeError("เอาข้อความมาคูณกันไม่ได้นะ", line=line)
            l_val = (1 if left else 0) if is_l_bool else left
            r_val = (1 if right else 0) if is_r_bool else right
            res = l_val * r_val
            return check_number(res)

        # ---------------------------------------------------------------------
        # Division Operator: /
        # ---------------------------------------------------------------------
        if op == "/":
            if is_l_str or is_r_str:
                raise AraiwaRuntimeError("เอาข้อความมาหารกันไม่ได้นะ", line=line)
            l_val = (1 if left else 0) if is_l_bool else left
            r_val = (1 if right else 0) if is_r_bool else right
            if r_val == 0:
                raise AraiwaRuntimeError("หารด้วยศูนย์ไม่ได้นะ", line=line)
            if isinstance(l_val, int) and isinstance(r_val, int) and l_val % r_val == 0:
                res = l_val // r_val
            else:
                res = l_val / r_val
            return check_number(res)

        # ---------------------------------------------------------------------
        # Comparison Operators
        # ---------------------------------------------------------------------
        if op in ("==", "เท่ากับ"):
            l_val = (1 if left else 0) if is_l_bool and is_r_num else left
            r_val = (1 if right else 0) if is_r_bool and is_l_num else right
            return l_val == r_val

        if op in ("!=", "ไม่เท่ากับ"):
            l_val = (1 if left else 0) if is_l_bool and is_r_num else left
            r_val = (1 if right else 0) if is_r_bool and is_l_num else right
            return l_val != r_val

        # Order comparisons
        l_comp = (1 if left else 0) if is_l_bool else left
        r_comp = (1 if right else 0) if is_r_bool else right

        if op in (">", "มากกว่า"):
            return l_comp > r_comp
        if op in ("<", "น้อยกว่า"):
            return l_comp < r_comp
        if op in (">=", "มากกว่าหรือเท่ากับ"):
            return l_comp >= r_comp
        if op in ("<=", "น้อยกว่าหรือเท่ากับ"):
            return l_comp <= r_comp

        raise AraiwaRuntimeError(f"ไม่รู้จักตัวดำเนินการ '{op}'", line=line)

    def _is_truthy(self, val: Any) -> bool:
        if isinstance(val, bool):
            return val
        if isinstance(val, (int, float)):
            return val != 0
        if isinstance(val, str):
            return len(val) > 0
        return bool(val)
