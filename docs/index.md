# Welcome to Glorp: The Official Documentation

Glorp is a modern, statically-typed programming language that transpiles to Python. It is designed to be expressive, readable, and powerful, combining the safety of static types with a clean, concise syntax.

This documentation will guide you through all the features of the Glorp language, from the basics to advanced topics like lazy evaluation and reactive programming.


## 1. Getting Started

### Your First Glorp Program

Let's start with the classic "Hello, World!". Create a file named `hello.glorp`.

```glorp
// hello.glorp

// Every Glorp program needs a Main function as its entry point.
fn Null Main() ->
    out("Hello, Glorp World!\n")
```

To run this, you would use the Glorp interpreter:

```bash
glorp hello.glorp
```

### The Entry Point: `Main()`

**Every executable Glorp program must have a function named `Main`**. This is where the execution of your program begins. It can take no arguments and typically returns `Null`, but can return other types if needed.

```glorp
fn Int Main() ->
    out("Program starting...\n")
    => 0 // Return an exit code
```

---

## 2. Core Concepts

### Comments

Glorp supports two types of comments, just like C++, Java, or JavaScript.

```glorp
// This is a single-line comment.

/*
  This is a
  multi-line comment block.
*/
```

### Data Types

Glorp is statically typed. You must declare the type of every variable and function return value.

| Glorp Type | Python Equivalent | Description                               |
| :--------- | :---------------- | :---------------------------------------- |
| `Int`      | `int`             | Whole numbers (e.g., `10`, `-5`).         |
| `Float`    | `float`           | Floating-point numbers (e.g., `3.14`).    |
| `Str`      | `str`             | Text strings (e.g., `"hello"`).           |
| `Bool`     | `bool`            | `true` or `false`.                        |
| `List`     | `list` / `iterator` | An ordered collection of items.         |
| `Dict`     | `dict`            | A collection of key-value pairs.          |
| `Null`     | `None`            | Represents the absence of a value.        |

---

## 3. Variables and Scope

### Variable Declaration (`let`)

You declare a new variable using the `let` keyword. A value must be assigned at declaration.

```glorp
let Int score = 100
let Str player_name = "Alex"
let Bool is_active = true
```

### Variable Reassignment (`set`)

To change the value of an *existing* variable, use the `set` keyword. This helps prevent accidental re-declarations.

```glorp
let Int health = 100
set health = health - 10 // health is now 90

// This would cause an error, as 'health' is already declared.
// let Int health = 50
```

### Private Variables

When creating modules, you can declare variables with `private`. These variables will not be accessible from outside the module file.

```glorp
// in my_module.glorp
private Str api_key = "SECRET_KEY" // This cannot be accessed via my_module.api_key
let Str public_data = "some data"
```

### Watched Variables (`watch`)

This powerful feature allows you to execute a block of code whenever a variable's value changes. This is a core concept for reactive programming in Glorp.

```glorp
// The handler code will run every time 'level.value' is changed.
watch Int level = 1 ->
    out("Level up! You are now level ", level, "!\n")

// To access or change the value, use '.value'
out("Current level: ", level.value, "\n") // Prints 1

set level.value = 2 // Triggers the handler, printing "Level up!..."
```

---

## 4. Operators

### Arithmetic Operators

| Operator | Description        | Example         |
| :------- | :----------------- | :-------------- |
| `+`      | Addition           | `5 + 3`         |
| `-`      | Subtraction        | `5 - 3`         |
| `*`      | Multiplication     | `5 * 3`         |
| `/`      | Division           | `5 / 3`         |
| `%`      | Modulo (remainder) | `5 % 3`         |
| `%%`     | Integer Division   | `5 %% 3`        |
| `^`      | Power              | `5 ^ 3`         |

### Comparison Operators

| Operator | Description              | Example       |
| :------- | :----------------------- | :------------ |
| `==`     | Equal to                 | `x == y`      |
| `!=`     | Not equal to             | `x != y`      |
| `>`      | Greater than             | `x > y`       |
| `<`      | Less than                | `x < y`       |
| `>=`     | Greater than or equal to | `x >= y`      |
| `<=`     | Less than or equal to    | `x <= y`      |

