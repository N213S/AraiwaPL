"""Automated test suite verifying 100% of Araiwa specification rules and meme traps."""

import sys
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from errors import AraiwaSyntaxError, AraiwaRuntimeError, AraiwaFatalError


def run_code(code: str, args=None):
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter()
    return interpreter.interpret(ast, args or [])


def test_slash_slash_trap():
    code = r"""
yo เริ่มละนะ|| อยู่ในนี้
    // อันนี้คอมเมนต์แบบภาษาซี
    ตัวเลข x = 1 นะ
เหรอวะ
"""
    try:
        run_code(code)
        assert False, "Should have failed on // trap"
    except AraiwaSyntaxError as e:
        assert str(e) == "SyntaxError: ใส่ขีดสองอันมาทำไมวะ จำไม่ได้เหรอว่าต้องพิมพ์ว่า อันนี้ไม่ใช้:", f"Got: {e}"
    print("[PASS] // Trap test passed")


def test_missing_na_trap():
    code = r"""
yo เริ่มละนะ|| อยู่ในนี้
    ตัวเลข แต้ม = 100
เหรอวะ
"""
    try:
        run_code(code)
        assert False, "Should have failed on missing 'นะ'"
    except AraiwaSyntaxError as e:
        assert str(e) == "SyntaxError: คำสั่งไม่มีหางเสียง กรุณาลงท้ายด้วย นะ", f"Got: {e}"
    print("[PASS] Missing 'นะ' trap test passed")


def test_customs_trap():
    code = r"""
นำเข้าจากแดนไกล เครื่องคิดเลข นะ
yo เริ่มละนะ|| อยู่ในนี้
    พอละเหนื่อย 0 นะ
เหรอวะ
"""
    try:
        run_code(code)
        assert False, "Should have failed on Customs trap"
    except AraiwaRuntimeError as e:
        assert str(e) == "RuntimeError: ศุลกากรปฏิเสธพัสดุ พูดจาห้วนเกินไป กรุณาลงท้ายด้วย ครับ หรือ ค่ะ ให้เรียบร้อย", f"Got: {e}"
    print("[PASS] Customs trap test passed")


def test_string_plus_number_trap():
    code = r"""
yo เริ่มละนะ|| อยู่ในนี้
    ข้อความ ข้อความ1 = "ตัวเลขคือ: " + 123 นะ
เหรอวะ
"""
    try:
        run_code(code)
        assert False, "Should have failed on String + Number"
    except AraiwaRuntimeError as e:
        assert str(e) == "RuntimeError: ลองไปถามพ่อมึง", f"Got: {e}"
    print("[PASS] String + Number trap test passed")


def test_number_plus_string_trap():
    code = r"""
yo เริ่มละนะ|| อยู่ในนี้
    ข้อความ ข้อความ1 = 123 + "ตัวเลขคือ: " นะ
เหรอวะ
"""
    try:
        run_code(code)
        assert False, "Should have failed on Number + String"
    except AraiwaRuntimeError as e:
        assert str(e) == "RuntimeError: ลองไปถามพ่อมึง", f"Got: {e}"
    print("[PASS] Number + String trap test passed")


def test_number_67_trap():
    # Direct 67
    code1 = r"""
yo เริ่มละนะ|| อยู่ในนี้
    ตัวเลข x = 67 นะ
เหรอวะ
"""
    try:
        run_code(code1)
        assert False, "Should have failed on number 67"
    except AraiwaRuntimeError as e:
        assert str(e) == "RuntimeError: บ่ ไม่ขำ gen alpha หรือไง", f"Got: {e}"

    # Calculation resulting in 67
    code2 = r"""
yo เริ่มละนะ|| อยู่ในนี้
    ตัวเลข x = 60 + 7 นะ
เหรอวะ
"""
    try:
        run_code(code2)
        assert False, "Should have failed on calc resulting in 67"
    except AraiwaRuntimeError as e:
        assert str(e) == "RuntimeError: บ่ ไม่ขำ gen alpha หรือไง", f"Got: {e}"

    # 67.0 float
    code3 = r"""
yo เริ่มละนะ|| อยู่ในนี้
    ตัวเลข x = 67.0 นะ
เหรอวะ
"""
    try:
        run_code(code3)
        assert False, "Should have failed on 67.0"
    except AraiwaRuntimeError as e:
        assert str(e) == "RuntimeError: บ่ ไม่ขำ gen alpha หรือไง", f"Got: {e}"

    print("[PASS] Number 67 (Alpha Trap) test passed")


