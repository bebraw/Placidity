import inspect

class Commands(list):
    def __init__(self, commands):
        commands = commands if commands else []

        if not hasattr(commands, '__iter__'):
            commands = [commands]
        
        super(Commands, self).__init__(commands)

    def match(self, expression):
        for command in self:
            if command.matches(expression):
                return command

class Interpreter:

    def __init__(self, commands=None):
        self.commands = Commands(commands)
        self.vars = {}

    def interpret(self, expression):
        try:
            return eval(expression, {}, self.vars)
        except NameError:
            matching_command = self.commands.match(expression)

            if matching_command:
                execute_method = matching_command.execute
                parameter_name = inspect.getargspec(execute_method)[0][1]

                if parameter_name == 'variables':
                    return matching_command.execute(self.vars)
                else:
                    return matching_command.execute(self.commands)
            else:
                return 'null'
        except SyntaxError:
            l_value, r_value = expression.split('=')
            
            try:
                self.vars[l_value] = int(r_value)
            except ValueError:
                self.vars[l_value] = self.interpret(r_value)