### Logical Operators

| Operator | Description                               | Example           |
|:---|:---|:---|
| `and`    | Logical AND (true if both are true)       | `a > 0 and b > 0` |
| `or`     | Logical OR (true if either is true)       | `a > 0 or b > 0`  |
| `not`    | Logical NOT (inverts boolean value)       | `not is_active`   |

---

## 5. Data Structures

### Lists

Lists are ordered collections.

```glorp
let List numbers = [1, 2, 3, 5, 8]
let List mixed = [1, "two", true]
```

### Dictionaries

Dictionaries store key-value pairs.

```glorp
let Dict user = {
    "name": "Gandalf",
    "class": "Wizard",
    "level": 20
}
```

### Lazy Ranges

Glorp provides a concise syntax for creating **lazy iterators** over a range of numbers. They do not consume memory for all numbers at once.

```glorp
// Creates a lazy iterator from 1 to 10 (inclusive)
let List my_range = [1...10]

// Creates a lazy iterator from 0 to 100 with a step of 5
let List by_fives = [0, 5...100]
```

### Element Access

Access elements in lists and dictionaries using square brackets `[]`.

```glorp
let List items = ["sword", "shield", "potion"]
let Str first_item = items[0] // "sword"

let Dict user = {"name": "Aragorn"}
let Str user_name = user["name"] // "Aragorn"
```

---

## 6. Control Flow

Glorp uses `->` for single-line bodies and `{}` for multi-line bodies to keep syntax clean.

### `if` / `elif` / `else`

Standard conditional logic. `when` is an alias for a single `if`.

```glorp
let Int score = 85

if score > 90 -> out("Grade: A\n")
elif score > 80 {
    out("Grade: B\n")
    out("Good job!\n")
}
else -> out("Keep trying!\n")
```

### `switch`

A powerful alternative to `if-elif` chains, similar to pattern matching.

```glorp
let Str command = "go_north"

switch command ->
    "go_north" => out("You move north.")
    "go_south" => out("You move south.")
    "get_item" => out("You pick up the shiny object.")
    else       => out("Unknown command.")
```

### `while` Loops

Executes a block of code as long as a condition is true.

```glorp
let Int i = 0
while i < 5 ->
    out(i, "\n")
    set i = i + 1
```

### `for` Loops

Iterates over a numerical range.

```glorp
// Iterates from 1 up to 10
for i from 1 to 10 ->
    out(i, "\n")

// Iterates from 10 down to 1
for i from 10 to 1 ->
    out(i, "\n")
```

### `each` Loops

The idiomatic way to iterate over any collection or iterator.

**1. Block Form:**
```glorp
let List names = ["Frodo", "Sam", "Merry"]
each Str name in names -> {
    out("Welcome, ", name, "!\n")
}
```

**2. Quick Form (Lazy Comprehension):**
This form creates a new lazy iterator by transforming another.

```glorp
let List numbers = [1...10]

// Create a new lazy iterator of squared numbers
let List squares = each Int n in numbers -> n ^ 2

// Filter and transform at the same time
let List even_squares = each Int n in numbers where n % 2 == 0 -> n ^ 2
```

---

## 7. Functions

### Declaration

Functions are first-class citizens. They require type hints for parameters and the return value.

**1. Short Form (Lambda-style):**
For single-expression functions.
```glorp
fn Int add(Int a, Int b) => a + b
```

**2. Long Form (Block Body):**
For functions with multiple statements.
```glorp
fn Null greet(Str name) -> {
    let Str message = "Hello, " + name + "!"
    out(message)
    return // Explicit return for Null functions
}
```

### Generators and `yield`

A function becomes a **generator** if it uses the `->` statement (syntactic sugar for `yield`). Generators produce a sequence of values lazily.

