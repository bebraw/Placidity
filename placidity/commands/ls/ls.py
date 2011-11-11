import os

try:
    import colorama
except ImportError:
    colorama = None

# TODO: figure out how to get rid of warning caused by the import!

class Ls:
    aliases = ('ls', )
    description = 'Lists contents of the current directory'

    def execute(self):
        def colorify(i):
            col = colorama.Fore.YELLOW if colorama else ''

            return col + i if os.path.isdir(i) else i

        items = os.listdir(os.getcwd())
        items = map(colorify, items)

        for i in items:
            print i

