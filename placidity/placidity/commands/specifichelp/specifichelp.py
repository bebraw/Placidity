class SpecificHelp:
    def matches(self, expression):
        '''
        >>> specific_help = SpecificHelp()

        >>> specific_help.matches('help foo')
        True

        >>> specific_help.matches('    help     foo     ')
        True

        Accept just one parameter for now
        >>> specific_help.matches('help foo bar')
        False
        '''
        parts = expression.split()

        if parts[0] == 'help':
            if len(parts) == 2:
                return True

        return False

    def execute(self, expression, commands):
        '''
        >>> from mock import Mock

        >>> clean = Mock()
        >>> clean.aliases = 'clean'
        >>> clean.description = 'Cleans up stored variables'

        >>> commands = Mock()
        >>> def find(name):
        ...     if name == 'clean':
        ...         return clean
        >>> commands.find = find

        >>> specific_help = SpecificHelp()
        >>> specific_help.execute('   help   clean  ', commands)
        'Cleans up stored variables'
        '''
        target_name = expression.split()[1]
        target_command = commands.find(target_name)

        return target_command.description

if __name__ == "__main__":
    import doctest
    doctest.testmod()
