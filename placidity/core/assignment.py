from __future__ import absolute_import
import re

class Assignment:

    def matches(self, expression):
        '''
        >>> assignment = Assignment()

        >>> assignment.matches('a=5')
        True

        >>> assignment.matches('  a  =  5   ')
        True

        >>> assignment.matches('5=5')
        False

        Extra whitespace in name
        >>> assignment.matches('bar bar = 5')
        False

        Assignment of a variable's value
        >>> assignment.matches('a=b')
        True

        Underscore is allowed in the beginning
        >>> assignment.matches('_fooDOO=bar')
        True

        >>> assignment.matches('a=b+5')
        True

        Multiple assignment
        >>> assignment.matches('a=b=5')
        True

        Multipart
        >>> assignment.matches('a, b = 5, 10')
        True

        >>> assignment.matches('a, b, c = 5, 10')
        False

        Multiple assignment and multipart
        >>> assignment.matches('a, b = d, e = 10, 13')
        True

        Disallow minus in front of a name because "foo - -FOO" is
        ambiguous
        >>> assignment.matches('-FOO=b')
        False
        
        >>> assignment.matches('a, -b = 5, 10')
        False

        Disallow minus in middle of a name because "foo-doo" is
        ambiguous
        >>> assignment.matches('foo-doo=b')
        False

        Don't match if missing =
        >>> assignment.matches('a + b')
        False

        Don't match empty
        >>> assignment.matches('')
        False

        - expansion
        >>> assignment.matches('FOO-=b')
        True

        + expansion
        >>> assignment.matches('FOO+=b')
        True

        * expansion
        >>> assignment.matches('FOO*=b')
        True

        / expansion
        >>> assignment.matches('FOO/=b')
        True

        % expansion
        >>> assignment.matches('FOO%=b')
        True
        '''
        parts = self._split_expression(expression)

        if len(parts) < 2:
            return False

        first_segments_len = len(parts[0].segments)
        for part in parts:
            if len(part.segments) != first_segments_len:
                return False

        if len(parts) == 2 and len(parts[0].segments) == 1:
            l_part = parts[0].segments[0]

            if not l_part.is_valid():
                return False
        else:
            for part in parts[:-1]:
                for segment in part.segments:
                    if not segment.is_valid():
                        return False

        return True

    def execute(self, expression, commands, variables):
        '''
        >>> from mock import Mock
        >>> from py.test import raises

        >>> python = Mock()

        >>> commands = Mock()
        >>> commands.find.return_value = python

        >>> assignment = Assignment()

        Simple assignment
        >>> python.execute.return_value = 5
        >>> variables = {}
        >>> assignment.execute('a=5', commands, variables)
        >>> variables
        {'a': 5}

        Multipart
        >>> python.execute.return_value = 5
        >>> variables = {}
        >>> assignment.execute('a=b=5', commands, variables)
        >>> variables
        {'a': 5, 'b': 5}

        Multiple assignment
        TODO: check type conversion (int to str?)
        >>> def execute(expression, variables):
        ...     return expression
        >>> python.execute = execute
        >>> variables = {}
        >>> assignment.execute('a, b = 5, 10', commands, variables)
        >>> variables
        {'a': '5', 'b': '10'}

        Multiple assignment and multipart
        TODO: check type conversion (int to str?)
        >>> def execute(expression, variables):
        ...     return expression
        >>> python.execute = execute
        >>> variables = {'a': 5, 'b': 6}
        >>> assignment.execute('a, b = c, d = 5, 10', commands, variables)
        >>> variables
        {'a': '5', 'c': '5', 'b': '10', 'd': '10'}

        Assignment of the value of another variable
        >>> python.execute = Mock()
        >>> python.execute.return_value = 10
        >>> variables = {'a': 10}
        >>> assignment.execute('b=a', commands, variables)
        >>> variables
        {'a': 10, 'b': 10}

        Assignment of a result
        >>> python.execute.return_value = 15
        >>> variables = {'a': 10}
        >>> assignment.execute('b=a+5', commands, variables)
        >>> variables
        {'a': 10, 'b': 15}

        - expansion
        >>> python.execute.return_value = 5
        >>> variables = {'a': 10}
        >>> assignment.execute('a-=5', commands, variables)
        >>> variables
        {'a': 5}

        + expansion
        >>> python.execute.return_value = 15
        >>> variables = {'a': 10}
        >>> assignment.execute('a+=5', commands, variables)
        >>> variables
        {'a': 15}

        * expansion
        >>> python.execute.return_value = 50
        >>> variables = {'a': 10}
        >>> assignment.execute('a*=5', commands, variables)
        >>> variables
        {'a': 50}

        / expansion
        >>> python.execute.return_value = 2
        >>> variables = {'a': 10}
        >>> assignment.execute('a/=5', commands, variables)
        >>> variables
        {'a': 2}

        % expansion
        >>> python.execute.return_value = 0
        >>> variables = {'a': 10}
        >>> assignment.execute('a%=5', commands, variables)
        >>> variables
        {'a': 0}

        Assignment of an invalid variable
        >>> python.execute = Mock()
        >>> python.execute.side_effect = NameError("name 'b' is not defined")
        >>> variables = {}
        >>> exception = raises(NameError, assignment.execute, 'a=b', commands,
        ...     variables)
        >>> exception.typename
        'NameError'
        >>> variables
        {}

        Assignment of an invalid variable - Multipart case
        >>> python.execute = Mock()
        >>> python.execute.side_effect = NameError("name 'c' is not defined")
        >>> variables = {}
        >>> exception = raises(NameError, assignment.execute, 'a=b=c',
        ...     commands, variables)
        >>> exception.typename
        'NameError'
        >>> variables
        {}

        Assignment of an invalid variable - Multiple assignment case
        >>> python.execute = Mock()
        >>> python.execute.side_effect = NameError("name 'c' is not defined")
        >>> variables = {}
        >>> exception = raises(NameError, assignment.execute, 'a,b=c,d',
        ...     commands, variables)
        >>> exception.typename
        'NameError'
        >>> variables
        {}
        '''
        def set_variables(l_part, r_part):
            python = commands.find('python')

            for l_segment, r_segment in zip(l_part.segments, r_part.segments):
                if r_segment in variables:
                    variables[l_segment] = variables[r_segment]
                else:
                    variables[l_segment] = python.execute(r_segment, variables)

        parts = self._split_expression(expression)

        if len(parts) == 2:
            if len(parts[1].segments) == 1:
                parts[1].expand(parts[0])

            ret = set_variables(parts[0], parts[1])

            return ret
        else:
            for l_part in parts[:-1]:
                ret = set_variables(l_part, parts[-1])

                if ret:
                    return ret

    def _split_expression(self, expression):
        class Segment(str):
            def is_valid(self):
                return re.match('^[a-zA-Z_]{1}[a-zA-Z_]*$', self)

        class Part:
            def __init__(self, value):
                value = value.strip()

                if len(value) > 0 and value[-1] in ('+', '-', '*', '/', '%'):
                    self.expansion = value[-1]
                    self.segments = (Segment(value[:-1]), )
                else:
                    self.expansion = None
                    self.segments = (Segment(value), )

            def expand(self, l_part):
                expansion = l_part.expansion

                if expansion:
                    self.segments = (l_part.segments[0] + expansion + \
                        self.segments[0], )

        class SegmentedPart:
            def __init__(self, raw_part):
                segments = raw_part.split(',')

                self.segments = []
                for segment in segments:
                    self.segments.append(Segment(segment.strip()))

        expression = expression.strip()
        parts = expression.split('=')

        ret = []
        for part in parts:
            if part.count(',') > 0:
                ret.append(SegmentedPart(part))
            else:
                ret.append(Part(part))

        return ret

if __name__ == "__main__":
    import doctest
    doctest.testmod()
