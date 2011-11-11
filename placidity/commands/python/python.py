class Python:
    priority = 'low'

    def matches(self, expression):
        return True

    def execute(self, expression, variables):
        '''
        >>> from py.test import raises

        >>> python = Python()

        >>> python.execute('5+13', {})
        18

        >>> python.execute('a+7', {'a': 13, })
        20

        >>> exception = raises(NameError, python.execute, 'foobar', {})
        >>> exception.typename
        'NameError'
        '''
        return eval(expression, {}, variables)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
