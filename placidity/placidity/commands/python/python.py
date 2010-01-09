class Python:
    priority = 'low'

    def matches(self, expression):
        return True

    def execute(self, expression, variables):
        '''
        >>> python = Python()

        >>> python.execute('5+13', {})
        18

        >>> python.execute('a+7', {'a': 13, })
        20

        >>> python.execute('foobar', {})
        "NameError: name 'foobar' is not defined"
        '''
        try:
            return eval(expression, {}, variables)
        except Exception, e:
            class_name = e.__class__.__name__
            return class_name + ': ' + str(e)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
