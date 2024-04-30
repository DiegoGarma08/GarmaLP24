
# simplecheck.py
code = '''
a = 23
b = 42
c = 'hello'
d = a + 2*b
e = a + z
f = a + c
g = c * c
'''

import ast
top = ast.parse(code)
#print(ast.dump(top))

class SimpleCheck(ast.NodeVisitor):
        def __init__(self):
            self.symbols = { }

        def visit_Num(self, node):
            node.type = 'Num'

        def visit_Str(self, node):
            node.type = 'Str'

        def visit_Assign(self, node):
            # Visit the right-hand-side value to get types assignment
            self.visit(node.value)

            # Temporarily store the right-hand-side so it's visible in other methods
            self.assignment_value = node.value

            # Visit each target on the left-hand-side
            for target in node.targets:
                self.visit(target)
            
        def visit_Name(self, node):
            # If storing, a type is added to the symbol table (from self.assignment_value above)
            if isinstance(node.ctx, ast.Store):
                self.symbols[node.id] = getattr(self.assignment_value, 'type', None)

            # If loading, check definition in symbol table and attach type
            elif isinstance(node.ctx, ast.Load):
                if node.id not in self.symbols:
                    print('Error: Name %s not defined' % node.id)
                else:
                    # Attach known type information to the node (from symbol table)
                    node.type = self.symbols.get(node.id, None)

        def visit_BinOp(self, node):
            self.visit(node.left)
            self.visit(node.right)
            left_type = getattr(node.left, 'type', None)
            right_type = getattr(node.right, 'type', None)
            if left_type != right_type:
                print('Error: Type error.  %s %s %s' % (left_type, type(node.op).__name__, right_type))
                node.type = 'error'
            else:
                node.type = left_type

checker = SimpleCheck()
checker.visit(top)
print(checker.symbols)