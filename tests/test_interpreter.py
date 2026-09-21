import unittest
from bedrock.lexer import Lexer
from bedrock.parser import Parser
from bedrock.interpreter import Interpreter
from bedrock.tokens import TokenType

class TestBedrockLanguage(unittest.TestCase):
    def test_lexer_tokens(self):
        source = 'var x = 10\nsay "Hello World"\nfill ~ ~ ~ ~5 ~5 ~5 "glass"'
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        types = [t.type for t in tokens if t.type != TokenType.NEWLINE and t.type != TokenType.EOF]
        self.assertEqual(types, [
            TokenType.VAR, TokenType.IDENTIFIER, TokenType.ASSIGN, TokenType.NUMBER,
            TokenType.SAY, TokenType.STRING,
            TokenType.FILL, TokenType.TILDE, TokenType.TILDE, TokenType.TILDE,
            TokenType.TILDE, TokenType.NUMBER, TokenType.TILDE, TokenType.NUMBER,
            TokenType.TILDE, TokenType.NUMBER, TokenType.STRING
        ])

    def test_variables_and_arithmetic(self):
        source = '''
        var a = 5
        var b = 10
        var c = a + b * 2
        print c
        '''
        logs = []
        interpreter = Interpreter(output_callback=logs.append)
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        interpreter.eval(ast)
        self.assertIn("25", logs)

    def test_if_else_control_flow(self):
        source = '''
        var signal = 15
        if signal > 10 {
            say "High Signal"
        } else {
            say "Low Signal"
        }
        '''
        logs = []
        interpreter = Interpreter(output_callback=logs.append)
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        interpreter.eval(ast)
        self.assertIn("[Bedrock Say] High Signal", logs)

    def test_repeat_loop(self):
        source = '''
        var count = 0
        repeat 3 {
            count = count + 1
        }
        print count
        '''
        logs = []
        interpreter = Interpreter(output_callback=logs.append)
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        interpreter.eval(ast)
        self.assertIn("3", logs)

    def test_function_definition_and_call(self):
        source = '''
        function add_mobs(mob, amount) {
            say "Adding " + amount + " " + mob
            return amount * 10
        }
        var total = add_mobs("creeper", 4)
        print total
        '''
        logs = []
        interpreter = Interpreter(output_callback=logs.append)
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        interpreter.eval(ast)
        self.assertIn("[Bedrock Say] Adding 4 creeper", logs)
        self.assertIn("40", logs)

    def test_bedrock_commands(self):
        source = '''
        give @p "diamond" 64
        summon "zombie" ~ ~5 ~
        '''
        logs = []
        interpreter = Interpreter(output_callback=logs.append)
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        interpreter.eval(ast)
        self.assertIn("[Command Block /give] @p diamond 64", logs)
        self.assertIn("[Command Block /summon] zombie ~ ~5 ~", logs)

if __name__ == "__main__":
    unittest.main()
