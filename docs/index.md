Отличная идея обновить документацию! Это критически важно для любого проекта. Я взял твою текущую документацию и обновил её, чтобы отразить все изменения в версии 1.0.3, а также улучшил структуру и примеры для большей ясности.

Вот обновленная версия.

---

<div align="center">
  <h1>Glorp Language Reference</h1>
  <p><strong>The official language documentation for Glorp v1.0.3.</strong></p>
</div>
<iframe src="https://discord.com/widget?id=1390350998236696686&theme=dark" width="350" height="500" allowtransparency="true" frameborder="0" sandbox="allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts"></iframe>

---

## Introduction

Glorp is a statically-typed, pragmatic programming language. It is designed for clarity and developer productivity, featuring a C-like syntax, a powerful reactivity system, and the ability to transpile directly to Python.

This document serves as the official reference for the Glorp language syntax and features.

## 1. Syntax Fundamentals

### 1.1. Comments

Comments are ignored by the compiler and are used to leave notes in the code. Glorp supports two types of comments.

```glorp
// This is a single-line comment.

/*
  This is a multi-line, or block, comment.
*/
```

### 1.2. Data Types

Glorp is statically typed. You must declare the type of every variable. The built-in primitive types are:

| Type   | Description                | Example Literal   |
|--------|----------------------------|-------------------|
| `Int`  | A signed integer.          | `42`, `-10`       |
| `Str`  | A string of text.          | `"Hello, Glorp!"` |
| `Bool` | A boolean value.           | `true`, `false`   |
| `List` | An ordered collection (array). | `[1, "a", true]`  |
| `Dict` | A collection of key-value pairs. | `{"name": "Alex", "age": 30}` |
| `Null` | Represents the absence of a value. | Used as a return type for functions that do not return anything. |

---

## 2. Variables and Re-assignment

### 2.1. Declaration with `let`

Variables are declared for the first time using the `let` keyword. They must be given a type and can be initialized with a value.

**Syntax:**
`let <Type> <name> = <expression>`

**Example:**
```glorp
let Str welcome_message = "Welcome to the language guide!"
let Int user_count = 100
let List initial_scores = [100, 200, 300]
let Dict user_data = {"id": 1, "active": true}
```

### 2.2. Re-assignment with `set`

To change the value of an *existing* variable, use the `set` keyword. You do not need to specify the type again. Using `let` to declare a variable that already exists will cause an error.

**Syntax:**
`set <name> = <expression>`

**Example:**
```glorp
// Correct usage
let Int my_var = 10
out(my_var) // Prints 10

set my_var = 20
out(my_var) // Prints 20

// Incorrect usage
// let Int my_var = 30 // Error: 'my_var' has already been declared.
```

---

## 3. Functions

Functions are a core building block for reusable code. Glorp supports two syntax styles for defining functions.

### 3.1. Block Body Functions

Used for functions with multiple statements. The `=>` symbol is used inside the body to return a value.

**Syntax:**
`fn <ReturnType> <name>(<parameters>) { <body> }`

