Welcome to the Glorp programming language! Glorp is a modern, multi-paradigm language designed to be expressive, powerful, and a joy to use. It combines the best features from various languages into a single, cohesive syntax, all while running on the robust and battle-tested Python runtime.

## Core Philosophy

Glorp is built on three foundational principles:

1.  **Expressive & Modern Syntax:** Writing code should be intuitive. Glorp provides a clean and concise syntax that gets out of your way. With features like the `:=` operator for immutability, powerful list comprehensions, and clear control flow structures like `switch`, your code can be both readable and efficient.

2.  **Seamless Python Interoperability:** Why reinvent the wheel? Glorp embraces the vast Python ecosystem. You can import and use any Python library with a single line: `use py.numpy`. This gives you immediate access to powerful tools for data science, web development, and more, directly within your Glorp code.

3.  **Built-in Reactive Capabilities:** Modern applications often need to react to changes in data. Glorp makes this easy with the built-in `watch` keyword. You can create variables that automatically trigger code whenever their value is updated, simplifying event-driven and reactive programming without needing external libraries.

## Key Features at a Glance

Glorp is packed with features designed for modern software development. Here are just a few you'll learn about in this documentation:

*   **Flexible Variables:** Choose between standard mutable variables (`=`) and concise, clear immutable constants (`:=`).
*   **Object-Oriented Programming:** Full support for classes, inheritance, and properties.
*   **Built-in Module System:** Organize your code into reusable modules with the `use` keyword.
*   **Advanced Control Flow:** Go beyond simple `if/else` with `when` for single conditions and a powerful `switch` statement for matching against multiple values.
*   **First-Class Functions:** Use functions as variables, pass them as arguments, and even create lightweight anonymous `lambda` functions.
*   **Generator Support:** Create efficient iterators with the `>>` (yield) operator.
*   **Built-in Safety:** A division operator that handles division-by-zero errors gracefully by returning infinity.
*   **Simple Tooling:** A single command-line tool, `glorp`, handles running, transpiling, and debugging your code.