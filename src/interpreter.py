class Interpreter:
    def __init__(self, node) -> None:
        self.node = node

    def visit(self, node):
        method = getattr(self, node.__class__.name)
        return method(node)

    def no_visit_defined(self, node):
        print('no method defined')

    def bin_op_node(self, node):
        pass