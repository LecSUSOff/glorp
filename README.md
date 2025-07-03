<div align="center">

# Glorp 🦉

**A simple, statically-typed language with built-in reactivity.**

<p>
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
  </a>
  <a href="CONTRIBUTING.md">
    <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome">
  </a>
</p>

</div>

Glorp combines the safety of static types with a clean, modern syntax. Its killer feature is the `watch` keyword, allowing you to build reactive, event-driven applications with zero boilerplate.

For better experience, join our [**Discord**](https://discord.gg/nbNMvvc9) community

---

### Core Features

-   ✅ **Simple & Clean Syntax:** Write readable code, free from clutter.
-   🔒 **Static Typing:** Catch errors before you run, not after.
-   ✨ **Built-in Reactivity:** Use `watch` to create code that magically responds to data changes.

---

## 🚀 Getting Started

Get up and running in less than a minute.

#### 1. Download

Grab the latest `glorp` executable from the [**Releases**](https://github.com/LecSUSOff/glorp/releases) page.

#### 2. Install

Place the downloaded file in a directory and add it to your system's `PATH`. This allows you to run `glorp` from anywhere.

#### 3. Verify

Open a new terminal and check that it's working:
```bash
glorp --version
```

---

## Hello, Glorp!

Let's write your first program.

**Create `main.glorp`:**
```glorp
// The Main function is the entry point of your program
fn Null Main() {
    out("Hello, World!")
}
```

**Run it:**
```bash
glorp main.glorp
```

**Output:**
```
Hello, World!
```

---

## ✨ The Power of `watch`

This is where Glorp truly shines. The `watch` keyword lets you execute code whenever a variable's value changes.

**Create `counter.glorp`:**
```glorp
fn Null Main() {
    // This block will run automatically every time 'counter' is updated
    watch Int counter = 0 -> {
        out("Counter changed to: ", counter)
    }

    out("Starting...")

    // The 'watch' block triggers on each of these lines
    let Int counter = 1
    let Int counter = 2
    let Int counter = 3

    out("Finished!")
}
```

**Run it:**
```bash
glorp counter.glorp
```

**Output:**
```
Starting...
Counter changed to: 1
Counter changed to: 2
Counter changed to: 3
Finished!
```
*Notice how the reactive block was triggered automatically on each assignment. No callbacks, no boilerplate.*

## 🗺️ Roadmap

Glorp is actively developed. Here's what's next:

-   [ ] Better and more helpful error messages.
-   [ ] A core standard library (string utils, file I/O).
-   [ ] Syntax highlighting for VS Code.

## ❤️ Contributing

Contributions are welcome!

-   **Find a bug?** Open an [Issue](https://github.com/LecSUSOff/glorp/issues).
-   **Have an idea?** Start a [Discussion](https://github.com/LecSUSOff/glorp/discussions).
-   **Want to code?** Fork the repo and submit a **Pull Request**.

This project is licensed under the MIT License.
