class SpecificHelp:
 
    def __init__(self, target_name):
        '''
        >>> from mock import Mock
         
        >>> clean = Mock()
        >>> clean.aliases = 'clean'
        >>> clean.description = 'Cleans up stored variables'
         
        >>> commands = Mock()
        >>> commands.find.return_value = clean
         
        >>> help = SpecificHelp('clean')
        >>> help.execute(commands)
        'Cleans up stored variables'
        '''
        self.target_name = target_name
 
    def execute(self, commands):
        target_command = commands.find(self.target_name)
 
        return target_command.description
 
 
class Help:
    aliases = 'help'
 
    def matches(self, expression):
        parts = expression.split()
 
        if parts[0] == 'help':
            if len(parts) > 1:
                return SpecificHelp(parts[1])
 
            return self
 
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