<div align="center">
  <h1>Glorp Language Reference</h1>
  <p><strong>The official language documentation for Glorp v1.0.5.</strong></p>
</div>
<iframe src="https://discord.com/widget?id=1390350998236696686&theme=dark" width="350" height="500" allowtransparency="true" frameborder="0" sandbox="allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts"></iframe>

## Introduction

Glorp is a statically-typed, pragmatic programming language. It is designed for clarity and developer productivity, featuring a C-like syntax, a powerful reactivity system, and the ability to transpile directly to Python. This version introduces powerful list initialization and more intuitive loop constructs.

This document serves as the official reference for the Glorp language syntax and features.

## 1. Syntax Fundamentals

### 1.1. Comments

```glorp
// Single-line comment.
/* Multi-line comment. */
```

### 1.2. Data Types

Glorp is statically typed. The built-in primitive types are:

| Type    | Description                       | Example Literal                |
|---------|-----------------------------------|--------------------------------|
| `Int`   | A signed integer.                 | `42`, `-10`                    |
| `Float` | A number with a decimal point.    | `3.14`, `99.9`, `-0.5`         |
| `Str`   | A string of text.                 | `"Hello, Glorp!"`              |
| `Bool`  | A boolean value.                  | `true`, `false`                |
| `List`  | An ordered collection (array).    | `[1, "a", true]`               |
| `Dict`  | A collection of key-value pairs.  | `{"name": "Alex", "age": 30}`  |
| `Null`  | Represents the absence of a value.| Used as a return type.         |

---

## 2. Variables and Re-assignment

### 2.1. Declaration (`let`)

Variables are declared using `let`. They must be given a type.

**Syntax:** `let <Type> <name> = <expression>`
```glorp
let Str message = "Hello!"
let Int count = 100
let Float gravity = 9.81
```

### 2.2. Re-assignment (`set`)

To change the value of an existing variable, use `set`.

**Syntax:** `set <name> = <expression>`
```glorp
let Int score = 0
set score = 100 // Correct
```

---

## 3. Functions

### 3.1. Block Body Functions

For multi-statement logic. Use `=>` to return a value.
`fn <ReturnType> <name>(<parameters>) { <body> }`
```glorp
fn Str get_status(Int code) {
    if code == 200 { => "OK" }
    => "Error"
}
```

### 3.2. Shorthand Expression Functions

For single-expression logic. The result is implicitly returned.
`fn <ReturnType> <name>(<parameters>) => <expression>`
```glorp
fn Float circle_area(Float radius) => 3.14159 * (radius ^ 2)
```

---

## 4. Reactivity: The `watch` Statement

The `watch` keyword declares a variable and attaches a handler that executes every time the variable's value changes. Use `set` to update a watched variable.

**Syntax:** `watch <Type> <name> = <initial_value> -> <handler>`
```glorp
watch Float price = 99.99 -> {
    out("Price changed! New price: $", price, "\n")
}

set price = 89.99 // Handler runs.
```
---

## 5. Control Flow

### 5.1. Conditional: `if/elif/else`

```glorp
fn Str get_grade(Int score) {
    if score >= 90 { => "A" } 
    elif score >= 80 { => "B" } 
    else { => "C" }
}
```

### 5.2. Loops

Glorp provides three types of loops for handling iterative tasks.

#### 5.2.1. `while` Loop

Executes a block of code as long as a condition is true.

```glorp
let Int i = 3
while i > 0 {
    out(i, "... ")
    set i = i - 1
} // Prints "3... 2... 1... "
```

#### 5.2.2. `for ... to` Loop (Range Iteration)

Iterates over an inclusive range of integers. As of v1.0.5, the `let` keyword is no longer required in the declaration.

`for <Type> <var> = <start> to <end> { <body> }`
```glorp
// The 'let' keyword is now omitted for cleaner syntax.
for Int i = 1 to 3 { 
    out("Lap ", i, "\n") 
}
```

#### 5.2.3. `for each ... in` Loop (Collection Iteration)

**New in 1.0.5:** This loop provides a simple way to iterate over each element in a `List`.

`for each <var> in <collection> { <body> }`

The type of the loop variable `<var>` is automatically inferred from the elements of the collection.

```glorp
// Create a list from 5 down to 1 using the new range syntax
let List countdown = [5, ..., 1]

// Iterate over the newly created list
for each num in countdown {
    out(num, "! ")
}
out("Go!\n")

// --- Output ---
// 5! 4! 3! 2! 1! Go!
```

---

## 6. Expressions and Operators

Glorp follows a standard order of operations. When an `Int` and a `Float` are used in an operation, the result is promoted to a `Float`.

```glorp
let Float result = (10 + 2.5) * 2 // result is 25.0
```
---
## 7. Data Structures

### 7.1. Lists (Arrays)

Ordered, zero-indexed collections of values.

**Standard Initialization:**
```glorp
let List data = [1, 3.14, "Glorp"]
let Str item = data[2] // "Glorp"
```

**Range-based Initialization (New in 1.0.5):**

