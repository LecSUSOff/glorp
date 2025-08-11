<br/>
<p align="center">
  <h1 align="center">Glorp Programming Language</h1>
  <p align="center">
    An expressive, reactive, and Python-interoperable language that transpiles to clean Python.
    <br/>
    <br/>
    <a href="https://glorp.readthedocs.io/en/latest/"><strong>Explore the Docs »</strong></a>
    <br/>
    <br/>
    <a href="https://github.com/LecSUSOff/glorp/issues">Report Bug</a>
    ·
    <a href="https://github.com/LecSUSOff/glorp/issues">Request Feature</a>
  </p>
</p>

<p align="center">
  <!-- Badges -->
  <a href="https://discord.gg/nbNMvvc9"><img src="https://img.shields.io/discord/YOUR_SERVER_ID?logo=discord&label=Discord" alt="Discord"></a>
  <a href="https://glorp.readthedocs.io/en/latest/"><img src="https://img.shields.io/readthedocs/glorp" alt="Documentation Status"></a>
  <a href="https://github.com/LecSUSOff/glorp/blob/main/LICENSE"><img src="https://img.shields.io/github/license/LecSUSOff/glorp" alt="License"></a>
  <a href="https://github.com/LecSUSOff/glorp/actions/workflows/ci.yml"><img src="https://github.com/LecSUSOff/glorp/actions/workflows/ci.yml/badge.svg" alt="Build Status"></a>
</p>

---

## About Glorp

Glorp is a modern programming language designed for productivity and developer happiness. It combines an expressive, clean syntax with powerful features like first-class reactivity and seamless Python library integration.

At its core, Glorp is a **transpiled language**. It takes your `.glorp` source code and converts it into highly readable and efficient Python, giving you the performance and reliability of a mature ecosystem with the benefits of a cutting-edge syntax.

The core philosophies are:
*   **Write Expressive Code**: Focus on your logic with an intuitive syntax that reduces boilerplate.
*   **Leverage Python's Power**: Don't reinvent the wheel. Use any Python library (`numpy`, `requests`, `Django`) with a single line of code.
*   **Embrace Reactivity**: Build event-driven and reactive applications effortlessly with the built-in `watch` statement.

## Key Features

✨ **Seamless Python Interop**: Use any Python library as if it were native to Glorp.
```glorp
use py.numpy as np

fn null Main() {
    arr = np.array([1, 2, 3])
    out(arr)
}
```

⚡ **Built-in Reactivity**: Create variables that execute code when their value changes.
```glorp
watch score = 0 {
    out("New score: " + score)
}
score = 100 // Prints "New score: 100"
```

💎 **Modern, Concise Syntax**: Enjoy features like immutable declarations (`:=`), list comprehensions, and powerful `switch` statements.
```glorp
// Create a new list of squared even numbers
evens_squared = [each n in [1,2,3,4] where n % 2 == 0 -> n ^ 2]
```

🛡️ **Built-in Safety**: The division operator (`/`) handles division-by-zero by returning `Infinity`, preventing common runtime crashes.

📦 **Simple Tooling**: A single command-line tool handles running, transpiling, and debugging your code.

## Getting Started

### Installation

1.  Download the latest `glorp.exe` from the [Releases page](https://github.com/LecSUSOff/glorp/releases).
2.  Place the executable in a permanent folder (e.g., `C:\Glorp` or `~/bin/glorp`).
3.  Add this folder to your system's `PATH` environment variable.

Verify the installation by opening a new terminal and running:
```sh
glorp --version
```

### Your First Program

1.  Create a file named `hello.glorp`:

```glorp
// All programs start with the Main function
fn Main() {
    out("Hello from Glorp!")
}
```

2.  Run it from your terminal:

```sh
glorp run hello.glorp
```
**Output:**
```
Hello from Glorp!
```

## Community & Documentation

Join our community and dive into the official documentation to learn more about Glorp's features.

[**Join our Discord Server**](https://discord.gg/nbNMvvc9)

[**Read the Full Documentation**](https://glorp.readthedocs.io/en/latest/)

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.