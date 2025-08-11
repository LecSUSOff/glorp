This chapter will guide you through writing and running your very first Glorp program. By the end, you will know how to create a script, compile it, and see the output on your screen.

## Installation

Getting Glorp running on your system is straightforward. There's no complex installer:

1.  Place the `glorp.exe` file in a dedicated folder (e.g., `C:\Glorp`).
2.  Add this folder to your system's `PATH` environment variable. This allows you to run the `glorp` command from any directory in your terminal.

To verify the installation, open a new terminal or command prompt and type:

```sh
glorp --version
```

If it's set up correctly, you will see the Glorp version number printed.

## Your First Program: "Hello, World!"

All programs need an entry point—the place where execution begins. In Glorp, this is a special function called `Main`.

Let's create a "Hello, World!" program.

1.  Create a new file named `hello.glorp`.
2.  Open it in your favorite text editor and add the following code:

```glorp
// Your first Glorp program!
fn Main() {
    out("Hello, World!")
}
```

Let's break this down:
*   `//`: This is a single-line comment, ignored by the program.
*   `fn Main() { ... }`: This defines the main function. The code inside the curly braces `{}` is the function's body.
*   `out(...)`: This is a built-in function that prints text to the console.

## How to Run a Glorp Script

Running your script is done using the `glorp` command in your terminal.

1.  Navigate to the directory where you saved `hello.glorp`.
2.  Run the following command:

```sh
glorp run hello.glorp
```

You will see the following output on your screen:

```
Hello, World!
```

Congratulations! You have successfully written and executed your first Glorp program.

## The `Main` Entry Point

The `Main` function is essential. The Glorp runtime looks for this specific function by name and executes it to start your program. Every executable Glorp script must have a `fn Main()`.

As you'll see in later chapters, `Main` can also accept command-line arguments, allowing you to build powerful command-line tools.

With the basics of running a script covered, you're ready to dive into the fundamental building blocks of the language in the next chapter.