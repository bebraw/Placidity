class Operations(tuple):
 
    def __new__(cls, *args):
        class Operation:
 
            def __init__(self, expression, result):
                self.expression = expression
                self.result = result
 
        operations = []
        
        for arg in args:
            operations.append(Operation(*arg))
 
        return tuple.__new__(cls, operations)
