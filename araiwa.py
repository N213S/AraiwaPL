"""Araiwa Programming Language - CLI Entry Point.
Usage:
    python araiwa.py <script.arw> [arg1 arg2 ...]
"""

import sys
from typing import List, Any
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from errors import AraiwaError, AraiwaSyntaxError, AraiwaRuntimeError, AraiwaFatalError


def parse_cli_arg(arg: str) -> Any:
    """Parses a command-line argument into int, float, or str."""
    # Check int
    try:
        return int(arg)
    except ValueError:
        pass
    # Check float
    try:
        return float(arg)
    except ValueError:
        pass
    # String
    return arg


def main():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    if hasattr(sys.stderr, "reconfigure"):
        try:
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass

    if len(sys.argv) < 2:
        print("วิธีใช้: python araiwa.py <ไฟล์.arw> [ข้อโต้แย้ง 1] [ข้อโต้แย้ง 2] ...")
        sys.exit(1)

    file_path = sys.argv[1]
    raw_args = sys.argv[2:]
    parsed_args: List[Any] = [parse_cli_arg(a) for a in raw_args]

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
    except FileNotFoundError:
        sys.stderr.write(f"ข้อผิดพลาด: หาไฟล์ '{file_path}' ไม่พบ\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"ข้อผิดพลาดในการอ่านไฟล์: {e}\n")
        sys.exit(1)

    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()

        interpreter = Interpreter()
        exit_code = interpreter.interpret(ast, parsed_args)

        if isinstance(exit_code, int):
            sys.exit(exit_code)
        sys.exit(0)

    except (AraiwaSyntaxError, AraiwaRuntimeError, AraiwaFatalError) as e:
        sys.stderr.write(f"{e}\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"เกิดข้อผิดพลาดที่ไม่คาดคิด: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
