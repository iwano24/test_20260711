# --------------------------------------------------
# 1. ASTノード定義（前回のクラスを少し拡張）
# --------------------------------------------------
class Node: pass

class LiteralNode(Node): # 数値などのリテラル
    def __init__(self, value, value_type):
        self.value = value
        self.value_type = value_type # 'int' や 'str' など

class BinOpNode(Node): # 二項演算
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

# --------------------------------------------------
# 2. 意味解析器（Semantic Analyzer）
# --------------------------------------------------
class SemanticAnalyzer:
    def analyze(self, node):
        """ノードの種類に応じて処理を振り分ける（再帰的に木を巡回）"""
        if isinstance(node, LiteralNode):
            # リテラルノードは、その保持している型をそのまま返す
            return node.value_type
            
        elif isinstance(node, BinOpNode):
            # 1. 左側と右側の子ノードをそれぞれ意味解析（型を取得）
            left_type = self.analyze(node.left)
            right_type = self.analyze(node.right)
            
            # 2. 型チェック（今回のルール：int 同士の計算のみ許可）
            if left_type == 'int' and right_type == 'int':
                return 'int' # 計算結果も 'int' 型になる
            else:
                # ルール違反があればエラー（意味論エラー）を出す
                raise TypeError(f"不正な型エラー: '{left_type}' と '{right_type}' の計算はできません。")

# --------------------------------------------------
# 3. 実行検証
# --------------------------------------------------
# 構文解析によって、すでに (3 * 2) + (4 * 5) のASTが完成していると仮定
#          +
#        /   \
#       *     *
#      / \   / \
#     3   2 4   5
normal_ast = BinOpNode(
    BinOpNode(LiteralNode(3, 'int'), '*', LiteralNode(2, 'int')),
    '+',
    BinOpNode(LiteralNode(4, 'int'), '*', LiteralNode(5, 'int'))
)

# 不正な木（例: 3 * "hello"）のAST
error_ast = BinOpNode(LiteralNode(3, 'int'), '*', LiteralNode("hello", 'str'))

# 意味解析の実行
analyzer = SemanticAnalyzer()

# 正常系：エラーなく通過し、最終的な式全体の型（int）が判明する
print("正常なASTの解析結果（型）:", analyzer.analyze(normal_ast)) 

# 異常系：型エラーが検知される
try:
    analyzer.analyze(error_ast)
except TypeError as e:
    print("異常なASTの解析結果:", e)
