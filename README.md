```
  ____  _____ ____  ____   ____   ____  _  __
 | __ )| ____|  _ \|  _ \ / __ \ / ___|| |/ /
 |  _ \|  _| | | | | |_) | |  | | |    | ' /
 | |_) | |___| |_| |  _ <| |__| | |___ | . \
 |____/|_____|____/|_| \_\_/\____/\____|_|\_\
                [ B E T A ]
```

# Bedrock Programming Language

**Bedrock** is an expressive, lightweight, Minecraft Bedrock Edition-inspired programming language designed for scripting, command block automation, redstone logic simulation, and game mechanics.

With native support for the **`.bd`** file extension, Bedrock provides a clean syntax that bridges familiar Minecraft commands (`say`, `summon`, `give`, `fill`, `tp`, `effect`) with standard programming constructs like variables, loops, conditionals, functions, and math operations.

---

## 🌟 Key Features

- **File Format:** Native **`.bd`** script files.
- **ASCII Logo & Beta Label:** Official CLI and Web branding with `[ BETA ]` badge.
- **Minecraft Command Block Integration:** Built-in commands (`say`, `give`, `summon`, `fill`, `tp`, `effect`) and relative coordinates (`~`, `~10`).
- **Redstone Logic & Control Flow:** Control loops (`repeat`, `while`) and conditional logic (`if`, `else`, `execute if`).
- **Functions & Data Structures:** Functions with parameters/return values, variables (`var`), arrays, and strings.
- **Interactive Web UI:** "Thanks for Installing" welcome website with a live interactive playground.
- **CLI Utilities:** Built-in runner, REPL shell, and web server commands.

---

## 🚀 Quickstart & Installation

Clone the repository and run Bedrock scripts using Python 3:

```bash
# Display ASCII Logo and Version
python3 -m bedrock version

# Run a Bedrock script file (.bd)
python3 -m bedrock run examples/hello.bd

# Launch Interactive REPL
python3 -m bedrock repl

# Start Welcome / Thanks for Installing Web Server
python3 -m bedrock serve --port 8000
```

---

## 📜 `.bd` File Syntax Overview

### 1. Basic Commands & Say
```bedrock
# hello.bd
say "Welcome to Minecraft Bedrock Scripting!"
var player = "@p"

give player "diamond_sword" 1
effect player "speed" 30 2
```

### 2. Redstone Logic & Loops
```bedrock
# redstone.bd
var signal_strength = 0

while signal_strength <= 15 {
    print "Redstone Wire Signal: " + signal_strength
    if signal_strength == 15 {
        say "Redstone Comparator Powered!"
    }
    signal_strength = signal_strength + 5
}
```

### 3. Structure Building & Relative Coordinates
```bedrock
# house_builder.bd
say "Building shelter..."
fill ~0 ~0 ~0 ~10 ~5 ~10 "stone_bricks"
fill ~1 ~1 ~1 ~9 ~4 ~9 "air"
fill ~5 ~1 ~0 ~5 ~2 ~0 "oak_door"
say "Shelter complete!"
```

### 4. Functions & Mob Spawning
```bedrock
# mob_spawner.bd
function spawn_guard(mob_type, count) {
    say "Summoning " + count + " " + mob_type
    repeat count {
        summon mob_type ~ ~ ~
    }
}

spawn_guard("iron_golem", 2)
```

---

## 💻 Welcome Web Application

Bedrock includes a built-in web server with Minecraft Bedrock UI styling, command block console output, syntax documentation, and a live code execution playground.

To launch the web interface:
```bash
python3 -m bedrock serve --port 8000
```
Then visit `http://localhost:8000` in your web browser!

---

## 🧪 Running Tests

Run the complete unittest test suite for Bedrock:
```bash
python3 -m unittest discover -s tests
```

---

## 📄 License
MIT License. Inspired by Minecraft Bedrock Edition.
