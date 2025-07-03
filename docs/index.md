<div align="center">
  <h1>Glorp Language Reference</h1>
  <p><strong>The official language documentation for Glorp.</strong></p>
</div>
<iframe src="https://discord.com/widget?id=1390350998236696686&theme=dark" width="350" height="500" allowtransparency="true" frameborder="0" sandbox="allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts"></iframe>
---

## Introduction

Glorp is a statically-typed, pragmatic programming language. It is designed for clarity and developer productivity, featuring a simple syntax and a powerful, built-in reactivity system.

This document serves as the official reference for the Glorp language syntax and features.

!!! note "Core Philosophy"
    Glorp aims to provide the safety of static types and the power of modern language features (like reactivity) while leveraging the vast and mature Python ecosystem.

## 1. Syntax Fundamentals

### 1.1. Comments

Comments are ignored by the compiler and are used to leave notes in the code. Glorp supports two types of comments.

```glorp
// This is a single-line comment. It extends to the end of the line.

/*
  This is a multi-line, or block, comment.
  It can span multiple lines.
*/
```

### 1.2. Data Types

Glorp is statically typed. You must declare the type of every variable. The built-in primitive types are:

| Type   | Description                | Example Literal   |
|--------|----------------------------|-------------------|
| `Int`  | A signed integer.          | `42`, `-10`       |
| `Str`  | A string of text.          | `"Hello, Glorp!"` |
| `Bool` | A boolean value.           | `true`, `false`   |
| `List` | An ordered collection.     | `[1, 2, 3]`       |
| `Null` | Represents the absence of a value. | Used as a return type for functions that do not return a value. |

---

## 2. Variables

Variables are declared using the `let` keyword. They must be initialized with a value of the specified type.

**Syntax:**
`let <Type> <name> = <expression>`

**Example:**
```glorp
let Str welcome_message = "Welcome to the language guide!"
let Int user_count = 100
let List initial_scores = [100, 200, 300]
```

Variables can be reassigned later in the code, but their type cannot be changed.

```glorp
let Int my_var = 10
let Int my_var = 20 // This is valid

// let Int my_var = "hello" // This will cause a type error
```

---

## 3. Functions

Functions are a core building block for reusable code. Glorp supports two syntax styles for defining functions.

### 3.1. Block Body Functions

Used for functions with multiple statements or complex logic.

**Syntax:**
`fn <ReturnType> <name>(<parameters>) { <body> }`

```glorp
fn Null greet(Str name) {
    let Str message = "Hello, " + name + "!"
    out(message)
    // No return value, so the type is Null
}
```

### 3.2. Shorthand Expression Functions

Used for simple, single-expression functions. The result of the expression is implicitly returned.

**Syntax:**
`fn <ReturnType> <name>(<parameters>) => <expression>`

```glorp
// This function takes two integers and returns their sum.
fn Int add(Int a, Int b) => a + b
```

### 3.3. Parameters and Return

- **Parameters:** A comma-separated list of `Type name` pairs within the parentheses.
- **Return:** The `=>` symbol is used to return a value from within a block body function.

```glorp
fn Int check_age(Int age) {
    if age >= 18 {
        => 1 // Return 1 if adult
    }
    => 0 // Return 0 otherwise
}
```

---

## 4. Reactivity: The `watch` Statement

The `watch` keyword is Glorp's most distinctive feature. It declares a variable and simultaneously attaches a "handler" block that automatically executes every time the variable's value changes.

**Syntax:**
`watch <Type> <name> = <initial_value> -> <handler>`

The handler can be a single statement or a block of code in curly braces.

**Example:**
```glorp
fn Null Main() {
    // 1. Declare a watched variable `counter`.
    // 2. The code in the { ... } block will run every time
    //    the value of `counter` is updated.
    watch Int counter = 0 -> {
        out("Value changed! Counter is now: ", counter)
        if counter > 3 {
            out("Counter has exceeded 3!")
        }
    }

    out("Program start.")
    
    let Int counter = 1  // Handler runs. Output: "Value changed! Counter is now: 1"
    let Int counter = 2  // Handler runs. Output: "Value changed! Counter is now: 2"
    // No change, no handler execution
    let Int counter = 2
    
    // Using a single-statement handler
    watch Str name = "Guest" -> out("Name changed to: ", name)
    let Str name = "Admin" // Handler runs. Output: "Name changed to: Admin"
}
```
---

## 5. Control Flow

### 5.1. Conditional: `if/elif/else`

Executes code based on one or more conditions.

```glorp
fn Str get_grade(Int score) {
    if score >= 90 {
        => "A"
    } elif score >= 80 {
        => "B"
    } else {
        => "C"
    }
}
```

### 5.2. `while` Loop

Repeats a block of code as long as a condition is `true`.

```glorp
let Int i = 1
while i <= 5 {
    out("Current value of i: ", i)
    let Int i = i + 1
}
```

### 5.3. `for` Loop

Glorp's `for` loop iterates over an inclusive range of integers.

**Syntax:**
`for let Int <var> = <start> to <end> { <body> }`

```glorp
// This loop will print numbers from 1 to 5, including 5.
for let Int i = 1 to 5 {
    out("Iteration ", i)
}
```

---

## 6. Expressions and Operators

Glorp follows a standard order of operations. Use parentheses `()` to enforce a specific evaluation order.

| Category      | Operators                                   | Associativity |
|---------------|---------------------------------------------|---------------|
| **Power**     | `^`                                         | Right         |
| **Term**      | `*`, `/`                                    | Left          |
| **Arithmetic**| `+`, `-`                                    | Left          |
| **Comparison**| `==`, `!=`, `>`, `<`, `>=`, `<=`            | Left          |
| **Logical**   | `not` (prefix), `and` (infix), `or` (infix) | Left          |

**Example:**
```glorp
let Int result = (10 + 2) * 3 // result is 36
let Bool is_true = (5 > 3) and (10 != 20) // is_true is true
```

---

## 7. Data Structures

### 7.1. Arrays

Arrays are ordered, zero-indexed collections of elements. They are defined using square brackets.

```glorp
// Declaration
let List names = ["Alice", "Bob", "Charlie"]
let List numbers =
let List empty_list = []

// Element Access
let Str first_name = names // "Alice"
out(first_name)
```

---

## 8. Modules and Scope

### 8.1. Modules (`use`)

You can split your code into multiple `.glorp` files and import them using the `use` statement. This treats the imported file as a class-like namespace.

**`math.glorp`:**
```glorp
// This function is public by default
fn Int add(Int a, Int b) => a + b

// This variable is private and will not be accessible from other modules
private Str version = "1.0"
```

**`main.glorp`:**
```glorp
// Import the math module
use math

fn Null Main() {
    // Call the function using the module's name as a namespace
    let Int sum = math.add(5, 7) // sum is 12
    out(sum)

    // out(math.version) // This would cause an error
}
```

### 8.2. Private Members

The `private` keyword makes a variable accessible only within the file it is declared in. It cannot be accessed from a module that `use`s it.

**Syntax:**
`private <Type> <name> = <expression>`

---

## 9. Built-in Functions

Glorp provides a small set of built-in functions for basic I/O.

### 9.1. `out()`

Prints one or more values to the console. Arguments are separated by commas.

```glorp
out("The answer is:", 42) // Prints "The answer is: 42"
```

### 9.2. `clear()`

Clears the terminal screen (by sending ANSI escape codes).

```glorp
clear()
```
