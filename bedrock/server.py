import http.server
import socketserver
import json
import urllib.parse
from bedrock.lexer import Lexer
from bedrock.parser import Parser
from bedrock.interpreter import Interpreter
from bedrock.ascii import ASCII_LOGO

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bedrock Language - Welcome & Quickstart</title>
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #121212;
            --bedrock-bg: #1e1e24;
            --bedrock-border: #4a4a5a;
            --mc-green: #55FF55;
            --mc-gold: #FFAA00;
            --mc-red: #FF5555;
            --mc-aqua: #55FFFF;
            --mc-gray: #AAAAAA;
            --mc-dark-gray: #555555;
            --panel-bg: #282830;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg-dark);
            background-image:
                radial-gradient(#2c2c36 15%, transparent 16%),
                radial-gradient(#2c2c36 15%, transparent 16%);
            background-size: 32px 32px;
            background-position: 0 0, 16px 16px;
            color: #ffffff;
            font-family: 'VT323', monospace;
            font-size: 22px;
            line-height: 1.4;
            padding: 20px;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
        }

        header {
            background: var(--panel-bg);
            border: 4px solid var(--bedrock-border);
            box-shadow: 6px 6px 0px #000000;
            padding: 24px;
            text-align: center;
            margin-bottom: 24px;
            position: relative;
        }

        .beta-badge {
            display: inline-block;
            background-color: var(--mc-gold);
            color: #000;
            font-family: 'Press Start 2P', cursive;
            font-size: 14px;
            padding: 6px 14px;
            border: 2px solid #fff;
            margin-top: 10px;
            letter-spacing: 2px;
            text-shadow: 1px 1px 0px #000;
        }

        pre.ascii-logo {
            font-family: monospace;
            font-size: 16px;
            color: var(--mc-green);
            line-height: 1.1;
            overflow-x: auto;
            text-shadow: 0 0 8px rgba(85, 255, 85, 0.4);
            margin-bottom: 12px;
        }

        h1 {
            font-family: 'Press Start 2P', cursive;
            font-size: 24px;
            color: var(--mc-gold);
            text-shadow: 3px 3px 0px #000;
            margin-bottom: 12px;
        }

        .subtitle {
            font-size: 24px;
            color: var(--mc-aqua);
        }

        .grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 24px;
        }

        @media(min-width: 768px) {
            .grid {
                grid-template-columns: 1fr 1fr;
            }
        }

        .card {
            background: var(--panel-bg);
            border: 4px solid var(--bedrock-border);
            box-shadow: 5px 5px 0px #000;
            padding: 20px;
        }

        .card h2 {
            font-family: 'Press Start 2P', cursive;
            font-size: 16px;
            color: var(--mc-gold);
            margin-bottom: 16px;
            border-bottom: 2px dashed var(--bedrock-border);
            padding-bottom: 8px;
        }

        .editor-container {
            grid-column: 1 / -1;
        }

        textarea#code-input {
            width: 100%;
            height: 220px;
            background: #15151a;
            color: var(--mc-green);
            font-family: 'VT323', monospace;
            font-size: 22px;
            border: 3px solid var(--bedrock-border);
            padding: 12px;
            outline: none;
            resize: vertical;
        }

        .btn-group {
            display: flex;
            gap: 12px;
            margin-top: 12px;
            flex-wrap: wrap;
        }

        button {
            font-family: 'Press Start 2P', cursive;
            font-size: 12px;
            padding: 12px 20px;
            background: #3a3a48;
            color: #fff;
            border: 3px solid #6e6e85;
            cursor: pointer;
            box-shadow: 3px 3px 0px #000;
            transition: all 0.1s ease;
        }

        button:hover {
            background: #4e4e60;
            border-color: var(--mc-gold);
        }

        button:active {
            transform: translate(2px, 2px);
            box-shadow: 1px 1px 0px #000;
        }

        button.primary {
            background: #2e6b2e;
            border-color: var(--mc-green);
            color: #ffffff;
        }

        button.primary:hover {
            background: #3e8b3e;
        }

        #console-output {
            background: #0d0d10;
            border: 3px solid #333;
            color: var(--mc-aqua);
            font-family: 'VT323', monospace;
            font-size: 20px;
            padding: 16px;
            min-height: 140px;
            max-height: 300px;
            overflow-y: auto;
            margin-top: 16px;
            white-space: pre-wrap;
        }

        .command-badge {
            background: #402818;
            color: var(--mc-gold);
            padding: 2px 8px;
            border: 1px solid var(--mc-gold);
            font-family: monospace;
            font-size: 18px;
        }

        ul {
            list-style: square;
            padding-left: 24px;
        }

        li {
            margin-bottom: 8px;
        }

        footer {
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: var(--mc-gray);
            font-size: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <pre class="ascii-logo">
  ____  _____ ____  ____   ____   ____  _  __
 | __ )| ____|  _ \|  _ \ / __ \ / ___|| |/ /
 |  _ \|  _| | | | | |_) | |  | | |    | ' /
 | |_) | |___| |_| |  _ <| |__| | |___ | . \
 |____/|_____|____/|_| \_\_/\____/\____|_|\_\
            </pre>
            <h1>BEDROCK LANGUAGE</h1>
            <div class="subtitle">Minecraft Bedrock Edition Inspired Programming Language</div>
            <div class="beta-badge">[ BETA VERSION 0.1.0 ]</div>
        </header>

        <div class="grid">
            <div class="card">
                <h2>🎮 WELCOME & THANKS!</h2>
                <p>Thank you for installing <strong>Bedrock</strong>! Bedrock brings the power, simplicity, and fun of Minecraft Bedrock Edition commands and redstone logic into a full-fledged scriptable programming language with <span class="command-badge">.bd</span> file format support.</p>
                <br>
                <p><strong>Features:</strong></p>
                <ul>
                    <li>Bedrock Commands: <code>say</code>, <code>give</code>, <code>summon</code>, <code>fill</code>, <code>tp</code>, <code>effect</code></li>
                    <li>Redstone Logic & Control Flow: <code>if</code>, <code>else</code>, <code>repeat</code>, <code>while</code></li>
                    <li>Functions, Variables, Arithmetic, Relative Coordinates (<code>~</code>)</li>
                    <li>CLI REPL & Execution Engine</li>
                </ul>
            </div>

            <div class="card">
                <h2>🚀 QUICKSTART</h2>
                <p>Execute your first <span class="command-badge">.bd</span> file from the command line:</p>
                <br>
                <pre style="background: #111; padding: 10px; color: var(--mc-green); border: 2px solid #444;">
