from bedrock.tokens import TokenType, Token

KEYWORDS = {
    "say": TokenType.SAY,
    "var": TokenType.VAR,
    "set": TokenType.SET,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "execute": TokenType.EXECUTE,
    "run": TokenType.RUN,
    "repeat": TokenType.REPEAT,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "in": TokenType.IN,
    "function": TokenType.FUNCTION,
    "return": TokenType.RETURN,
    "give": TokenType.GIVE,
    "summon": TokenType.SUMMON,
    "tp": TokenType.TP,
    "fill": TokenType.FILL,
    "effect": TokenType.EFFECT,
    "redstone": TokenType.REDSTONE,
    "print": TokenType.PRINT,
    "true": TokenType.BOOLEAN,
    "false": TokenType.BOOLEAN,
    "and": TokenType.AND,
    "or": TokenType.OR,
    "not": TokenType.NOT,
}

class LexerError(Exception):
    pass

class Lexer:
    def __init__(self, source_code: str):
        self.source = source_code
        self.pos = 0
        self.line = 1
        self.column = 1

    def peek(self, offset: int = 0) -> str:
        idx = self.pos + offset
        if idx >= len(self.source):
            return ""
        return self.source[idx]

    def advance(self) -> str:
        ch = self.peek()
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def tokenize(self) -> list[Token]:
        tokens = []

        while self.pos < len(self.source):
            ch = self.peek()

            # Skip spaces/tabs
            if ch in (" ", "\t", "\r"):
                self.advance()
                continue

            # Handle comments (# or //)
            if ch == "#" or (ch == "/" and self.peek(1) == "/"):
                while self.pos < len(self.source) and self.peek() != "\n":
                    self.advance()
                continue

            # Newline
            if ch == "\n":
                line_no = self.line
                col_no = self.column
                self.advance()
                tokens.append(Token(TokenType.NEWLINE, "\n", line_no, col_no))
                continue

            # String literals
            if ch in ('"', "'"):
                quote = ch
                start_line = self.line
                start_col = self.column
                self.advance() # consume quote
                val = []
                while self.pos < len(self.source) and self.peek() != quote:
                    if self.peek() == "\\" and self.peek(1) in ('"', "'", "\\", "n", "t"):
                        self.advance()
                        escaped = self.advance()
                        if escaped == "n":
                            val.append("\n")
                        elif escaped == "t":
                            val.append("\t")
                        else:
                            val.append(escaped)
                    else:
                        val.append(self.advance())
                if self.pos >= len(self.source):
                    raise LexerError(f"Unterminated string literal at line {start_line}, col {start_col}")
                self.advance() # consume closing quote
                tokens.append(Token(TokenType.STRING, "".join(val), start_line, start_col))
                continue

            # Numbers
            if ch.isdigit():
                start_line = self.line
                start_col = self.column
                num_str = []
                is_float = False
                while self.pos < len(self.source) and (self.peek().isdigit() or (self.peek() == "." and not is_float and self.peek(1).isdigit())):
                    if self.peek() == ".":
                        is_float = True
                    num_str.append(self.advance())
                val_str = "".join(num_str)
                val = float(val_str) if is_float else int(val_str)
                tokens.append(Token(TokenType.NUMBER, val, start_line, start_col))
                continue

            # Identifier / Keyword
            if ch.isalpha() or ch in ("_", "@", "$"):
                start_line = self.line
                start_col = self.column
                id_str = []
                while self.pos < len(self.source) and (self.peek().isalnum() or self.peek() in ("_", "@", "$", ":", "-")):
                    id_str.append(self.advance())
                text = "".join(id_str)

                # Check keywords
                lower_text = text.lower()
                if lower_text in KEYWORDS:
                    t_type = KEYWORDS[lower_text]
                    val = True if lower_text == "true" else (False if lower_text == "false" else text)
                    tokens.append(Token(t_type, val, start_line, start_col))
                else:
                    tokens.append(Token(TokenType.IDENTIFIER, text, start_line, start_col))
                continue

            # Relative coordinates or symbol ~
            if ch == "~":
                start_line = self.line
                start_col = self.column
                self.advance()
                tokens.append(Token(TokenType.TILDE, "~", start_line, start_col))
                continue

            # Multi-char operators
            start_line = self.line
            start_col = self.column
            if ch == "=" and self.peek(1) == "=":
                self.advance(); self.advance()
                tokens.append(Token(TokenType.EQ, "==", start_line, start_col))
                continue
            if ch == "!" and self.peek(1) == "=":
                self.advance(); self.advance()
                tokens.append(Token(TokenType.NEQ, "!=", start_line, start_col))
                continue
            if ch == "<" and self.peek(1) == "=":
                self.advance(); self.advance()
                tokens.append(Token(TokenType.LTE, "<=", start_line, start_col))
                continue
            if ch == ">" and self.peek(1) == "=":
                self.advance(); self.advance()
                tokens.append(Token(TokenType.GTE, ">=", start_line, start_col))
                continue
            if ch == "&" and self.peek(1) == "&":
                self.advance(); self.advance()
                tokens.append(Token(TokenType.AND, "&&", start_line, start_col))
                continue
            if ch == "|" and self.peek(1) == "|":
                self.advance(); self.advance()
                tokens.append(Token(TokenType.OR, "||", start_line, start_col))
                continue

            # Single char operators & punctuation
            single_ops = {
                "=": TokenType.ASSIGN,
                "+": TokenType.PLUS,
                "-": TokenType.MINUS,
                "*": TokenType.STAR,
                "/": TokenType.SLASH,
                "%": TokenType.PERCENT,
                "<": TokenType.LT,
                ">": TokenType.GT,
                "!": TokenType.NOT,
                "(": TokenType.LPAREN,
                ")": TokenType.RPAREN,
                "{": TokenType.LBRACE,
                "}": TokenType.RBRACE,
                "[": TokenType.LBRACKET,
                "]": TokenType.RBRACKET,
                ",": TokenType.COMMA,
                ";": TokenType.SEMICOLON,
                ":": TokenType.COLON,
            }

            if ch in single_ops:
                self.advance()
                tokens.append(Token(single_ops[ch], ch, start_line, start_col))
                continue

            raise LexerError(f"Unexpected character '{ch}' at line {self.line}, col {self.column}")

        tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return tokens
