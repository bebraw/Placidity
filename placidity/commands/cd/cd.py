import os

class Cd:
    aliases = 'cd'
    description = 'Change working directory'

    def matches(self, expression):
        parts = expression.split()

        return parts[0] == 'cd' and len(parts) == 2

    def execute(self, expression):
        target = expression.split()[1]

        os.chdir(os.path.join(os.getcwd(), target))

