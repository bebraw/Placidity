from __future__ import absolute_import
import os

class Cd:
    aliases = 'cd'
    description = 'Change working directory'

    def matches(self, expression):
        parts = expression.split()

        return parts[0] == 'cd' and len(parts) == 2

    def execute(self, expression, variables):
        target = expression.split()[1]
        target = variables.get(target, target)

        # TODO: ~ -> home, - -> prev

        try:
            os.chdir(os.path.join(os.getcwd(), target))
        except IOError:
            return "Directory not found!"

