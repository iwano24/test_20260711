class Node:
    pass

class NameNode(Node):
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"NameNode({self.name!r})"

class BinOpNode(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
        
    def __repr__(self):
        return f"BinOpNode({self.left!r}, {self.op!r}, {self.right!r})"

class SimpleParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def parse_expr(self):
        left = self.parse_term()
        while self.current() == '+':
            self.pos += 1
            right = self.parse_term()
            left = BinOpNode(left, '+', right)
        return left

    def parse_term(self):
        left = NameNode(self.current())
        self.pos += 1
        while self.current() == '*':
            self.pos += 1
            right = NameNode(self.current())
            self.pos += 1
            left = BinOpNode(left, '*', right)
        return left

tokens = ['1', '+', '2', '*', '3', '+', '4']
parser = SimpleParser(tokens)
ast_tree = parser.parse_expr()

# 構造が入れ子になっているか確認
print(ast_tree)