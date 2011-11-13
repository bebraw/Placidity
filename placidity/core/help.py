class Help:
    aliases = 'help'
    priority = 'low'
 
    def execute(self, commands):
        '''
        >>> from mock import Mock
         
        >>> clean = Mock()
        >>> clean.aliases = 'clean'
        >>> clean.description = 'Cleans up stored variables'
         
        >>> variables = Mock()
        >>> variables.aliases = ('variables', 'vars', )
        >>> variables.description = 'Shows stored variables'
         
        >>> commands = [clean, variables]
         
        >>> help = Help()
        >>> help.execute(commands)
        'clean - Cleans up stored variables\\nvariables, vars - Shows stored variables'
        '''
        ret = ''
 
        for command in commands:
            if hasattr(command, 'description'):
                if hasattr(command.aliases, '__iter__'):
                    ret += ', '.join(command.aliases)
                else:
                    ret += command.aliases
 
                ret += ' - ' + command.description + '\n'
 
        return ret.rstrip()
 
 
if __name__ == "__main__":
    import doctest
    doctest.testmod()