```glorp
// This function generates the Fibonacci sequence infinitely.
fn List fibonacci() ->
    let Int a = 0
    let Int b = 1
    while true ->
        -> a // Yield the current value
        let Int temp = a
        set a = b
        set b = temp + b
```

---

## 8. Advanced Features

### Lazy Evaluation

Many of Glorp's features, like ranges `[...]`, quick `each` loops, and generators, are **lazy**. This means they don't compute their values until they are actually needed. This is incredibly efficient for memory and allows you to work with very large or even infinite data sets.

### Modules (`use`)

Split your code into multiple files and use them as modules.

```glorp
// file: math_utils.glorp
fn Int double(Int x) => x * 2
private Int secret = 42 // Not exported

// file: main.glorp
use "math_utils"

fn Null Main() ->
    let Int result = math_utils.double(10) // 20
    out(result)
    // math_utils.secret would be an error
```

### Infinity (`Inf`)

Glorp has built-in support for infinity.

```glorp
// A loop that runs until manually broken
for i from 0 to Inf ->
    if i > 1000 -> break
    out(i, "\n")
```

### Taking from Iterators (`take`)

Safely get a specific number of items from any iterator, including infinite ones.

```glorp
// From the fibonacci() generator example above
let List first_10_fib = take 10 from fibonacci()

each Int n in first_10_fib ->
    out(n, " ") // 0 1 1 2 3 5 8 13 21 34
```

---

## 9. Error Handling

### `try` / `catch`

Handle potential runtime errors gracefully. The error is captured in the `exception` variable.

```glorp
try {
    let Int num = read_int("Enter a number: ")
    out("You entered: ", num, "\n")
}
catch {
    out("That wasn't a valid integer! Details: ", exception, "\n")
}
```

### `throw`

Raise your own custom errors.

```glorp
fn Null check_age(Int age) ->
    if age < 18 -> throw "User is too young!"
    out("Access granted.")
```

---

## 10. Built-in Functions

Glorp provides a small but useful standard library of global functions.

| Function | Description |
|:---|:---|
| `out(...)` | Prints arguments to the console without a newline. |
| `clear()` | Clears the console screen. |
| `readfile(filename)` | Reads an entire file into a string. |
| `writefile(filename, content)`| Writes a string to a file. |
| `read(prompt)` | Reads a line of text from the user. |
| `read_str(prompt)` | Alias for `read`. |
| `read_int(prompt)` | Reads input and ensures it's a valid integer. |
| `read_float(prompt)` | Reads input and ensures it's a valid float. |
| `read_bool(prompt)` | Reads input and ensures it's a valid boolean (`true`/`false`). |
| `str(val)`, `int(val)`, etc. | Type conversion functions. |
| `take(n, iterable)` | Returns a lazy iterator with the first `n` items. |
| `grange(start, end, step?)` | The underlying function for lazy ranges. |

---

## 11. Use Cases & Examples

### Case 1: Interactive CLI Tool

This program asks for a user's name and year of birth, then calculates their approximate age.

```glorp
// age_calculator.glorp

fn Null Main() ->
    out("--- Age Calculator ---\n")
    let Str name = read_str("What is your name? ")
    let Int birth_year = read_int("What year were you born? ")
    let Int current_year = 2024 // Or fetch dynamically

    let Int age = current_year - birth_year

    out("\nHello, ", name, "! You are approximately ", age, " years old.\n")
```

### Case 2: Lazy Data Processing Pipeline

This example reads a large log file, finds all lines containing "ERROR", extracts a message, and prints the first 5 found, all without loading the whole file into memory.

```glorp
// log_analyzer.glorp

fn Null Main() ->
    let Str file_content = readfile("large_log_file.log")
    let List lines = str.split(file_content, "\n")

    // Create a lazy iterator of error messages
    let List error_msgs = each Str line in lines
                          where str.contains(line, "ERROR")
                          -> str.replace(line, "ERROR: ", "")

    // Take only the first 5 errors found
    let List first_five_errors = take 5 from error_msgs

    out("First 5 errors found:\n")
    each Str msg in first_five_errors ->
        out("- ", msg, "\n")
```

