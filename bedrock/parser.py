from bedrock.tokens import TokenType, Token
from bedrock.ast import (
    ASTNode, ProgramNode, VarDeclNode, AssignNode, SayNode, PrintNode,
    CommandNode, IfNode, RepeatNode, WhileNode, FunctionDefNode,
    FunctionCallNode, ReturnNode, BinaryOpNode, UnaryOpNode,
    LiteralNode, IdentifierNode, ListNode, TildeCoordNode
)

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    def current_token(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]

    def peek_token(self, offset: int = 1) -> Token:
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1]

    def advance(self) -> Token:
        tok = self.current_token()
        self.pos += 1
        return tok

    def match(self, *token_types: TokenType) -> bool:
        if self.current_token().type in token_types:
            self.advance()
            return True
        return False

    def consume(self, token_type: TokenType, err_msg: str) -> Token:
        if self.current_token().type == token_type:
            return self.advance()
        tok = self.current_token()
        raise ParserError(f"{err_msg} (at line {tok.line}, col {tok.column}, found '{tok.value}')")

    def skip_newlines(self):
        while self.current_token().type == TokenType.NEWLINE:
            self.advance()

    def parse(self) -> ProgramNode:
        statements = []
        while self.current_token().type != TokenType.EOF:
            if self.match(TokenType.NEWLINE, TokenType.SEMICOLON):
                continue
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return ProgramNode(statements)

    def parse_statement(self):
        self.skip_newlines()
        tok = self.current_token()

        if tok.type == TokenType.EOF:
            return None

        if tok.type == TokenType.VAR:
            return self.parse_var_decl()

        if tok.type == TokenType.SAY:
            return self.parse_say()

        if tok.type == TokenType.PRINT:
            return self.parse_print()

        if tok.type == TokenType.IF or (tok.type == TokenType.EXECUTE and self.peek_token().type == TokenType.IF):
            return self.parse_if()

        if tok.type == TokenType.REPEAT:
            return self.parse_repeat()

        if tok.type == TokenType.WHILE:
            return self.parse_while()

        if tok.type == TokenType.FUNCTION:
            return self.parse_function_def()

        if tok.type == TokenType.RETURN:
            self.advance()
            if self.current_token().type in (TokenType.NEWLINE, TokenType.SEMICOLON, TokenType.RBRACE, TokenType.EOF):
                return ReturnNode(None)
            expr = self.parse_expression()
            return ReturnNode(expr)

        if tok.type in (TokenType.GIVE, TokenType.SUMMON, TokenType.TP, TokenType.FILL, TokenType.EFFECT, TokenType.REDSTONE):
            return self.parse_bedrock_command()

        # Expression or assignment statement
        if tok.type == TokenType.IDENTIFIER:
            if self.peek_token().type == TokenType.ASSIGN:
                var_name = self.advance().value
                self.consume(TokenType.ASSIGN, "Expected '=' in assignment")
                val_expr = self.parse_expression()
                return AssignNode(var_name, val_expr)

            if self.peek_token().type == TokenType.LPAREN:
                return self.parse_function_call_expr()

        # Fallback to expression
        return self.parse_expression()

    def parse_var_decl(self):
        self.consume(TokenType.VAR, "Expected 'var'")
        name_tok = self.consume(TokenType.IDENTIFIER, "Expected variable name after 'var'")
        val_expr = None
        if self.match(TokenType.ASSIGN):
            val_expr = self.parse_expression()
        else:
            val_expr = LiteralNode(None)
        return VarDeclNode(name_tok.value, val_expr)

    def parse_say(self):
        self.consume(TokenType.SAY, "Expected 'say'")
        expr = self.parse_expression()
        return SayNode(expr)

    def parse_print(self):
        self.consume(TokenType.PRINT, "Expected 'print'")
        expr = self.parse_expression()
        return PrintNode(expr)

    def parse_bedrock_command(self):
        cmd_tok = self.advance()
        cmd_name = cmd_tok.value
        args = []
        while self.current_token().type not in (TokenType.NEWLINE, TokenType.SEMICOLON, TokenType.RBRACE, TokenType.EOF):
            if self.current_token().type == TokenType.TILDE:
                self.advance()
                offset = 0
                if self.current_token().type == TokenType.NUMBER:
                    offset = self.advance().value
                args.append(TildeCoordNode(offset))
            else:
                args.append(self.parse_primary())
        return CommandNode(cmd_name, args)

    def parse_if(self):
        if self.current_token().type == TokenType.EXECUTE:
            self.advance() # consume execute
        self.consume(TokenType.IF, "Expected 'if'")

        has_paren = self.match(TokenType.LPAREN)
        cond = self.parse_expression()
        if has_paren:
            self.consume(TokenType.RPAREN, "Expected ')' after if condition")

        if self.match(TokenType.RUN):
            pass # optional 'run' keyword

        then_body = self.parse_block_or_statement()

        else_body = []
        self.skip_newlines()
        if self.match(TokenType.ELSE):
            else_body = self.parse_block_or_statement()

        return IfNode(cond, then_body, else_body)

    def parse_repeat(self):
        self.consume(TokenType.REPEAT, "Expected 'repeat'")
        has_paren = self.match(TokenType.LPAREN)
        count_expr = self.parse_expression()
        if has_paren:
            self.consume(TokenType.RPAREN, "Expected ')'")

        body = self.parse_block_or_statement()
        return RepeatNode(count_expr, body)

    def parse_while(self):
        self.consume(TokenType.WHILE, "Expected 'while'")
        has_paren = self.match(TokenType.LPAREN)
        cond = self.parse_expression()
        if has_paren:
            self.consume(TokenType.RPAREN, "Expected ')'")

        body = self.parse_block_or_statement()
        return WhileNode(cond, body)

    def parse_function_def(self):
        self.consume(TokenType.FUNCTION, "Expected 'function'")
        func_name = self.consume(TokenType.IDENTIFIER, "Expected function name").value
        params = []
        if self.match(TokenType.LPAREN):
            if self.current_token().type != TokenType.RPAREN:
                params.append(self.consume(TokenType.IDENTIFIER, "Expected parameter name").value)
                while self.match(TokenType.COMMA):
                    params.append(self.consume(TokenType.IDENTIFIER, "Expected parameter name").value)
            self.consume(TokenType.RPAREN, "Expected ')' after parameter list")

        body = self.parse_block()
        return FunctionDefNode(func_name, params, body)

    def parse_block_or_statement(self) -> list[ASTNode]:
        self.skip_newlines()
        if self.current_token().type == TokenType.LBRACE:
            return self.parse_block()
        else:
            stmt = self.parse_statement()
            return [stmt] if stmt else []

    def parse_block(self) -> list[ASTNode]:
        self.skip_newlines()
        self.consume(TokenType.LBRACE, "Expected '{'")
        stmts = []
        while self.current_token().type not in (TokenType.RBRACE, TokenType.EOF):
            if self.match(TokenType.NEWLINE, TokenType.SEMICOLON):
                continue
            stmt = self.parse_statement()
            if stmt:
                stmts.append(stmt)
        self.consume(TokenType.RBRACE, "Expected '}'")
        return stmts

    def parse_expression(self) -> ASTNode:
        return self.parse_logical_or()

    def parse_logical_or(self) -> ASTNode:
        left = self.parse_logical_and()
        while self.current_token().type == TokenType.OR:
            op = self.advance().value
            right = self.parse_logical_and()
            left = BinaryOpNode(left, op, right)
        return left

    def parse_logical_and(self) -> ASTNode:
        left = self.parse_equality()
        while self.current_token().type == TokenType.AND:
            op = self.advance().value
            right = self.parse_equality()
            left = BinaryOpNode(left, op, right)
        return left

    def parse_equality(self) -> ASTNode:
        left = self.parse_relational()
        while self.current_token().type in (TokenType.EQ, TokenType.NEQ):
            op = self.advance().value
            right = self.parse_relational()
            left = BinaryOpNode(left, op, right)
        return left

    def parse_relational(self) -> ASTNode:
        left = self.parse_additive()
        while self.current_token().type in (TokenType.LT, TokenType.GT, TokenType.LTE, TokenType.GTE):
            op = self.advance().value
            right = self.parse_additive()
            left = BinaryOpNode(left, op, right)
        return left

    def parse_additive(self) -> ASTNode:
        left = self.parse_multiplicative()
        while self.current_token().type in (TokenType.PLUS, TokenType.MINUS):
            op = self.advance().value
            right = self.parse_multiplicative()
            left = BinaryOpNode(left, op, right)
        return left

    def parse_multiplicative(self) -> ASTNode:
        left = self.parse_unary()
        while self.current_token().type in (TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op = self.advance().value
            right = self.parse_unary()
            left = BinaryOpNode(left, op, right)
        return left

    def parse_unary(self) -> ASTNode:
        if self.current_token().type in (TokenType.MINUS, TokenType.NOT):
            op = self.advance().value
            right = self.parse_unary()
            return UnaryOpNode(op, right)
        return self.parse_primary()

    def parse_primary(self) -> ASTNode:
        tok = self.current_token()

        if tok.type in (TokenType.NUMBER, TokenType.STRING, TokenType.BOOLEAN):
            self.advance()
            return LiteralNode(tok.value)

        if tok.type == TokenType.IDENTIFIER:
            if self.peek_token().type == TokenType.LPAREN:
                return self.parse_function_call_expr()
            self.advance()
            return IdentifierNode(tok.value)

        if tok.type == TokenType.TILDE:
            self.advance()
            offset = 0
            if self.current_token().type == TokenType.NUMBER:
                offset = self.advance().value
            return TildeCoordNode(offset)

        if tok.type == TokenType.LBRACKET:
            return self.parse_list_literal()

        if tok.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN, "Expected ')'")
            return expr

        raise ParserError(f"Unexpected token '{tok.value}' (type: {tok.type}) at line {tok.line}, col {tok.column}")

    def parse_function_call_expr(self) -> FunctionCallNode:
        func_name = self.consume(TokenType.IDENTIFIER, "Expected function name").value
        self.consume(TokenType.LPAREN, "Expected '('")
        args = []
        if self.current_token().type != TokenType.RPAREN:
            args.append(self.parse_expression())
            while self.match(TokenType.COMMA):
                args.append(self.parse_expression())
        self.consume(TokenType.RPAREN, "Expected ')'")
        return FunctionCallNode(func_name, args)

    def parse_list_literal(self) -> ListNode:
        self.consume(TokenType.LBRACKET, "Expected '['")
        elements = []
        if self.current_token().type != TokenType.RBRACKET:
            elements.append(self.parse_expression())
            while self.match(TokenType.COMMA):
                elements.append(self.parse_expression())
        self.consume(TokenType.RBRACKET, "Expected ']'")
        return ListNode(elements)