# Run a Bedrock script
python3 -m bedrock run examples/hello.bd

# Launch Interactive REPL
python3 -m bedrock repl

# Display ASCII Logo & Version
python3 -m bedrock version
                </pre>
            </div>

            <div class="card editor-container">
                <h2>⚡ INTERACTIVE .BD PLAYGROUND</h2>
                <p>Write Bedrock script below and click <strong>RUN CODE</strong> to test the interpreter live!</p>
                <br>
                <textarea id="code-input"># Bedrock Interactive Demo Script (.bd)
say "Welcome to Minecraft Bedrock Scripting!"

var player = "@p"
var redstone_power = 15

give player "diamond_sword" 1
effect player "speed" 30 2

if redstone_power == 15 {
    say "Redstone Comparator Active! Signal Strength: " + redstone_power
}

function spawn_guards(count) {
    say "Summoning " + count + " Iron Golems!"
    repeat count {
        summon "iron_golem" ~ ~ ~
    }
}

spawn_guards(2)
</textarea>
                <div class="btn-group">
                    <button class="primary" onclick="runBedrockCode()">▶ RUN CODE</button>
                    <button onclick="loadSample('hello')">Sample: Hello</button>
                    <button onclick="loadSample('redstone')">Sample: Redstone</button>
                    <button onclick="loadSample('builder')">Sample: Shelter Builder</button>
                    <button onclick="clearConsole()">Clear Output</button>
                </div>

                <div id="console-output">Output console will display command block & script execution output here...</div>
            </div>
        </div>

        <footer>
            Bedrock Language Engine v0.1.0-beta | File Format Extension: .bd
        </footer>
    </div>

    <script>
        const samples = {
            hello: `# hello.bd
say "Hello from Bedrock Language!"
give @p "golden_apple" 5
print "Quickstart demo executed successfully!"`,
            redstone: `# redstone_counter.bd
var signal = 0
while signal <= 15 {
    print "Redstone wire level: " + signal
    if signal == 15 {
        say "Redstone Lamp Lit!"
    }
    signal = signal + 5
}`,
            builder: `# house_builder.bd
say "Building Bedrock shelter structure..."
fill ~0 ~0 ~0 ~10 ~5 ~10 "stone_bricks"
fill ~1 ~1 ~1 ~9 ~4 ~9 "air"
fill ~5 ~1 ~0 ~5 ~2 ~0 "oak_door"
say "Structure complete!"`
        };

        function loadSample(name) {
            if (samples[name]) {
                document.getElementById('code-input').value = samples[name];
            }
        }

        function clearConsole() {
            document.getElementById('console-output').textContent = 'Console cleared.';
        }

        async function runBedrockCode() {
            const code = document.getElementById('code-input').value;
            const consoleBox = document.getElementById('console-output');
            consoleBox.textContent = 'Executing script...';

            try {
                const response = await fetch('/api/run', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ code: code })
                });
                const data = await response.json();
                if (data.error) {
                    consoleBox.style.color = '#FF5555';
                    consoleBox.textContent = 'Error: ' + data.error;
                } else {
                    consoleBox.style.color = '#55FFFF';
                    consoleBox.textContent = data.output.join('\n') || 'Script executed with no output.';
                }
            } catch (err) {
                consoleBox.style.color = '#FF5555';
                consoleBox.textContent = 'Network or server error: ' + err.message;
            }
        }
    </script>
</body>
</html>
"""

class BedrockHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode("utf-8"))
        else:
            self.send_error(404, "Page Not Found")

    def do_POST(self):
        if self.path == "/api/run":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            try:
                payload = json.loads(post_data)
                code = payload.get("code", "")

                output_logs = []
                lexer = Lexer(code)
                tokens = lexer.tokenize()
                parser = Parser(tokens)
                ast = parser.parse()
                interpreter = Interpreter(output_callback=output_logs.append)
                interpreter.eval(ast)

                response_data = {"output": output_logs}
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode("utf-8"))
            except Exception as e:
                response_data = {"error": str(e)}
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode("utf-8"))
        else:
            self.send_error(404, "Endpoint Not Found")

def run_server(port=8000):
    handler = BedrockHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Bedrock Welcome Web Server running on http://localhost:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    run_server()
