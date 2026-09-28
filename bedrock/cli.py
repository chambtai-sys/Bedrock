import sys
import argparse
from bedrock.lexer import Lexer
from bedrock.parser import Parser
from bedrock.interpreter import Interpreter
from bedrock.ascii import ASCII_HEADER, ASCII_LOGO

def run_code(source_code: str, output_callback=None):
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter(output_callback=output_callback)
    interpreter.eval(ast)
    return interpreter.output_logs

def main():
    parser = argparse.ArgumentParser(description="Bedrock Programming Language CLI")
    subparsers = parser.add_subparsers(dest="command")

    # run subcommand
    run_parser = subparsers.add_parser("run", help="Run a Bedrock (.bd) file")
    run_parser.add_argument("filename", help="Path to .bd script file")

    # version subcommand
    subparsers.add_parser("version", help="Show Bedrock version and ASCII logo")

    # repl subcommand
    subparsers.add_parser("repl", help="Start interactive Bedrock REPL")

    # serve subcommand
    serve_parser = subparsers.add_parser("serve", help="Start the Bedrock Welcome web server")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port to serve on")

    args = parser.parse_args()

    if args.command == "version" or len(sys.argv) == 1:
        print(ASCII_HEADER)
        return

    if args.command == "run":
        try:
            with open(args.filename, "r", encoding="utf-8") as f:
                code = f.read()
            run_code(code)
        except Exception as e:
            print(f"Error executing {args.filename}: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "repl":
        print(ASCII_LOGO)
        print("Bedrock Interactive REPL v0.1.0-beta (.bd)")
        print("Type 'exit' or 'quit' to exit.\n")
        interpreter = Interpreter()
        while True:
            try:
                line = input("bedrock> ")
                if line.strip() in ("exit", "quit"):
                    break
                if not line.strip():
                    continue
                lexer = Lexer(line)
                tokens = lexer.tokenize()
                p = Parser(tokens)
                ast = p.parse()
                res = interpreter.eval(ast)
                if res is not None:
                    print(res)
            except Exception as e:
                print(f"Error: {e}")

    elif args.command == "serve":
        from bedrock.server import run_server
        run_server(port=args.port)

if __name__ == "__main__":
    main()