Glorp offers a powerful shorthand to create lists containing a sequence of integers using the `...` operator.

**Syntax:** `[<start>, ..., <end>]`

This creates a new list with an inclusive range of integers. The operator automatically handles ascending and descending sequences.

```glorp
// Ascending sequence
let List up = [1, ..., 5]
// up is now [1, 2, 3, 4, 5]

// Descending sequence
let List down = [10, ..., 7]
// down is now [10, 9, 8, 7]

let Int limit = 3
let List from_var = [limit, ..., limit - 2]
// from_var is now [3, 2, 1]
```

### 7.2. Dictionaries
Unordered collections of key-value pairs.
```glorp
let Dict user = {"id": 101, "name": "Alice"}
let Str name = user["name"] // "Alice"
```
---

## 8. Error Handling

### 8.1. `try/catch`
Handles potential runtime errors. The special variable `exception` is available inside the `catch` block.

```glorp
try {
    let Int result = 10 / 0
} catch {
    out("Error: Cannot divide by zero. Details: ", exception, "\n")
}
```
---
## 9. Modules and Scope
Glorp encourages code organization by allowing you to split your code into multiple files, which can then be used as modules. This system helps you create reusable components and manage the complexity of larger projects.

### 9.1. Creating and Using Modules (`use`)

Any `.glorp` file can act as a module. You can import one file into another using the `use` statement. When you do this, all public, top-level `let` variables and `fn` functions from the imported file become available under a namespace that matches the filename.

**`config.glorp`:**
```glorp
let Str API_ENDPOINT = "https://api.example.com"
fn Bool is_valid_port(Int port) => (port > 1024) and (port < 65535)
```

**`main.glorp`:**
```glorp
use config

fn Null Main() {
    out("Connecting to: ", config.API_ENDPOINT)
    if config.is_valid_port(8080) {
        out("Port 8080 is valid.\n")
    }
}
```

### 9.2. Private Variables for Internal State

The `private` keyword allows you to define variables that are strictly confined to the file they are declared in. They are used for internal calculations and are completely inaccessible from outside the module file.

**Syntax:** `private <Type> <name> = <expression>`

### 9.3. A Peculiarity of Module Scopes: Self-Referencing

Glorp's module system has a unique characteristic. To access a member (variable or function) from within the same module, you must explicitly use the module's own name as a namespace.

**`math.glorp`:**
```glorp
let Int PI_APPROX = 3

// Correct: To access PI_APPROX from within the same module, 
// you must qualify it with the module's name 'math'.
fn Int get_pi() {
    => math.PI_APPROX
}
```

**Why?** This is a result of how Glorp transpiles modules to Python classes. `let PI_APPROX = 3` becomes a class attribute, and `fn Int get_pi()` becomes a method. From inside a method, you need to reference the class (`math`) to access its attributes.

> **Rule of Thumb:** When inside a file `my_module.glorp`, always use `my_module.member` to access another top-level member in that same file.

### 9.4. Understanding Glorp's Strict Privacy Model

A `private` variable in Glorp is a temporary, file-scoped constant. It exists only during the initial processing of the module and is erased afterwards. This means a `private` variable cannot be accessed by any functions, not even public functions within the same module, because the variable is deleted before the functions can be called. Use `private` variables for one-time setup calculations.

**`secret_key_manager.glorp`:**
```glorp
// Private key used only for the initial calculation.
private Str MASTER_KEY = "super-secret-master-string"

// Public token derived from the private key. This is permanent.
let Str PUBLIC_API_TOKEN = MASTER_KEY + "-public-token"

// This function would FAIL if uncommented, because MASTER_KEY no longer exists.
// fn Str get_master_key_again() => secret_key_manager.MASTER_KEY
```

---
## 10. Built-in Functions

### 10.1. Console Output

*   **`out(...args)`**: Prints all arguments to the console, concatenated directly without spaces or a trailing newline.
    ```glorp
    out("Hello, ", "World!", "\n") // Prints "Hello, World!" and a newline.
    ```
*   **`clear()`**: Clears the console screen.

### 10.2. Console Input

These functions safely read user input, repeatedly prompting on invalid entry.

*   **`read_str(prompt)`**: Reads a line of text. Returns `Str`.
*   **`read_int(prompt)`**: Reads and validates an integer. Returns `Int`.
*   **`read_float(prompt)`**: Reads and validates a float. Returns `Float`.
*   **`read_bool(prompt)`**: Reads and validates a boolean (`true`/`false`, `y`/`n`). Returns `Bool`.

### 10.3. File I/O

*   **`writefile(Str path, Str content)`**: Writes (or overwrites) a string to a file.
*   **`readfile(Str path)`**: Reads an entire file's content into a string. Returns `Str`.

### 10.4. Exception Handling
* **`exception(Str e)`**: Exits the program with exit code `1` after outputting `Glorp runtime exception: {e}`.
```glorp
fn Float Sqrt(Int a) {
  if a < 0 {
    exception("Trying to take negative square root")
  }
  => a ^ 0.5
}
```
