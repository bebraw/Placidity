class Quit:
    aliases = ('quit', 'quit()', ':q', )
    description = 'Quits the application'

    def execute(self):
        raise SystemExit
