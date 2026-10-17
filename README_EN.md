<div align="right">
  <a href="README.md"><img src="https://img.shields.io/badge/Language-🇹🇭_ไทย-grey?style=for-the-badge" alt="ภาษาไทย"></a>
  <a href="README_EN.md"><img src="https://img.shields.io/badge/Language-🇬🇧_English-D80027?style=for-the-badge" alt="English"></a>
</div>

# Araiwa Programming Language

> [!WARNING]
> **Content Warning & Disclaimer:**  
> - This project was created strictly for **entertainment, educational, and parody/satire purposes**.  
> - Error messages, linter warnings, and language rules contain **explicit language, profanity, and strong Thai slang** for comedic meme effect.  
> - Code and documentation for this project were developed with the assistance of **AI (Artificial Intelligence)**.  
> Viewer discretion is advised.

> **Version:** `v0.1 Pre-Alpha`  
> **Supported Extensions:** `.arw` or `.araiwa`  
> **Paradigm:** Imperative, Dynamically typed with meme-driven constraints  
> **System Requirements:** Python 3.8+ (Pure Standard Library, zero third-party dependencies)

---

## Table of Contents
1. [Language Overview](#language-overview)
2. [Architecture & Workflow](#architecture--workflow)
3. [Version Capabilities (v0.1)](#version-capabilities-v01)
4. [Strict Meme Rules & Traps](#strict-meme-rules--traps)
5. [Syntax & Statement Structure](#syntax--statement-structure)
6. [Usage Guide](#usage-guide)
7. [Real-World Examples](#real-world-examples)
8. [Project File Structure](#project-file-structure)

---

## Language Overview

**Araiwa (อะไรวะ - "What the heck?")** is an imperative programming language designed for humor, satire, and strict logic testing. The entire syntax is written in the Thai language blended with mathematical operators, featuring aggressive linter warnings and runtime traps that penalize unconventional coding behaviors—such as excessive spacebar presses, C-style comments, forbidden numbers, and runaway loops.

---

## Architecture & Workflow

The interpreter follows standard interpreter design, cleanly decoupled into modular components:

```
[ .arw Source Code ]
        │
        ▼
   [ Lexer / Tokenizer ] (lexer.py, tokens.py)
        │ - Scans Thai keywords and symbols
        │ - Counts spacebar presses before the "นะ" terminator
        │ - Disambiguates "/" (LPAREN vs division operator)
        │ - Detects forbidden "//" traps and parses comments
        ▼
     [ Tokens ]
        │
        ▼
   [ Parser ] (parser.py, ast_nodes.py)
        │ - Converts tokens into an Abstract Syntax Tree (AST)
        │ - Enforces operator precedence
        │ - Validates block boundaries (อยู่ในนี้ / เหรอวะ)
        │ - Enforces mandatory polite particle "นะ" termination
        ▼
    [ AST Tree ]
        │
        ▼
 [ Interpreter / Runtime ] (interpreter.py, runtime.py, errors.py)
        │ - Manages lexical variable scope
        │ - Evaluates arithmetic and string operations
        │ - Enforces type coercion and type validation
        │ - Tracks loop iterations for FatalError (> 6967 iterations)
        │ - Enforces forbidden numbers (Alpha Trap: 67, Memory Loss: > 6967)
        ▼
 [ Console Output / stdout, stderr ]
```

---

## Version Capabilities (v0.1)

### 1. Program Entry Point & Parameter Pipeline
- Every program requires a single entry point: `yo เริ่มละนะ|<params>| อยู่ในนี้ ... เหรอวะ`
- Arguments passed via CLI are bound directly to entry point parameters (e.g., `yo เริ่มละนะ|รอบ, ผู้เล่น|`).

### 2. Module Customs Rule
- Modules can be imported with: `นำเข้าจากแดนไกล <ModuleName> <ครับ or ค่ะ>`
- Strictly enforces Thai polite endings (`ครับ` or `ค่ะ`).

### 3. Data Types
- **`ตัวเลข` (Number):** Supports both integers and floating-point numbers.
- **`ข้อความ` (String):** Declared inside double quotes `"..."` supporting escape sequences (`\n`, `\t`, `\"`, `\\`).
- **`เรื่องโกหก` (Boolean):** Features two constants: `จริง` (True) and `ตอแหล` (False).

### 4. Delimiters & Symbols
- Open parenthesis `(` is `/`
- Close parenthesis `)` is `\`
- Open curly brace `{` is `อยู่ในนี้`
- Close curly brace `}` is `เหรอวะ`
- String concatenation operator is `฿` (Thai Baht currency symbol)

### 5. Control Flow
- **Conditional:** `ถ้า /<condition>\ อยู่ในนี้ ... เหรอวะ` and `เหรอวะ ช่างแม่ง อยู่ในนี้ ... เหรอวะ` (Else).
- **While Loop:** `วนแม่งเข้าไป /<condition>\ อยู่ในนี้ ... เหรอวะ`.
- **For Range Loop:** `เอาตั้งแต่ /ตัวเลข <var> = <start> ไปจนถึง <end>\ อยู่ในนี้ ... เหรอวะ` (Inclusive range, ascending or descending).
- **Loop Control:** `พอเหอะ นะ` (Break) and `ช่างมันรอบนี้ นะ` (Continue).

### 6. Output, Interactive Input & Return
- **Interactive Console Input (stdin):** `ถาม/<prompt>\` or `บอกมา/<prompt>\` (equivalent to Python's `input()` or C's `scanf`, with automatic type adaptation and Alpha Trap validation).
- **Standard Output:** `ตะโกน/<expression>\ นะ`
- **Return and exit:** `พอละเหนื่อย <expression> นะ`

---

## Strict Meme Rules & Traps

| Rule / Trap | Trigger Condition | Behavior / Exact Error Message |
| :--- | :--- | :--- |
| **Spacebar Linter Warning** | More than 10 spaces immediately preceding `นะ` | Prints warning to `stderr` but execution continues:<br>`[คำเตือน]: เว้นวรรคหาพ่อมึงเหรอ เคาะ Spacebar เยอะขนาดนี้แป้นพิมพ์มึงค้างเหรอวะ? (แต่ช่างแม่ง รันต่อให้ก็ได้)` |
| **Missing Polite Particle** | Statement missing mandatory `นะ` terminator | `SyntaxError: คำสั่งไม่มีหางเสียง กรุณาลงท้ายด้วย นะ` |
| **C-Style Comment Trap** | Token `//` encountered anywhere in code | `SyntaxError: ใส่ขีดสองอันมาทำไมวะ จำไม่ได้เหรอว่าต้องพิมพ์ว่า อันนี้ไม่ใช้:` |
| **Customs Inspection Trap** | `นำเข้าจากแดนไกล` not ending with `ครับ` or `ค่ะ` | `RuntimeError: ศุลกากรปฏิเสธพัสดุ พูดจาห้วนเกินไป กรุณาลงท้ายด้วย ครับ หรือ ค่ะ ให้เรียบร้อย` |
| **Cross-Type Addition Trap** | Adding `String + Number` or `Number + String` with `+` | `RuntimeError: ลองไปถามพ่อมึง`<br>*(String concatenation with numbers must use `฿`)* |
| **Boolean Coercion** | `Boolean + Number` or `Boolean + String` with `+` | `จริง` = 1, `ตอแหล` = 0 when added to numbers.<br>Coerced to `"จริง"` or `"ตอแหล"` when added to strings. |
| **Alpha Trap (Number 67)** | Any literal, assignment, or computation equals `67` or `67.0` | `RuntimeError: บ่ ไม่ขำ gen alpha หรือไง` |
| **Memory Loss Trap** | Any number exceeds `6967` | `RuntimeError: อะไรวะ จำไม่ได้`<br>*(Numbers greater than 6967 must be stored as "ข้อความ")* |
| **Loop Trap** | Any loop executes more than `6967` iterations | `FatalError: วนเหี้ยไรเกิน 6967 รอบ อะไรวะ จำไม่ได้ เหนื่อยโว้ย!` |

---

## Syntax & Statement Structure

### File Skeleton
```araiwa
นำเข้าจากแดนไกล จอแสดงผล ครับ
นำเข้าจากแดนไกล เครื่องคิดเลข ค่ะ

yo เริ่มละนะ|รอบ, ผู้เล่น| อยู่ในนี้
    <statements>*
เหรอวะ
```

### Variable Declaration & Assignment
```araiwa
ข้อความ ชื่อ = "สมชาย" นะ
ตัวเลข อายุ = 25 นะ
เรื่องโกหก โสด = จริง นะ

อายุ = 26 นะ
```

### Interactive Console Input (scanf / input)
```araiwa
อันนี้ไม่ใช้: String input
ข้อความ player_name = ถาม/"Enter your name: "\ นะ

อันนี้ไม่ใช้: Number input (automatically parses number and enforces Alpha Trap 67)
ตัวเลข guess = ถาม/"Guess a number (1-100): "\ นะ

อันนี้ไม่ใช้: "บอกมา" can be used interchangeably with "ถาม"
ตัวเลข score = บอกมา/"Enter score: "\ นะ
```

### String Concatenation with ฿
```araiwa
ข้อความ ข้อมูล = "ชื่อ: " ฿ ชื่อ ฿ " อายุ: " ฿ อายุ นะ
ตะโกน/ข้อมูล\ นะ
```

### Conditionals (If-Else)
```araiwa
ถ้า /อายุ มากกว่าหรือเท่ากับ 18\ อยู่ในนี้
    ตะโกน/"เป็นผู้ใหญ่แล้ว"\ นะ
เหรอวะ ช่างแม่ง อยู่ในนี้
    ตะโกน/"ยังเป็นเด็กอยู่"\ นะ
เหรอวะ
```

### Comparison Operators
Supports both standard symbols and Thai natural language keywords:
- `==` or `เท่ากับ`
- `!=` or `ไม่เท่ากับ`
- `>` or `มากกว่า`
- `<` or `น้อยกว่า`
- `>=` or `มากกว่าหรือเท่ากับ`
- `<=` or `น้อยกว่าหรือเท่ากับ`

### Loops
```araiwa
เอาตั้งแต่ /ตัวเลข i = 1 ไปจนถึง 5\ อยู่ในนี้
    ถ้า /i เท่ากับ 2\ อยู่ในนี้
        ช่างมันรอบนี้ นะ    อันนี้ไม่ใช้: Continue to next iteration
    เหรอวะ
    ถ้า /i เท่ากับ 4\ อยู่ในนี้
        พอเหอะ นะ          อันนี้ไม่ใช้: Break out of loop
    เหรอวะ
    ตะโกน/"รอบ: " ฿ i\ นะ
เหรอวะ
```

### Comments
```araiwa
อันนี้ไม่ใช้: Single-line comment ignoring rest of line

อันนี้ไม่ใช้="
Multi-line comment
ignoring everything between =" and "=
"=
```

---

## Usage Guide

### 1. Requirements
Python **3.8** or newer is required. Verify with:
```bash
python --version
```

### 2. Running an Araiwa Script
Run any `.arw` script via the CLI:
```bash
python araiwa.py <script.arw> [argument 1] [argument 2] ...
```

**Example:**
```bash
python araiwa.py test.arw 1 มหาเทพโปรแกรมเมอร์
```

**Output:**
```text
[คำเตือน]: เว้นวรรคหาพ่อมึงเหรอ เคาะ Spacebar เยอะขนาดนี้แป้นพิมพ์มึงค้างเหรอวะ? (แต่ช่างแม่ง รันต่อให้ก็ได้)
ยินดีต้อนรับผู้เล่น: มหาเทพโปรแกรมเมอร์
ผ่านเกณฑ์แล้ววะ
รอบปัจจุบัน: 1
รอบปัจจุบัน: 3
สถานะ + แต้ม = 101
```

### 3. Running Automated Traps Test Suite
Execute the comprehensive test suite verifying all 11 meme rules and edge cases:
```bash
python -X utf8 test_traps.py
```

Expected result:
```text
[PASS] // Trap test passed
[PASS] Missing 'นะ' trap test passed
[PASS] Customs trap test passed
[PASS] String + Number trap test passed
[PASS] Number + String trap test passed
[PASS] Number 67 (Alpha Trap) test passed
[PASS] Number > 6967 (Memory Loss Trap) test passed
[PASS] Loop trap (while loop) test passed
[PASS] Loop trap (infinite loop count) test passed
[PASS] Boolean coercion test passed
[PASS] Spacebar warning test passed

ALL 11 TESTS PASSED SUCCESSFULLY!
```

---

## Real-World Examples

### 1. Restaurant POS & Cashier System (`pos_cashier.arw`)
A complete restaurant point-of-sale checkout simulation demonstrating interactive ordering loops, running subtotal calculation, receipt printing, cash validation, and change computation:

- **Features:**
  - Interactive ordering menu utilizing `ถาม` for live user input
  - Dynamic item counting and order subtotal tracking
  - Full receipt generation
  - Cash payment validation (prompts for additional payment if cash is insufficient)
  - Change calculation with Alpha Trap (67) avoidance checks

**Run Command:**
```bash
python araiwa.py pos_cashier.arw
```

**Sample Output:**
```text
===============================================
 🍛 ยินดีต้อนรับสู่ระบบคิดเงินร้านอาหารตามสั่ง (POS) 
===============================================

--- เมนูอาหาร ---
1. กะเพราหมูกรอบไข่ดาว (70 บาท)
2. ข้าวผัดหมูโบราณ (50 บาท)
3. ต้มยำกุ้งน้ำข้น (120 บาท)
4. ชาไทยเย็นหวานเจี๊ยบ (30 บาท)
5. 💳 คิดเงิน / ชำระบิล
6. ❌ ยกเลิกและออกจากระบบ
👉 กรุณาเลือกรายการ (1-6): 1
สั่งกี่จานดี: 2
✅ เพิ่ม กะเพราหมูกรอบ 2 จาน (ยอดสะสม: 140 บาท)

--- เมนูอาหาร ---
...
👉 กรุณาเลือกรายการ (1-6): 5

================ ใบเสร็จรับเงิน ================
รวมจำนวนที่สั่งทั้งหมด: 2 รายการ
ยอดรวมทั้งสิ้น: 140 บาท
-----------------------------------------------
💵 รับเงินสดจากลูกค้า: 100
❌ เงินไม่พอเว้ย! ยังขาดอีก 40 บาท จ่ายเพิ่มมาเดี๋ยวนี้
💵 รับเงินสดจากลูกค้า: 200
💰 เงินทอน: 60 บาท
🎉 ชำระเงินเรียบร้อย ขอบใจที่มาอุดหนุน โอกาสหน้าเชิญใหม่นะไอ้สอง!
===============================================
```

---

### 2. Interactive Number Guessing Game (`guess_game.arw`)
A real-time number guessing game utilizing a `วนแม่งเข้าไป` loop and `ถาม` input to prompt the player for guesses, offering "too high" or "too low" hints until the correct answer is guessed:

**Run Command:**
```bash
python araiwa.py guess_game.arw
```

---

## Project File Structure

| File | Purpose |
| :--- | :--- |
| `araiwa.py` | CLI entry point parsing command-line arguments and executing scripts |
| `lexer.py` | Scanner/Tokenizer handling Thai keywords, whitespace counting, and `//` detection |
| `tokens.py` | `TokenType` enum and `Token` data structure |
| `parser.py` | Recursive descent parser generating the AST and enforcing syntax rules |
| `ast_nodes.py` | AST node classes for expressions, statements, and blocks |
| `runtime.py` | Lexical `Scope`, value formatting, and `check_number` trap validator |
| `interpreter.py` | Tree-walking AST evaluator with loop iteration tracking |
| `errors.py` | Custom language exceptions matching exact rules.txt output strings |
| `test.arw` | Official reference test suite script |
| `guess_game.arw` | Real-time interactive number guessing game using the `ถาม` input command |
| `pos_cashier.arw` | Interactive Restaurant POS & Cashier checkout system |
| `test_traps.py` | Automated test suite verifying all 11 meme traps and edge cases |
| `README.md` | Complete documentation and specifications in Thai |
| `README_EN.md` | Complete documentation and specifications in English |
