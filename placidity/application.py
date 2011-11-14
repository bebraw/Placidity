try:
    import colorama

    colorama.init(autoreset=True)
except ImportError:
    colorama = None

import readline
from itertools import chain
from file import PluginDirectory
from interpreter import Interpreter
from plugin_loader import PluginLoader
from threads import InputThread, Poller

class KeyboardInput(InputThread):
    def get_data(self):
        color = colorama.Fore.GREEN if colorama else ''

        return raw_input(color + '>>> ')

class Application:
    input_source = KeyboardInput

    def run(self):
        plugin_loader = PluginLoader()
        plugin_directory = PluginDirectory('core')
        commands = plugin_loader.load(plugin_directory)
        
        self._init_completion(commands)
        
        self.interpreter = Interpreter(commands)
        
        poller = Poller(self.input_source, self.input_evaluator)
        poller.poll()

    def _init_completion(self, commands):
        # http://stackoverflow.com/questions/2046050/tab-completion-in-python-command-line-interface-how-to-catch-tab-events
        # TODO: http://stackoverflow.com/questions/5637124/tab-completion-in-pythons-raw-input (path completion)
        # Note that OS X users need to install http://pypi.python.org/pypi/readline/ for this to work!
        def get_names(i):
            aliases = i.aliases

            return aliases if hasattr(aliases, '__iter__') else [aliases]

        command_names = filter(None, chain(*map(get_names, commands)))

        def complete(text, state):
            for cmd in command_names:
                if cmd.startswith(text):
                    if not state:
                        return cmd
                    else:
                        state -= 1

        readline.parse_and_bind('tab: complete')
        readline.set_completer(complete)

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
