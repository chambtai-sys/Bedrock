from enum import Enum, auto

class TokenType(Enum):
    # Keywords / Commands
    SAY = auto()
    VAR = auto()
    SET = auto()
    IF = auto()
    ELSE = auto()
    EXECUTE = auto()
    RUN = auto()
    REPEAT = auto()
    WHILE = auto()
    FOR = auto()
    IN = auto()
    FUNCTION = auto()
    RETURN = auto()
    GIVE = auto()
    SUMMON = auto()
    TP = auto()
    FILL = auto()
    EFFECT = auto()
    REDSTONE = auto()
    PRINT = auto()

    # Literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()
    BOOLEAN = auto()
    TILDE = auto() # ~ relative coords

    # Operators & Symbols
    ASSIGN = auto()        # =
    PLUS = auto()          # +
    MINUS = auto()         # -
    STAR = auto()          # *
    SLASH = auto()         # /
    PERCENT = auto()       # %
    EQ = auto()            # ==
    NEQ = auto()           # !=
    LT = auto()            # <
    GT = auto()            # >
    LTE = auto()           # <=
    GTE = auto()           # >=
    AND = auto()           # && or AND
    OR = auto()            # || or OR
    NOT = auto()           # ! or NOT

    # Delimiters
    LPAREN = auto()        # (
    RPAREN = auto()        # )
    LBRACE = auto()        # {
    RBRACE = auto()        # }
    LBRACKET = auto()      # [
    RBRACKET = auto()      # ]
    COMMA = auto()         # ,
    SEMICOLON = auto()     # ;
    COLON = auto()         # :
    NEWLINE = auto()
    EOF = auto()

class Token:
    def __init__(self, type_: TokenType, value: any, line: int, column: int):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)}, line={self.line}, col={self.column})"
