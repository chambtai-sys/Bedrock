from typing import Any

class ASTNode:
    pass

class ProgramNode(ASTNode):
    def __init__(self, statements: list[ASTNode]):
        self.statements = statements

class VarDeclNode(ASTNode):
    def __init__(self, name: str, value_expr: ASTNode):
        self.name = name
        self.value_expr = value_expr

class AssignNode(ASTNode):
    def __init__(self, name: str, value_expr: ASTNode):
        self.name = name
        self.value_expr = value_expr

class SayNode(ASTNode):
    def __init__(self, message_expr: ASTNode):
        self.message_expr = message_expr

class PrintNode(ASTNode):
    def __init__(self, expr: ASTNode):
        self.expr = expr

class CommandNode(ASTNode):
    def __init__(self, command_name: str, args: list[ASTNode]):
        self.command_name = command_name
        self.args = args

class IfNode(ASTNode):
    def __init__(self, condition: ASTNode, then_body: list[ASTNode], else_body: list[ASTNode] = None):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body or []

class RepeatNode(ASTNode):
    def __init__(self, count_expr: ASTNode, body: list[ASTNode]):
        self.count_expr = count_expr
        self.body = body

class WhileNode(ASTNode):
    def __init__(self, condition: ASTNode, body: list[ASTNode]):
        self.condition = condition
        self.body = body

class FunctionDefNode(ASTNode):
    def __init__(self, name: str, params: list[str], body: list[ASTNode]):
        self.name = name
        self.params = params
        self.body = body

class FunctionCallNode(ASTNode):
    def __init__(self, name: str, args: list[ASTNode]):
        self.name = name
        self.args = args

class ReturnNode(ASTNode):
    def __init__(self, expr: ASTNode = None):
        self.expr = expr

class BinaryOpNode(ASTNode):
    def __init__(self, left: ASTNode, op: str, right: ASTNode):
        self.left = left
        self.op = op
        self.right = right

class UnaryOpNode(ASTNode):
    def __init__(self, op: str, expr: ASTNode):
        self.op = op
        self.expr = expr

class LiteralNode(ASTNode):
    def __init__(self, value: Any):
        self.value = value

class IdentifierNode(ASTNode):
    def __init__(self, name: str):
        self.name = name

class ListNode(ASTNode):
    def __init__(self, elements: list[ASTNode]):
        self.elements = elements

class TildeCoordNode(ASTNode):
    def __init__(self, offset: float = 0):
        self.offset = offset
