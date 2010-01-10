from mock import Mock
from placidity.interpreter import Interpreter

class TestInterpreter(AbstractTestInterpreter):
    def setup_method(self, method):
        interpreter = Interpreter()
        self.interpret = interpreter.interpret

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
