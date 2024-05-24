import ast

class CodeGenerator(ast.NodeVisitor):
    '''
    Sample code generator with basic blocks and control flow
    '''
    def __init__(self):
        self.code = []
        self._label = 0

    def new_block(self):
        self._label += 1
        return 'b%d' % self._label

    def visit_If(self, node):
        '''
        Example of compiling a simple Python if statement. 
        '''
        # Step 1: Evaluate the test condition
        self.visit(node.test)

        # Step 2: Make a block labels for both branches and the merge point
        ifblock = self.new_block()
        elseblock = self.new_block()
        mergeblock = self.new_block()

        self.code.append(('JUMP_IF_FALSE', elseblock))

        # Step 3: Traverse all of the statements in the if-body
        self.code.append(('BLOCK', ifblock))
        for bnode in node.body:
            self.visit(bnode)
        self.code.append(('JUMP', mergeblock))

        # Step 4: If there's an else-clause, create a new block and traverse statements
        if node.orelse:
            self.code.append(('BLOCK', elseblock))
            # Visit the body of the else-clause
            for bnode in node.orelse:
                self.visit(bnode)

        # Step 5: Start a new block to continue on with more instructions
        self.code.append(('BLOCK', mergeblock))

    def visit_While(self, node):
        '''
        Compile a Python while statement.
        '''
        # Step 1: Create labels for the start of the loop, the body, and the end
        startblock = self.new_block()
        bodyblock = self.new_block()
        endblock = self.new_block()

        # Step 2: Start the loop
        self.code.append(('BLOCK', startblock))

        # Step 3: Evaluate the test condition
        self.visit(node.test)
        self.code.append(('JUMP_IF_FALSE', endblock))

        # Step 4: Traverse all the statements in the body
        self.code.append(('BLOCK', bodyblock))
        for bnode in node.body:
            self.visit(bnode)

        # Step 5: Jump back to the start of the loop
        self.code.append(('JUMP', startblock))

        # Step 6: End the loop
        self.code.append(('BLOCK', endblock))

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)
        opname = node.op.__class__.__name__
        inst = ("BINARY_" + opname.upper(),)
        self.code.append(inst)

    def visit_Compare(self, node):
        self.visit(node.left)
        opname = node.ops[0].__class__.__name__
        self.visit(node.comparators[0])
        inst = ("BINARY_" + opname.upper(),)
        self.code.append(inst)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):  # Si es una carga
            inst = ('LOAD_GLOBAL', node.id)  # Cargar el valor global
        elif isinstance(node.ctx, ast.Store):  # Si es una asignación
            inst = ('STORE_GLOBAL', node.id)  # Almacenar el valor global
        else:
            inst = ('Unimplemented',)  # Otra operación no implementada
        self.code.append(inst)


    def visit_Num(self, node):
        inst = ('LOAD_CONST', node.n)
        self.code.append(inst)


top = ast.parse('''\
n = 5
while n > 0:
    n = n - 1
''')
gen = CodeGenerator()
gen.visit(top)
for instr in gen.code:
    print(instr)
