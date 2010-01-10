from mock import Mock
from placidity.interpreter import Commands, Interpreter

# TODO: convert execute asserts to assert_called_with and handle
# return with return_value. Note that it's possible to mock the
# signatures in Mock 0.7 (fix after release or include svn version in
# /lib)

class TestCommands:
    def test_find_single(self):
        class Foo:
            pass

        command = Foo()

        commands = Commands(command)

        assert commands.find(name='foo') == command

    def test_find_nothing(self):
        commands = Commands()

        assert commands.find(name='foo') == None

    def test_find_based_on_priority(self):
        class Bar:
            priority = 'low'

        class Foo:
            priority = 'normal'

        class Help:
            priority = 'normal'

        command1 = Bar()
        command2 = Foo()
        command3 = Help()

        commands = Commands((command1, command2, command3))

        assert commands.find(priority='low') == [command1, ]

        multiple = commands.find(priority='normal')
        assert command2 in multiple
        assert command3 in multiple

class TestInterpreter:
    def test_exception(self):
        interpreter = Interpreter()

        assert interpreter.interpret('foobar') == 'null'

    def test_no_return(self):
        def execute():
            pass
        command = self.create_command('foo', execute_method=execute)

        interpreter = Interpreter(command)

        assert interpreter.interpret('foo') == None

    def test_priority(self):
        def execute_1():
            return 'foo'
        command1 = self.create_command('bar', 'high', execute_1)

        def execute_2():
            return 'BYE'
        command2 = self.create_command('bar', 'normal', execute_2)

        def execute_3():
            return 'BYEBYE'
        command3 = self.create_command('bar', 'low', execute_3)

        interpreter = Interpreter([command1, command2, command3])

        assert interpreter.interpret('bar') == 'foo'

    def test_execute_parameters(self):
        def no_parameters():
            return 'executed command'

        def with_commands(commands):
            assert commands == [command, ]

            return 'executed command'

        def with_expression(expression):
            assert expression == 'command'

            return 'executed command'

        def with_variables(variables):
            assert variables == {}
            
            return 'executed command'

        def with_multiple_parameters(expression, commands,
                variables):
            assert commands == [command, ]
            assert expression == 'command'
            assert variables == {}

            return 'executed command'

        execute_methods = (no_parameters, with_commands, with_expression, \
            with_variables, with_multiple_parameters, )

        command = self.create_command('command')
        interpreter = Interpreter(command)

        for execute_method in execute_methods:
            command.execute = execute_method

            assert interpreter.interpret('command') == 'executed command', \
                execute_method.__name__ + ' failed!'
            command.matches.assert_called_with('command')

    def test_execute_command(self):
        def execute():
            return 'executed command'

        command1 = self.create_command('foo', execute_method=execute)
        command2 = self.create_command('bar', execute_method=execute)

        interpreter = Interpreter([command1, command2, ])

        assert interpreter.interpret('foo') == 'executed command'

    def create_command(self, name, priority='normal', execute_method=None):
        command = Mock()
        command.aliases = name

        command.matches = Mock()
        command.matches.return_value = True

        if execute_method:
            command.execute = execute_method

        command.priority = priority

        return command
