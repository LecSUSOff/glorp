# Welcome to Glorp: The Official Documentation

Glorp is a modern, dynamically-typed programming language that transpiles to Python. It is designed to be expressive, readable, and powerful, offering a clean, concise syntax that simplifies everything from simple scripts to complex applications.

This documentation will guide you through all the features of the Glorp language. We'll start with a practical example to see it in action, then dive into the details.

---

## 1. Glorp by Example: A Guessing Game

Instead of just talking about syntax, let's see what Glorp code looks like by building a small, complete program. Here is a number guessing game.

Create a file named `game.glorp` and add the following code:

```glorp
fn Main() {
    out("--- Guess the Number Game ---\n")
    out("I'm thinking of a number between 1 and 100.\n\n")

    var secret_number = 73
    var is_running = true

    while is_running {
        var guess = read_int("Your guess: ")

        if guess < secret_number {
            out("Too low! Try again.\n")
        } elif guess > secret_number {
            out("Too high! Try again.\n")
        } else {
            out("\nYou got it! The number was ", secret_number, ".\n")
            var is_running = false // End the loop
        }
    }

    out("Thanks for playing!\n")
}
```

To run your game, use the Glorp interpreter from your terminal:

```bash
glorp game.glorp
```

### Breaking Down the Example

Let's look at the features this small program uses:

1.  **`fn Main() { ... }`**: This is the **entry point**. All executable Glorp programs must have a `Main` function where the program begins.
2.  **`out(...)`**: A built-in function that prints text to the console.
3.  **`var secret_number = 73`**: This is **variable declaration**. We use the `var` keyword to create a new variable. Glorp is dynamically typed, so you don't need to specify the type.
4.  **`while is_running { ... }`**: A **`while` loop** that continues to execute the code inside its `{}` block as long as the condition (`is_running`) is `true`.
5.  **`read_int(...)`**: A built-in function that pauses the program, prompts the user for input, and ensures the value they enter is a valid integer.
6.  **`if/elif/else`**: The **conditional block** that checks the user's guess and provides feedback.
7.  **`var is_running = false`**: This is **variable reassignment**. We change the value of an existing variable to control the flow of our loop.

This single example showcases a huge part of the language! Now, let's explore these concepts in more detail.

---

## 2. Core Concepts

### Comments

Use comments to leave notes in your code that are ignored by the interpreter.

```glorp
// This is a single-line comment.

/*
  This is a
  multi-line comment block.
*/
```

### Dynamic Typing

You do not need to specify the type of a variable. The type is inferred from the value you assign.

```glorp
var score = 100             // Inferred as an Integer
var player_name = "Alex"    // Inferred as a String
var is_active = true        // Inferred as a Boolean
```

---

## 3. Variables and Scope

### Variable Declaration and Assignment (`var`)

Declare a new variable and assign its initial value using the `var` keyword. To change the value later, simply use `var` again with the same variable name.

```glorp
fn Main() {
    // Declaration
    var health = 100
    out("Initial health: ", health, "\n")

    // Reassignment
    var health = health - 10
    out("Health after taking damage: ", health, "\n")
}
```

### Private Variables (`private`)

When creating modules, `private` provides **true encapsulation**. Private variables are inaccessible from outside the module file, protecting your internal implementation. Glorp achieves this through **name mangling**, renaming the variable to a unique, randomized name.

```glorp
// in my_module.glorp
private api_key = "SECRET_KEY" // Cannot be accessed via my_module.api_key
var public_data = "some data"
```

### Watched Variables (`watch`)

This powerful feature executes a block of code whenever a variable's value changes, enabling a reactive programming style. To access or change the watched value, you must use the `.value` property.

```glorp
fn Main() {
    // This handler runs every time 'level.value' changes.
    watch level = 1 {
        out("Level up! You are now level ", level, "!\n") //Note: you use level, not level.value there
    }

    out("Game start. Current level: ", level.value, "\n")
    var level.value = 2 // Triggers the handler
    var level.value = 3 // Triggers the handler again
}
```

---

## 4. Operators

### Arithmetic Operators

| Operator | Description | Example |
|:---|:---|:---|
| `+` | Addition | `5 + 3` |
| `-` | Subtraction | `5 - 3` |
| `*` | Multiplication | `5 * 3` |
| `/` | Division | `5 / 3` |
| `%` | Modulo (remainder) | `5 % 3` |
| `%%` | Integer Division | `5 %% 3` |
| `^` | Power | `5 ^ 3` |

### Comparison and Logical Operators

| Operator | Description |
|:---|:---|
| `==`, `!=`, `>`, `<`, `>=`, `<=` | Standard comparison operators. |
| `and` | Logical AND (true if both are true). |
| `or` | Logical OR (true if either is true). |
| `not` | Logical NOT (inverts a boolean value). |

---

## 5. Data Structures

### Lists (Arrays)

Lists are ordered, mutable collections of items.

```glorp
var numbers = [1, 2, 3, 5, 8]
var mixed = [1, "two", true, [10, 20]]
```

### Dictionaries

Dictionaries store key-value pairs.

```glorp
var user = {
    "name": "Gandalf",
    "class": "Wizard",
    "level": 20
}
```

