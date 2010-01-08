class Variables:
    aliases = ('variables', 'vars', )
    description = 'Shows stored variables'
 
    def execute(self, variables):
        '''
        >>> variables_command = Variables()
         
        >>> variables = {}
        >>> variables_command.execute(variables)
        'No stored variables'
         
        >>> variables = {'a': 14, 'b': -4, 'animal': 'boar', }
        >>> variables_command.execute(variables)
        "Stored variables:\\na=14\\nb=-4\\nanimal='boar'"
        '''
        variable_str = ''
 
        for name, value in variables.items():
            if isinstance(value, str):
                value_str = "'" + value + "'"
            else:
                value_str = str(value)
 
            variable_str += '\n' + name + '=' + value_str
 
        if variable_str:
            return 'Stored variables:' + variable_str
 
        return 'No stored variables'
 
if __name__ == "__main__":
    import doctest
    doctest.testmod()
