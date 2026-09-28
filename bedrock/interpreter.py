from bedrock.ast import (
    ProgramNode, VarDeclNode, AssignNode, SayNode, PrintNode,
    CommandNode, IfNode, RepeatNode, WhileNode, FunctionDefNode,
    FunctionCallNode, ReturnNode, BinaryOpNode, UnaryOpNode,
    LiteralNode, IdentifierNode, ListNode, TildeCoordNode
)

class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value

class RuntimeError(Exception):
    pass

class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.functions = {}
        self.parent = parent

    def get_var(self, name: str):
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get_var(name)
        raise RuntimeError(f"Undefined variable '{name}'")

    def set_var(self, name: str, value):
        if name in self.variables:
            self.variables[name] = value
            return
        if self.parent and self.parent.has_var(name):
            self.parent.set_var(name, value)
            return
        self.variables[name] = value

    def define_var(self, name: str, value):
        self.variables[name] = value

    def has_var(self, name: str) -> bool:
        if name in self.variables:
            return True
        if self.parent:
            return self.parent.has_var(name)
        return False

    def define_function(self, name: str, func_node: FunctionDefNode):
        self.functions[name] = func_node

    def get_function(self, name: str):
        if name in self.functions:
            return self.functions[name]
        if self.parent:
            return self.parent.get_function(name)
        return None

class Interpreter:
    def __init__(self, output_callback=None):
        self.global_env = Environment()
        self.output_callback = output_callback or print
        self.output_logs = []

    def log(self, text: str):
        self.output_logs.append(text)
        if self.output_callback:
            self.output_callback(text)

    def eval(self, node, env: Environment = None):
        if env is None:
            env = self.global_env

        if isinstance(node, ProgramNode):
            result = None
            for stmt in node.statements:
                result = self.eval(stmt, env)
            return result

        if isinstance(node, VarDeclNode):
            val = self.eval(node.value_expr, env)
            env.define_var(node.name, val)
            return val

        if isinstance(node, AssignNode):
            val = self.eval(node.value_expr, env)
            env.set_var(node.name, val)
            return val

        if isinstance(node, SayNode):
            val = self.eval(node.message_expr, env)
            self.log(f"[Bedrock Say] {val}")
            return val

        if isinstance(node, PrintNode):
            val = self.eval(node.expr, env)
            self.log(str(val))
            return val

        if isinstance(node, CommandNode):
            evaluated_args = [self.eval(arg, env) for arg in node.args]
            arg_str = " ".join(str(a) for a in evaluated_args)
            self.log(f"[Command Block /{node.command_name}] {arg_str}".strip())
            return f"Executed /{node.command_name} {arg_str}".strip()

        if isinstance(node, IfNode):
            cond_val = self.eval(node.condition, env)
            if bool(cond_val):
                res = None
                for stmt in node.then_body:
                    res = self.eval(stmt, env)
                return res
            elif node.else_body:
                res = None
                for stmt in node.else_body:
                    res = self.eval(stmt, env)
                return res
            return None

        if isinstance(node, RepeatNode):
            count = int(self.eval(node.count_expr, env))
            res = None
            for _ in range(count):
                for stmt in node.body:
                    res = self.eval(stmt, env)
            return res

        if isinstance(node, WhileNode):
            res = None
            while bool(self.eval(node.condition, env)):
                for stmt in node.body:
                    res = self.eval(stmt, env)
            return res

        if isinstance(node, FunctionDefNode):
            env.define_function(node.name, node)
            return f"<function {node.name}>"

        if isinstance(node, FunctionCallNode):
            func_node = env.get_function(node.name)
            if not func_node:
                raise RuntimeError(f"Undefined function '{node.name}'")
            arg_vals = [self.eval(arg, env) for arg in node.args]
            if len(arg_vals) != len(func_node.params):
                raise RuntimeError(f"Function '{node.name}' expected {len(func_node.params)} arguments, got {len(arg_vals)}")

            local_env = Environment(parent=self.global_env)
            for param_name, arg_val in zip(func_node.params, arg_vals):
                local_env.define_var(param_name, arg_val)

            try:
                for stmt in func_node.body:
                    self.eval(stmt, local_env)
            except ReturnSignal as ret:
                return ret.value
            return None

        if isinstance(node, ReturnNode):
            val = self.eval(node.expr, env) if node.expr else None
            raise ReturnSignal(val)

        if isinstance(node, BinaryOpNode):
            left = self.eval(node.left, env)
            right = self.eval(node.right, env)
            op = node.op
            if op == "+":
                if isinstance(left, str) or isinstance(right, str):
                    return str(left) + str(right)
                return left + right
            if op == "-": return left - right
            if op == "*": return left * right
            if op == "/": return left / right
            if op == "%": return left % right
            if op == "==": return left == right
            if op == "!=": return left != right
            if op == "<": return left < right
            if op == ">": return left > right
            if op == "<=": return left <= right
            if op == ">=": return left >= right
            if op in ("&&", "and"): return bool(left) and bool(right)
            if op in ("||", "or"): return bool(left) or bool(right)
            raise RuntimeError(f"Unknown binary operator '{op}'")

        if isinstance(node, UnaryOpNode):
            val = self.eval(node.expr, env)
            if node.op == "-": return -val
            if node.op in ("!", "not"): return not bool(val)
            raise RuntimeError(f"Unknown unary operator '{node.op}'")

        if isinstance(node, LiteralNode):
            return node.value

        if isinstance(node, IdentifierNode):
            if env.has_var(node.name):
                return env.get_var(node.name)
            if node.name.startswith("@") or True: # fallback identifier as literal string if undefined
                return node.name
            return env.get_var(node.name)

        if isinstance(node, ListNode):
            return [self.eval(elem, env) for elem in node.elements]

        if isinstance(node, TildeCoordNode):
            return f"~{node.offset}" if node.offset != 0 else "~"

        raise RuntimeError(f"Unknown AST node type '{type(node).__name__}'")