### Lazy Ranges

A concise syntax for creating memory-efficient **lazy iterators** over a range of numbers.

```glorp
// An iterator from 1 to 10 (inclusive)
var my_range = [1, ..., 10]

// An iterator from 0 to 100 with a step of 5
var by_fives = [0, 5, ..., 100]
```

### Element Access

Access elements in lists and dictionaries using square brackets `[]`.

```glorp
fn Main() {
    var items = ["sword", "shield", "potion"]
    var first_item = items[0] // "sword"
    out(first_item, "\n")

    var user = {"name": "Aragorn"}
    var user_name = user["name"] // "Aragorn"
    out(user_name, "\n")
}
```

---

## 6. Control Flow

Glorp uses `{}` for multi-line bodies. For single-statement bodies, you can use `->` as a concise alternative.

### `if` / `elif` / `else`

`when` is a convenient alias for a single `if` statement.

```glorp
fn Main() {
    var score = 85
    if score > 90 -> out("Grade: A\n")
    elif score > 80 {
        out("Grade: B\n")
        out("Good job!\n")
    }
    else -> out("Keep trying!\n")
    when score == 10 -> out("Your score is ten")
}
```

### `switch`

A powerful alternative to `if-elif` chains, perfect for handling multiple distinct cases.

```glorp
fn Main() {
    var command = "go_north"
    switch command {
        "go_north" -> out("You move north.")
        "go_south" -> out("You move south.")
        else       -> out("Unknown command.")
    }
}
```

### `for` and `each` Loops

`for` loops are for numerical ranges. `each` is the idiomatic way to iterate over any collection.

```glorp
fn Main() {
    // For loop
    for i from 1 to 3 -> out(i, " ") //> 1 2 3
    out("\n")

    // Each loop
    var names = ["Frodo", "Sam", "Merry"]
    each name in names {
        out("Welcome, ", name, "!\n")
    }
}
```

---

## 7. Functions

### Declaration

Functions are first-class citizens. They can be defined in a short form for single expressions or a long form for block bodies.

```glorp
// Short form for a single expression
fn add(a, b) => a + b

// Long form for multiple statements
fn greet(name) {
    var message = "Hello, " + name + "!"
    out(message)
}

fn Main() {
    var sum = add(5, 3)
    out("Sum is: ", sum, "\n")
    greet("World")
}
```

### Named and Default Arguments

Functions support **named arguments** for clarity and **default values** with `else` for flexibility.

```glorp
fn setup(host, port else 8080, user else "guest") {
    out("Connecting to ", host, ":", port, " as ", user, "\n")
}

fn Main() {
    setup("glorp-lang.dev")                    // Uses both defaults
    setup("localhost", port: 9000)             // Overrides one default
    setup(user: "admin", host: "internal.net") // Use named args in any order
}
```

### Generators and `yield`

A function becomes a **generator** if it uses `->` inside its body to `yield` a value. Generators produce a sequence of values lazily.

```glorp
// This function generates the Fibonacci sequence infinitely.
fn fibonacci() {
    var a = 0
    var b = 1
    while true {
        -> a // Yield the current value
        var temp = a
        var a = b
        var b = temp + b
    }
}
```

You can also **take** any amount of elements from generator

```glorp
fn Main() -> out(take 20 from [1, 3, ..., Inf]) //[1.0, 3.0, 5.0, 7.0, 9.0, 11.0, 13.0, 15.0, 17.0, 19.0, 21.0, 23.0, 25.0, 27.0, 29.0, 31.0, 33.0, 35.0, 37.0, 39.0]
```

---

## 8. Modules and Error Handling

### Modules (`use`)

Split your code into multiple files. Glorp supports **hierarchical imports**. When you import `utils.http`, the module is available under the final name, `http`.

*File `main.glorp`:*
```glorp
use utils.math // Imports utils/math.glorp

fn Main() {
    // Use 'math', not 'utils.math'
    var result = math.add(10, 5)
    out(result)
}
```

### Error Handling (`try` / `catch` and `throw`)

Handle potential errors with `try/catch`. The error is captured in the special `exception` variable. Raise your own errors with `throw`.

```glorp
fn check_age(age) {
    if age < 18 -> throw "User is too young!"
    out("Access granted.")
}

fn Main() {
    try {
        check_age(15)
    }
    catch {
        out("An error occurred! Details: ", exception, "\n")
    }
}
```

---

## 9. Built-in Functions

Glorp provides a small but useful standard library of global functions.

| Function | Description |
|:---|:---|
| `out(...)` | Prints arguments to the console without a newline. |
| `clear()` | Clears the console screen. |
| `readfile(filename)` | Reads an entire file into a string. |
| `writefile(filename, content)`| Writes a string to a file. |
| `read(prompt?)` | Reads a line of text from the user. |
| `read_int(prompt?)` | Reads input and ensures it's a valid integer. |
| `read_float(prompt?)` | Reads input and ensures it's a valid float. |
| `read_bool(prompt?)` | Reads input and ensures it's a valid boolean. |
| `str(val)`, `int(val)`, etc. | Type conversion functions. |
