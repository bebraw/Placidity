from file import PluginDirectory
from interpreter import Interpreter
from plugin_loader import PluginLoader
 
class Application:
 
    def run(self):
        plugin_loader = PluginLoader()
        plugin_directory = PluginDirectory()
        commands = plugin_loader.load(plugin_directory)
        interpreter = Interpreter(commands)
 
        while True:
            input = self.input()
            result = interpreter.interpret(input)

            self.output(result)

    def input(self):
        return raw_input()

    def output(self, result):
        print result
