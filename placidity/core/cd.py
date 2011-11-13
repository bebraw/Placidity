from __future__ import absolute_import
import os

class Cd:
    aliases = 'cd'
    description = 'Change working directory'
    prev = os.getcwd()

    def matches(self, expression):
        parts = expression.split()

        return parts[0] == 'cd' and len(parts) == 2

    def execute(self, expression, variables):
        target = expression.split()[1]
        target = variables.get(target, target)

        if target == "~":
            target = os.path.expanduser('~')

        if target == "-":
            target = self.prev

        try:
            cwd = os.getcwd()
            target_dir = os.path.join(cwd, target)
            os.chdir(target_dir)
            self.prev = cwd
        except IOError:
            return "Directory not found!"

