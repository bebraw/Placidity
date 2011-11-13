from __future__ import absolute_import
import subprocess

class System:
    priority = 'low'

    def matches(self, expression):
        return True

    def execute(self, expression, variables):
        '''
        >>> from py.test import raises

        >>> system = System()

        >>> system.execute('5+13', {})
        18

        >>> system.execute('a+7', {'a': 13, })
        20

        # XXX: figure out which error to give if doesn't match to
        # either py or shell
        #>>> exception = raises(NameError, system.execute, 'foobar', {})
        #>>> exception.typename
        #'NameError'
        '''
        try:
            return eval(expression, {}, variables)
        except Exception:
            p = subprocess.Popen(expression.split(' ') , stdout=subprocess.PIPE)
            return p.communicate()[0]

if __name__ == "__main__":
    import doctest
    doctest.testmod()
