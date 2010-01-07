class Clean:
    aliases = 'clean'
    description = 'Cleans up stored variables'
 
    def execute(self, variables):
        '''
        >>> clean = Clean()
         
        Cleaning empty vars should result in empty still
        >>> variables = {}
        >>> clean.execute(variables)
        >>> variables
        {}
         
        Cleaning existing variables should result in empty
        >>> variables = {'a': 5, }
        >>> clean.execute(variables)
        >>> variables
        {}
        '''
        for variable in variables.keys():
            del variables[variable]
 
if __name__ == "__main__":
    import doctest
    doctest.testmod()
