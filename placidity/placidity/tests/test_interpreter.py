from mock import Mock
from placidity.interpreter import Interpreter

class TestInterpreter:
    def test_exception(self):
        interpreter = Interpreter()

        assert interpreter.interpret('foobar') == 'null'

    def test_priority(self):
        command1 = self.create_command('bar', 'hi', 'high')
        command2 = self.create_command('bar', 'BYE', 'normal')
        command3 = self.create_command('bar', 'BYEBYE', 'low')

        interpreter = Interpreter([command1, command2, command3])

        assert interpreter.interpret('bar') == 'hi'

    def test_execute_parameters(self):
        # TODO: convert execute asserts to assert_called_with and handle
        # return with return_value. Note that it's possible to mock the
        # signatures in Mock 0.7 (fix after release or include svn version in
        # /lib)
        def with_commands(self, commands):
            assert commands == [command, ]

            return 'executed command'

        def with_expression(self, expression):
            assert expression == 'command'

            return 'executed command'

        def with_variables(self, variables):
            assert variables == {}
            
            return 'executed command'

        def with_multiple_parameters(self, expression, commands,
                variables):
            assert commands == [command, ]
            assert expression == 'command'
            assert variables == {}

            return 'executed command'

        execute_methods = (with_commands, with_expression, with_variables,
            with_multiple_parameters, )

        command = self.create_command('command')
        interpreter = Interpreter(command)

        for execute_method in execute_methods:
            command.__class__.execute = execute_method

            assert interpreter.interpret('command') == 'executed command'
            command.matches.assert_called_with('command')

    def test_execute_command(self):
        command1 = self.create_command('foo', 'executed command')
        command2 = self.create_command('bar', 'executed command')

        interpreter = Interpreter([command1, command2, ])

        assert interpreter.interpret('foo') == 'executed command'

    def create_command(self, name, execute_return, priority='normal'):
        command = Mock()
        command.aliases = name

        command.matches = Mock()
        command.matches.return_value = True

        command.execute = Mock()
        command.execute.return_value = 'executed command'

        command.priority = priority

        return command
