class Python:
    # TODO: make it possible to actually run Python interpeter as an app
    priority = 'low'

    def matches(self, expression):
        return True

    def execute(self, expression, variables):
        '''
        >>> python = Python()

        >>> variables = {}
        >>> python.execute('5+13', variables)
        18

        >>> variables = {'a':13, }
        >>> python.execute('a+7', variables)
        20
        '''
        return eval(expression, {}, variables)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
