from file import PluginDirectory
from interpreter import Interpreter
from plugin_loader import PluginLoader
from threads import InputThread, Poller

class KeyboardInput(InputThread):
    def get_data(self):
        return raw_input('>>> ')

class Application:
    input_source = KeyboardInput

    def run(self):
        plugin_loader = PluginLoader()
        plugin_directory = PluginDirectory()
        commands = plugin_loader.load(plugin_directory)
        self.interpreter = Interpreter(commands)
        poller = Poller(self.input_source, self.input_evaluator)

        poller.poll()

    def input_evaluator(self, user_input):
        if user_input is None:
            user_input = self.input()

        result = self.interpreter.interpret(user_input)

        if result is not None:
            if isinstance(result, str):
                lines = result.split('\n')

                if len(lines) > 1:
                    for line in lines:
                        self.output(line)
                else:
                    self.output(result)
            else:
                self.output(result)

    def output(self, result):
        print result