```glorp
fn Str get_status(Int code) {
    if code == 200 {
        => "OK"
    }
    => "Error"
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

---

## 4. Reactivity: The `watch` Statement

The `watch` keyword is Glorp's most distinctive feature. It declares a variable and simultaneously attaches a "handler" block that automatically executes every time the variable's value changes.

**Syntax:**
`watch <Type> <name> = <initial_value> -> <handler>`

The handler can be a single statement or a block of code in curly braces. To update a watched variable, use the `set` keyword.

**Example:**
```glorp
fn Null Main() {
    watch Int counter = 0 -> {
        out("Counter changed! It's now: ", counter)
    }

    out("Program start.")
    
    set counter = 1  // Handler runs. Output: "Counter changed! It's now: 1"
    set counter = 2  // Handler runs. Output: "Counter changed! It's now: 2"
    set counter = 2  // Handler does NOT run, because the value didn't change.
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
    set i = i + 1
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

| Category      | Operators                                   |
|---------------|---------------------------------------------|
| **Power**     | `^`                                         |
| **Term**      | `*`, `/`                                    |
| **Arithmetic**| `+`, `-`                                    |
| **Comparison**| `==`, `!=`, `>`, `<`, `>=`, `<=`            |
| **Logical**   | `not` (prefix), `and` (infix), `or` (infix) |

---

## 7. Data Structures

### 7.1. Lists (Arrays)

Lists are ordered, zero-indexed collections of elements, defined using square brackets `[]`.

```glorp
let List names = ["Alice", "Bob", "Charlie"]
let List empty_list = []

// Element Access (zero-indexed)
let Str first_name = names[0] // "Alice"
out(first_name)
```

### 7.2. Dictionaries

Dictionaries are unordered collections of key-value pairs, defined using curly braces `{}`. Keys are typically strings.

```glorp
// Declaration
let Dict user = {"name": "Bob", "id": 42, "is_active": true}
let Dict empty_dict = {}

// Element Access
let Str user_name = user["name"] // "Bob"
out(user_name)
```

---

Отлично, это очень важный и неинтуитивный аспект, который обязательно нужно объяснить в документации. Пользователи, привыкшие к другим языкам, точно столкнутся с этим и будут удивлены.

Я добавлю новый раздел `8.4. A Peculiarity of Module Scopes` (Особенность областей видимости модулей) и подробно, с примерами, объясню это поведение.

Вот обновленный раздел 8 целиком.

---

## 8. Modules and Scope

Glorp encourages code organization by allowing you to split your code into multiple files, which can then be used as modules. This system helps you create reusable components and manage the complexity of larger projects.

### 8.1. Creating and Using Modules (`use`)

Any `.glorp` file can act as a module. You can import one file into another using the `use` statement. When you do this, all public, top-level `let` variables and `fn` functions from the imported file become available under a namespace that matches the filename.

**`config.glorp`:**
```glorp
let Str API_ENDPOINT = "https://api.example.com"

fn Bool is_valid_port(Int port) {
    => (port > 1024) and (port < 65535)
}
```

**`main.glorp`:**
```glorp
use config

fn Null Main() {
    out("Connecting to: ", config.API_ENDPOINT)
    if config.is_valid_port(8080) {
        out("Port 8080 is valid.")
    }
}
```

### 8.2. Private Variables for Internal State

The `private` keyword allows you to define variables that are strictly confined to the file they are declared in. They are used for internal calculations and are completely inaccessible from outside the module file.

**Syntax:**
`private <Type> <name> = <expression>`

(For a detailed explanation of Glorp's strict privacy model, see section 8.4)

### 8.3. A Peculiarity of Module Scopes: Self-Referencing

Glorp's module system has a unique characteristic that developers must be aware of. When you define functions inside a module, they do not automatically have access to other members (variables or functions) of the same module. **To access another member of the same module, you must explicitly use the module's own name as a namespace.**

This is best explained with an example.

Let's consider a module named `math.glorp`.

**`math.glorp`:**
```glorp
let Int PI_APPROX = 3

// --- INCORRECT ---
// This function will fail because 'PI_APPROX' is not in its local scope.
// fn Int get_pi_incorrect() => PI_APPROX 

// --- CORRECT ---
// To access PI_APPROX from within the same module, you must qualify
// it with the module's name: 'math'.
fn Int get_pi() {
    => math.PI_APPROX
}

fn Int add_one_to_pi() {
    // This also requires using the 'math' namespace to call another
    // function in the same module.
    let Int pi_val = math.get_pi()
    => pi_val + 1
}
```

**Why does it work this way?**

This behavior is a direct result of how Glorp transpiles modules. When you write `use math`, the `math.glorp` file is processed and converted into a Python `class` named `math`.

*   `let PI_APPROX = 3` becomes a class attribute `math.PI_APPROX`.
*   `fn Int get_pi()...` becomes a method within the `math` class.

From inside a method in Python, you cannot directly access a class attribute by its name alone; you need to reference it through the class (or an instance, e.g., `self`). Glorp simplifies this by requiring you to always use the static class name (`math`). This makes the code consistent and explicit about where a variable or function is coming from, even when working inside the module itself.

**Rule of Thumb:** When inside a file `my_module.glorp`, always use `my_module.member` to access another top-level `member` (variable or function) defined in that same file.

### 8.4. Understanding Glorp's Strict Privacy Model

Glorp's privacy model for variables is stricter than in many other languages. Think of a private variable not as a "private field" of a class, but as a **temporary, file-scoped constant**. It exists only during the initial processing of the module and is erased afterwards.

This means a private variable **cannot be accessed by any functions**, not even public functions within the same module, because the variable is deleted before the functions can be called.

**`secret_key_manager.glorp`:**
```glorp
// A private, internal master key. It's only used right here.
private Str MASTER_KEY = "super-secret-master-string"

// A public variable whose value is DERIVED from the private key.
// This calculation happens once when the module is loaded.
let Str PUBLIC_API_TOKEN = MASTER_KEY + "-public-token"

// This function would FAIL if uncommented, because by the time it is called,
// MASTER_KEY no longer exists.
// fn Str get_master_key_again() => secret_key_manager.MASTER_KEY
```

This design ensures that sensitive information is completely erased and cannot be leaked or accidentally modified after the module is initialized. Use `private` variables for one-time setup calculations whose results are stored in public variables.

---

## 9. Built-in Functions and Error Handling

### 9.1. `out()`

Prints one or more values to the console.

```glorp
out("The answer is:", 42)
```

### 9.2. `clear()`

Clears the terminal screen.

```glorp
clear()
```

### 9.3. Error Handling with `try/catch`

Glorp provides a `try`/`catch` structure to handle potential runtime errors.

**Syntax:**
```glorp
try {
    // Code that may fail
} catch {
    // Code to run if an error occurs
}
```

The special variable `exception` is available inside the `catch` block to inspect the error.

```glorp
fn Null Main() {
    try {
        let Int result = 10 / 0
        out("This will not be printed.")
    } catch {
        out("An error occurred!", exception)
    }
    out("Program continues after try/catch.")
}
```