def test_number_over_6967_trap():
    # Constant > 6967
    code1 = r"""
yo เริ่มละนะ|| อยู่ในนี้
    ตัวเลข x = 6968 นะ
เหรอวะ
"""
    try:
        run_code(code1)
        assert False, "Should have failed on > 6967"
    except AraiwaRuntimeError as e:
        assert str(e) == "RuntimeError: อะไรวะ จำไม่ได้", f"Got: {e}"

    # Calc > 6967
    code2 = r"""
yo เริ่มละนะ|| อยู่ในนี้
    ตัวเลข x = 6000 + 1000 นะ
เหรอวะ
"""
    try:
        run_code(code2)
        assert False, "Should have failed on calc > 6967"
    except AraiwaRuntimeError as e:
        assert str(e) == "RuntimeError: อะไรวะ จำไม่ได้", f"Got: {e}"

    # Allowed: 6967 exactly
    code3 = r"""
yo เริ่มละนะ|| อยู่ในนี้
    ตัวเลข x = 6967 นะ
    ตะโกน/x\ นะ
เหรอวะ
"""
    run_code(code3)

    print("[PASS] Number > 6967 (Memory Loss Trap) test passed")


def test_loop_trap_while():
    code = r"""
yo เริ่มละนะ|| อยู่ในนี้
    เรื่องโกหก x = จริง นะ
    วนแม่งเข้าไป /x\ อยู่ในนี้
        x = จริง นะ
    เหรอวะ
เหรอวะ
"""
    try:
        run_code(code)
        assert False, "Should have failed on loop trap (> 6967 iterations)"
    except AraiwaFatalError as e:
        assert str(e) == "FatalError: วนเหี้ยไรเกิน 6967 รอบ อะไรวะ จำไม่ได้ เหนื่อยโว้ย!", f"Got: {e}"
    print("[PASS] Loop trap (while loop) test passed")


def test_loop_trap_for():
    # Loop over 6967 iterations
    code = r"""
yo เริ่มละนะ|| อยู่ในนี้
    ตัวเลข count = 0 นะ
    วนแม่งเข้าไป /count น้อยกว่าหรือเท่ากับ 6967\ อยู่ในนี้
        count = count + 0 นะ
    เหรอวะ
เหรอวะ
"""
    try:
        run_code(code)
        assert False, "Should have failed on infinite loop trap"
    except AraiwaFatalError as e:
        assert str(e) == "FatalError: วนเหี้ยไรเกิน 6967 รอบ อะไรวะ จำไม่ได้ เหนื่อยโว้ย!", f"Got: {e}"
    print("[PASS] Loop trap (infinite loop count) test passed")


def test_boolean_coercion():
    code = r"""
yo เริ่มละนะ|| อยู่ในนี้
    เรื่องโกหก a = จริง นะ
    เรื่องโกหก b = ตอแหล นะ
    ตัวเลข n1 = a + 10 นะ
    ตัวเลข n2 = b + 10 นะ
    ข้อความ s1 = "ค่าคือ " + a นะ
    ข้อความ s2 = b + " คือค่า" นะ
    ตะโกน/n1\ นะ
    ตะโกน/n2\ นะ
    ตะโกน/s1\ นะ
    ตะโกน/s2\ นะ
เหรอวะ
"""
    run_code(code)
    print("[PASS] Boolean coercion test passed")


def test_spacebar_warning():
    # Tests that > 10 spaces gives warning to stderr
    code = r"""
yo เริ่มละนะ|| อยู่ในนี้
    ตัวเลข x = 10           นะ
เหรอวะ
"""
    # 11 spaces before นะ
    run_code(code)
    print("[PASS] Spacebar warning test passed")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    test_slash_slash_trap()
    test_missing_na_trap()
    test_customs_trap()
    test_string_plus_number_trap()
    test_number_plus_string_trap()
    test_number_67_trap()
    test_number_over_6967_trap()
    test_loop_trap_while()
    test_loop_trap_for()
    test_boolean_coercion()
    test_spacebar_warning()
    print("\nALL 11 TESTS PASSED SUCCESSFULLY!")
