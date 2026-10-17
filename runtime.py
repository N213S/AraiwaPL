"""Araiwa Programming Language - Runtime Environment and Type Semantics."""

from typing import Dict, Any, Optional, Tuple
from errors import AraiwaRuntimeError


def check_number(val: Any) -> Any:
    """Enforces Araiwa forbidden number rules."""
    if isinstance(val, (int, float)) and not isinstance(val, bool):
        if val == 67:
            raise AraiwaRuntimeError("บ่ ไม่ขำ gen alpha หรือไง")
        if val > 6967:
            raise AraiwaRuntimeError("อะไรวะ จำไม่ได้")
    return val


def format_value(val: Any) -> str:
    """Formats an Araiwa runtime value for printing or concatenation."""
    if isinstance(val, bool):
        return "จริง" if val else "ตอแหล"
    if isinstance(val, float):
        if val.is_integer():
            return str(int(val))
        return str(val)
    if val is None:
        return ""
    return str(val)


class Scope:
    """Manages lexical scoping and variable bindings."""
    def __init__(self, parent: Optional['Scope'] = None):
        self.parent = parent
        self.variables: Dict[str, Tuple[Any, Optional[str]]] = {}

    def declare(self, name: str, value: Any, var_type: Optional[str] = None):
        self._validate_type(var_type, value)
        check_number(value)
        self.variables[name] = (value, var_type)

    def assign(self, name: str, value: Any):
        if name in self.variables:
            _, declared_type = self.variables[name]
            self._validate_type(declared_type, value)
            check_number(value)
            self.variables[name] = (value, declared_type)
            return

        if self.parent is not None:
            self.parent.assign(name, value)
            return

        raise AraiwaRuntimeError(f"ยังไม่ได้ประกาศตัวแปร '{name}' นะ")

    def lookup(self, name: str) -> Any:
        if name in self.variables:
            return self.variables[name][0]
        if self.parent is not None:
            return self.parent.lookup(name)
        raise AraiwaRuntimeError(f"ไม่พบตัวแปร '{name}' ในระบบนะ")

    def get_type(self, name: str) -> Optional[str]:
        if name in self.variables:
            return self.variables[name][1]
        if self.parent is not None:
            return self.parent.get_type(name)
        return None

    def _validate_type(self, declared_type: Optional[str], value: Any):
        if declared_type is None:
            return

        if declared_type == "ตัวเลข":
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise AraiwaRuntimeError(f"ชนิดข้อมูลไม่ถูกต้อง: คาดหวัง 'ตัวเลข' แต่ได้ {type(value).__name__}")
        elif declared_type == "ข้อความ":
            if not isinstance(value, str):
                raise AraiwaRuntimeError(f"ชนิดข้อมูลไม่ถูกต้อง: คาดหวัง 'ข้อความ' แต่ได้ {type(value).__name__}")
        elif declared_type == "เรื่องโกหก":
            if not isinstance(value, bool):
                raise AraiwaRuntimeError(f"ชนิดข้อมูลไม่ถูกต้อง: คาดหวัง 'เรื่องโกหก' (Boolean) แต่ได้ {type(value).__name__}")
