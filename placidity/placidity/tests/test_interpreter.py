from mock import Mock
from placidity.interpreter import Interpreter
from placidity.utils import Operations

class AbstractTestInterpreter:

    def setup_method(self, method):
        interpreter = Interpreter()
        self.interpret = interpreter.interpret

class TestInterpreter(AbstractTestInterpreter):
    def test_execute_commands(self):
        def execute_with_commands(self, commands):
            assert commands == [command, ]
            return 'executed command'

        def execute_with_variables(self, variables):
            assert variables == {}
            return 'executed command'

        execute_methods = (execute_with_commands, execute_with_variables, )

        command = self.create_command('command')
        interpreter = Interpreter(command)

        for execute_method in execute_methods:
            command.__class__.execute = execute_method

            assert interpreter.interpret('command') == 'executed command'
            command.matches.assert_called_with('command')

    def test_execute_with_multiple_commands(self):
        def execute_with_commands(self, commands):
            assert commands == [command1, command2, ]
            return 'executed command'

        def execute_with_variables(self, variables):
            assert variables == {}
            return 'executed command'

        command1 = self.create_command('foo', execute_with_commands)
        command2 = self.create_command('bar', execute_with_variables)
        interpreter = Interpreter([command1, command2, ])

        assert interpreter.interpret('foo') == 'executed command'

    def create_command(self, name, execute_method=None):
        command = Mock()
        command.aliases = name
        command.matches = Mock()
        command.matches.return_value = True

        if execute_method:
            command.__class__.execute = execute_method

        return command

class TestSetVariable(AbstractTestInterpreter):

    def test_set(self):
        self.interpret('a=6')
        assert self.interpret('a') == 6

    def test_set_expression(self):
        self.interpret('a=4*3')
        assert self.interpret('a') == 12

    def test_set_variable(self):
        self.interpret('a=8')
        self.interpret('b=a')
        assert self.interpret('b') == 8

    def test_variable_in_expression(self):
        self.interpret('a=12')
        assert self.interpret('a+3') == 15

class TestUnsetVariable(AbstractTestInterpreter):

    def test_unset_variable(self):
        assert self.interpret('a') == 'null'

    def test_variable_in_expression(self):
        assert self.interpret('a+3') == 'null'

class TestMath(AbstractTestInterpreter):
    operations = Operations(('1+1', 2), ('5-1', 4), ('3*5', 15), ('12/4', 3), )

    def test_operations(self):
        for operation in self.operations:
            assert self.interpret(operation.expression) == operation.result
