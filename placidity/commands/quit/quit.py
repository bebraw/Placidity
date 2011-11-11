class Quit:
    aliases = ('quit', 'quit()', )
    description = 'Quits the application'

    def execute(self):
        raise SystemExit
