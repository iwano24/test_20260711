# --------------------------------------------------
# 1. ASTを「下から上」の順序（ポストオーダー）のリストに変換
# --------------------------------------------------
# 実際のコンパイラでは、構文解析の時点でこの順序で出力することもあります。
# (3 * 2) + (4 * 5) の「下から順」の並び：
flat_ast = [
    ('LITERAL', 3, 'int'),
    ('LITERAL', 2, 'int'),
    ('OP', '*'),
    ('LITERAL', 4, 'int'),
    ('LITERAL', 5, 'int'),
    ('OP', '*'),
    ('OP', '+')
]

# --------------------------------------------------
# 2. ボトムアップ意味解析器（再帰なし、スタックを使用）
# --------------------------------------------------
class BottomUpAnalyzer:
    def analyze(self, flat_nodes):
        type_stack = [] # 型情報を一時保存するスタック

        for node in flat_nodes:
            if node[0] == 'LITERAL':
                # 葉ノード（一番下）の型をスタックに積む（シフトに似た動き）
                type_stack.append(node[2])
                
            elif node[0] == 'OP':
                # 演算子が出たら、スタックから下の部品の型を2つ取り出す
                right_type = type_stack.pop()
                left_type = type_stack.pop()
                op = node[1]
                
                # 型チェック（還元に似た動き）
                if left_type == 'int' and right_type == 'int':
                    # 計算が正しいので、結果の型（int）を上に伝える
                    type_stack.append('int')
                else:
                    raise TypeError(f"不正な型: {left_type} {op} {right_type}")
                    
        # 最後にスタックに残った型が、式全体の型（ルートの型）になる
        return type_stack[0]

# --------------------------------------------------
# 3. 実行
# --------------------------------------------------
analyzer = BottomUpAnalyzer()
final_type = analyzer.analyze(flat_ast)
print("ボトムアップ解析結果（全体の型）:", final_type) # int
