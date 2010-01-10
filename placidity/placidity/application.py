from file import PluginDirectory
from interpreter import Interpreter
from plugin_loader import PluginLoader
 
class Application:
 
    def run(self):
        plugin_loader = PluginLoader()
        plugin_directory = PluginDirectory()
        commands = plugin_loader.load(plugin_directory)
        interpreter = Interpreter(commands)

        try:
            while True:
                input = self.input()
                result = interpreter.interpret(input)

                if result is not None:
                    self.output(result)
        except SystemExit:
            pass

    def input(self):
        return raw_input('>>> ')

    def output(self, result):
        print result