---

## 12. Formal Syntax (Grammar)

For language tool developers and those interested in Glorp's inner workings, here is the formal grammar in Lark syntax.

```lark
start: global_statement+

global_statement: import_stmt | var_decl | func_short | func_long | private | watch_stmt

local_statement:    var_decl
                  | return_stmnt
                  | if_stmnt
                  | while_stmnt
                  | for_loop
                  | for_each
                  | watch_stmt
                  | var_change
                  | call
                  | try_stmt
                  | throw
                  | yield_stmt
                  | switch_case

import_stmt: "use" name

var_decl: "let" TYPE name "=" expression
var_change: "set" name "=" expression
private: "private" TYPE name "=" expression
func_short: "fn" TYPE name "(" parameters? ")" "=>" expression
watch_stmt: "watch" TYPE name "=" expression "->" (local_statement | body)
return_stmnt: "=>" expression
switch_case: "switch" expression "->" (expression "=>" local_statement | body)* ("else" "->" local_statement | body)
take_stmt: "take" expression "from" expression

func_long: "fn" TYPE name "(" parameters? ")" body

if_stmnt:     "if" expression body ("elif" expression body )* ("else" body)?
            | "when" expression body
while_stmnt: "while" expression body
for_loop: "for" name "from" expression ("up" | "down")? "to" expression body
for_each: "each" name "in" expression body
quick_foreach: "each" name "in" expression ("where" expression)? "->" expression ("else" expression)?
try_stmt: "try" body "catch" body
throw: "throw" expression
yield_stmt: "->" expression

body: ("{" local_statement* "}") | ("->" local_statement)

TYPE: NAME

parameters: TYPE name ("," TYPE name)*
expression: quick_foreach | logic_or

logic_or: logic_and ("or" logic_and)*
logic_and: logic_not ("and" logic_not)*
logic_not: "not" logic_not -> logic_unary_not
         | comparison
comparison: arith_exp (op_bool arith_exp)?

arith_exp: term (op_exp term)*
term: factor (op_term factor)*
factor: NUMBER
      | "-" INF     -> neg_inf
      | ("+")? INF     -> pos_inf
      | STRING
      | name
      | "(" expression ")"
      | call
      | array
      | dictionary
      | element
      | num_range
      | take_stmt

?op_exp: OP_ADD | OP_SUB
OP_ADD: "+"
OP_SUB: "-"

?op_term: OP_MUL | OP_DIV | OP_POW
OP_MUL: "*"
OP_DIV: "/" | "%" | "%%"
OP_POW: "^"

?op_bool: OP_EQ | OP_NE | OP_GT | OP_LT | OP_GE | OP_LE
OP_EQ: "=="
OP_NE: "!="
OP_GT: ">"
OP_LT: "<"
OP_GE: ">="
OP_LE: "<="

INF: "Inf" | "Infinity"

call: name "(" [arguments] ")"

array: "[" [array_elements] "]"
num_range: "[" expression "," (expression ",")? "..." "," expression "]"
dictionary: "{" dictionary_elements "}"
element: NAME "[" expression "]"

name: NAME("."NAME)*

arguments: expression ("," expression)*
array_elements: expression ("," expression)*
dictionary_element: expression ":" expression
dictionary_elements: dictionary_element ("," dictionary_element)*

%import common.CNAME
%import common.ESCAPED_STRING

%import common.CNAME -> NAME
%import common.SIGNED_NUMBER -> NUMBER
%import common.ESCAPED_STRING -> STRING
%import common.WS

SINGLE_LINE_COMMENT: /\/\/[^\n]*/
MULTI_LINE_COMMENT_STD: /\/\*[\s\S]*?\*\//

%ignore SINGLE_LINE_COMMENT
%ignore MULTI_LINE_COMMENT_STD
%import common.WS
%ignore WS
```
