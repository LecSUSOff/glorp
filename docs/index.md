# The Glorp Programming Language Documentation

Welcome to the official documentation for the Glorp programming language. This guide provides a comprehensive overview, from basic syntax to advanced features.

## Table of Contents
1.  [Introduction to Glorp](#chapter-1-introduction-to-glorp)
2.  [Getting Started](#chapter-2-getting-started)
3.  [Language Basics](#chapter-3-language-basics)
4.  [Control Flow](#chapter-4-control-flow)
5.  [Data Structures](#chapter-5-data-structures)
6.  [Functions](#chapter-6-functions)
7.  [Object-Oriented Programming](#chapter-7-object-oriented-programming)
8.  [Modules and Scope](#chapter-8-modules-and-scope)
9.  [Advanced Features](#chapter-9-advanced-features)
10. [The Command-Line Tool](#chapter-10-the-command-line-tool)

---

## Chapter 1: Introduction to Glorp

Glorp is a modern, multi-paradigm language designed to be expressive, powerful, and a joy to use. It combines the best features from various languages into a single, cohesive syntax, all while running on the robust and battle-tested Python runtime.

### Core Philosophy

1.  **Expressive & Modern Syntax**: Writing code should be intuitive. Glorp provides a clean and concise syntax that gets out of your way. With features like the `:=` operator for immutability and powerful list comprehensions, your code can be both readable and efficient.
2.  **Seamless Python Interoperability**: Glorp embraces the vast Python ecosystem. You can import any Python library with a single line (`use py.numpy`), giving you immediate access to powerful tools.
3.  **Built-in Reactive Capabilities**: The built-in `watch` keyword allows you to create variables that automatically trigger code whenever their value changes, simplifying event-driven programming.

### Key Features at a Glance

*   **Flexible Variables**: Choose between standard mutable variables (`=`) and concise, clear immutable constants (`:=`).
*   **Object-Oriented Programming**: Full support for classes, inheritance, and properties.
*   **Built-in Module System**: Organize your code into reusable modules with the `use` keyword.
*   **Advanced Control Flow**: Go beyond simple `if/else` with `when` for single conditions and a powerful `switch` statement.
*   **First-Class Functions**: Use functions as variables, pass them as arguments, and create anonymous `lambda` functions.
*   **Built-in Safety**: A division operator (`/`) that handles division-by-zero errors gracefully by returning infinity.
*   **Simple Tooling**: A single command-line tool, `glorp`, handles running, transpiling, and debugging your code.

---

## Chapter 2: Getting Started

This chapter guides you through writing and running your first Glorp program.

### Installation

Getting Glorp running on your system is straightforward. There's no complex installer:

1.  Place the `glorp.exe` file in a dedicated folder (e.g., `C:\Glorp`).
2.  Add this folder to your system's `PATH` environment variable. This allows you to run the `glorp` command from any terminal.

To verify the installation, open a new terminal and type `glorp --version`.

### Your First Program: "Hello, World!"

All programs need an entry point—the place where execution begins. In Glorp, this is a special function called `Main`.

1.  Create a new file named `hello.glorp`.
2.  Add the following code:

```glorp
// Your first Glorp program!
fn Main() {
    out("Hello, World!")
}
```
*   `//`: This is a single-line comment.
*   `fn Main() { ... }`: This defines the main function where the program starts.
*   `out(...)`: This is a built-in function that prints text to the console.

### How to Run a Glorp Script

1.  Navigate to the directory where you saved `hello.glorp`.
2.  Run the following command in your terminal:
    ```sh
    glorp run hello.glorp
    ```
3.  You will see the output: `Hello, World!`

Congratulations! You have successfully executed your first Glorp program.

---

## Chapter 3: Language Basics

This chapter covers the fundamental building blocks of Glorp.

### Comments

Comments are ignored by the program and are used for notes and explanations.

```glorp
// This is a single-line comment.

/*
  This is a
  multi-line comment block.
*/
```

### Variables and Immutability

Glorp has two kinds of variables: mutable (can be changed) and immutable (cannot be changed).

**Mutable Variables** are declared with `=`.

```glorp
x = 100 // x is 100
x = 150 // x is now 150
```

**Immutable Variables** (constants) are declared using `:=`. This is the preferred shorthand.

```glorp
PI := 3.14159 // PI is immutable and cannot be reassigned
```

For clarity, you can also use the `immutable` keyword, which is equivalent to `:=`:
`immutable PI = 3.14159`
`immutable PI := 3.14159`

### Primitive Data Types

*   **num**: Represents both integers and floating-point numbers (`10`, `42.5`).
*   **str**: Represents text, enclosed in double quotes (`"Hello"`).
*   **bool**: Represents `true` or `false`.
*   **null**: Represents the absence of a value.

### Basic Operators

| Operator | Description           | Example          |
| :------- | :-------------------- | :--------------- |
| `+`, `-`, `*` | Addition, Subtraction, Multiplication | `5 + 2` is `7` |
| `^`      | Power / Exponent      | `2 ^ 3` is `8`   |
| `==`, `!=` | Equal to, Not equal to | `x == y`         |
| `>`, `<`, `>=`, `<=` | Greater than, Less than, etc. | `x > 5`          |

### Console I/O

Glorp provides built-in functions to interact with the console.

*   `out(value)`: Prints a value to the console.
*   `read(prompt)`: Reads a line of text from the user.
*   `read_int(prompt)`: Reads input and ensures it is an integer.
*   `read_float(prompt)`: Reads input and ensures it is a number.

---

## Chapter 4: Control Flow

Control flow statements direct the order in which code is executed.

### `if` / `elif` / `else`

These are used for standard conditional logic.

```glorp
score = 85
if score > 90 {
    out("Grade: A")
} elif score > 75 {
    out("Grade: B")
} else {
    out("Grade: C or lower")
}
```

### `when`

For a single condition, `when` offers a more concise syntax than `if`.

```glorp
isLoggedIn = true
when isLoggedIn -> out("Welcome back!")
```

### `switch` / `case`

The `switch` statement checks a value against a series of `case` blocks.

```glorp
day = "Monday"
switch day {
    case "Saturday"
    case "Sunday" {
        out("It's the weekend!")
    }
    case "Monday" {
        out("Back to work.")
    }
    else {
        out("It's a weekday.")
    }
}
```

### Loops

**`while` Loop**: Repeats a block of code as long as a condition is `true`.
```glorp
count = 0
while count < 3 {
    out(count)
    count = count + 1
}
```

**`for` Loop**: Iterates over a numerical range. The `up` and `down` keywords are optional for readability.
```glorp
// Loop from 1 up to 5
for i from 1 to 5 {
    out(i)
}

// Loop from 10 down to 7
for i from 10 down to 7 {
    out(i)
}
```

**`each` Loop**: Iterates over the elements of a collection (like a list).
```glorp
myList = [10, 20, 30]
each item in myList {
    out(item)
}
```

---

## Chapter 5: Data Structures

Glorp provides powerful built-in structures for handling collections of data.

### Lists

A list is an ordered collection of items, created with `[]`.

```glorp
fruits = ["apple", "banana", "cherry"]
out(fruits[0]) // Access first item: "apple"

// Modify an item
fruits[1] = "blueberry"
```

### Dictionaries

A dictionary is a collection of key-value pairs, created with `{}`.

```glorp
person = {"name": "John", "age": 30}
out(person["name"]) // Access value by key: "John"```

### Numerical Ranges

You can create numerical ranges directly. These are useful in `for` loops or `switch` statements.

```glorp
// A simple range from 1 to 5
one_to_five = [1, ..., 5]

// A range from 10 to 30 with a step of 5
stepped_range = [10, 15, ..., 30]
```

### List Comprehensions (`quick_foreach`)

This is a powerful feature for creating a new list by transforming or filtering another list.

```glorp
numbers = [1, 2, 3, 4, 5, 6]

// Create a new list of squared even numbers
squaredEvens = [each n in numbers where n % 2 == 0 -> n ^ 2]
// Result: [4, 16, 36]
```

### The `take` Statement

The `take` statement allows you to get a specific number of items from the beginning of a list or iterable.

```glorp
letters = ["a", "b", "c", "d", "e"]
first_three = take 3 from letters
// Result: ["a", "b", "c"]```

---

## Chapter 6: Functions

Functions are reusable blocks of code that perform a specific task.

### Defining Functions

Functions are defined with the `fn` keyword.

```glorp
fn greet(name) {
    => "Hello, " + name
}

message = greet("Alice") // message is "Hello, Alice"
```

### Parameters and Default Values

You can provide default values for parameters using `else`.

```glorp
fn say(message else "Default message") {
    out(message)
}

say("Explicit message") // Prints "Explicit message"
say() // Prints "Default message"
```

### Returning Values

Use `=>` for a concise, single-expression return, or the `return` keyword for more complex logic.

```glorp
fn add(a, b) => a + b // Concise return

fn check(num) {
    if num < 0 {
        return "Negative"
    }
    return "Positive or Zero"
}
```

### Lambda Expressions

You can create small, anonymous functions on the fly.

```glorp
// A lambda that adds two numbers
adder = (a, b) -> a + b
out(adder(5, 3)) // Prints 8

// You can also call it immediately
out( ( (x) -> x * 2)(10) ) // Prints 20
```

### Generator Functions (`>>`)

A generator function produces a sequence of values one at a time using the `>>` (yield) operator, which is more memory-efficient than returning a full list.

```glorp
fn count_to(max) {
    i = 0
    while i < max {
        >> i // Yield the current value
        i = i + 1
    }
}

// Use the generator in a loop
each number in count_to(3) {
    out(number) // Prints 0, then 1, then 2
}
```

---

## Chapter 7: Object-Oriented Programming

Glorp supports classes, making it easy to model real-world objects.

### Defining Classes

Use the `class` keyword to define a new type.

```glorp
class Dog {
    fn bark() {
        out("Woof!")
    }
}

myDog = Dog()
myDog.bark() // Prints "Woof!"
```

### Constructors

A constructor is automatically created based on parameters in the class definition.

```glorp
class Person(name, age) {
    // name and age are automatically assigned as self.name and self.age
}

p = Person("Alice", 30)
out(p.name) // Prints "Alice"
```

### Properties (`prop`)

Properties look like fields but are computed by a function. They are useful for derived data.

```glorp
class Circle(radius) {
    prop diameter {
        => this.radius * 2
    }
}

c = Circle(10)
out(c.diameter) // Prints 20. Note: no parentheses!```

### Inheritance

A class can inherit methods and properties from another class.

```glorp
class Animal(name) {
    fn speak() => "I am an animal"
}

class Cat(name) : Animal {
    // The Cat class now has a 'name' and a 'speak' method
}

myCat = Cat("Whiskers")
out(myCat.speak()) // Prints "I am an animal"
```

### The `this` Keyword

Inside a class method or property, `this` refers to the current instance of the object.

---

## Chapter 8: Modules and Scope

Organize your project and control variable visibility.

### Glorp Modules

You can split your code into multiple `.glorp` files and import them as modules.

Suppose you have `utils.glorp`:
```glorp
// In utils.glorp
fn sayHi() => "Hi there!"
```

In your main file:
```glorp
// In main.glorp
use utils

fn Main() {
    out(utils.sayHi()) // Prints "Hi there!"
}
```
You can also assign an alias: `use utils for u`.

### Using Python Libraries

Import any Python library using the `use py.` prefix.

```glorp
use py.math
use py.random as rnd // Give it an alias

fn Main() {
    out(math.sqrt(16)) // Prints 4.0
    out(rnd.randint(1, 100)) // Prints a random number
}
```

### Variable Scope

**`private`**: Variables marked as `private` are only accessible within their module. This is enforced by name mangling, which makes accidental access from outside the module difficult.

```glorp
private secret = "my-secret-key" // Internal to this file
```

**`global`**: To modify a global variable from within a function, you must declare your intent with the `global` keyword.

```glorp
count = 0
fn increment() {
    global count
    count = count + 1
}```

---

## Chapter 9: Advanced Features

Explore some of the most powerful and unique features of Glorp.

### Reactive Programming with `watch`

The `watch` statement creates a variable that executes a code block whenever its value changes.

```glorp
fn Main() {
    watch score = 0 {
        out("Score changed! New score: " + score)
    }

    score = 10 // Prints: Score changed! New score: 10
    score = 25 // Prints: Score changed! New score: 25
    score = 25 // Does nothing, as the value is the same
}
```

### Structured Data with `container`

A `container` is a way to define a new type that holds a set of unique, related "field" types. It's useful for creating state machines or algebraic data types.

```glorp
container NetworkState {
    Loading,
    Success,
    Error
}

fn handleState(state) {
    switch state {
        case NetworkState.Loading { out("Fetching data...") }
        case NetworkState.Success { out("Data loaded!") }
    }
}

handleState(NetworkState.Loading)
```

### Error Handling (`try`, `catch`, `throw`)

Handle potential errors gracefully without crashing your program.

```glorp
fn mightFail(value) {
    if value < 0 {
        throw "Value cannot be negative!"
    }
    => 100 / value
}

try {
    result = mightFail(-5)
} catch {
    out("An error occurred: " + exception)
}
```

### Special Operators

*   **Safe Division (`/`)**: To prevent crashes, dividing by zero returns `Infinity`.
    ```glorp
    out(10 / 0) // Prints Infinity
    ```
*   **Integer Division (`%`)**: Performs floor division.
    ```glorp
    out(10 % 3) // Prints 3
    ```

---

## Chapter 10: The Command-Line Tool

The `glorp` executable is your main interface for working with Glorp files.

*   `glorp run <file.glorp>`
    Compiles and immediately runs your script. This is the most common command.

*   `glorp to-py <file.glorp>`
    Translates your Glorp code into a `.py` file without executing it. This is useful for inspection or for distributing Python source code.

*   `glorp run <file.glorp> -d`
    The `-d` (debug) flag prints the generated Python code to the console before running it.

*   `glorp run <file.glorp> -t`
    The `-t` (tree) flag displays the parsed Abstract Syntax Tree (AST) of your program.

*   `glorp run <file.glorp> -o`
    The `-o` (output) flag shows performance metrics, such as how long the code took to transpile and execute.