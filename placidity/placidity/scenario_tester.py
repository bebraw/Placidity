import types
from collections import deque

class InputError(Exception):
    pass

class NotRunningError(Exception):
    pass

class MatchError(Exception):
    pass

class OutputError(Exception):
    pass

class RunningError(Exception):
    pass

class Line:
    def __init__(self, line):
        self.content = line

    def check_input(self, app):
        raise InputError, 'Expected input but got output instead!' + \
            ' Failed at line "%s".' % self.content

    def check_output(self, result):
        raise OutputError, 'Expected output but got input instead!' + \
            ' Failed at line "%s". Result: %s.' % (self.content, result)

class PrefixLine(Line):
    def __init__(self, line):
        self.content = line.strip(self.prefix)

    @classmethod
    def matches(cls, line):
        return line.startswith(cls.prefix)

class Input(PrefixLine):
    prefix = '>>> '

    def check_input(self, app):
        return self.content

class Meta(PrefixLine):
    prefix = '--- '

    def check_input(self, app):
        def not_running():
            if app.running:
                raise RunningError, 'The application was expected to be ' + \
                    'halted but it was running instead!'

        def running():
            if not app.running:
                raise NotRunningError, 'The application was expected to ' + \
                    'be running but it was halted instead!'

        def restart():
            app.running = True

        {'not running': not_running, 'running': running,
            'restart': restart}[self.content]()

class Output(Line):
    @classmethod
    def matches(cls, line):
        return True

    def check_output(self, result):
        if self.content != str(result):
            raise MatchError, "Output content didn't match!" + \
                " Expected %s (%s) but got %s (%s) instead." \
                % (self.content, type(self.content), result, type(result))

class EllipsisOutput(Line):
    class Content:
        def __eq__(self, other):
            return True

    def __init__(self, line):
        self.content = self.Content()

    @classmethod
    def matches(cls, line):
        return line.startswith('...')

    def check_output(self, result):
        pass

class LineParser:
    line_types = (EllipsisOutput, Input, Meta, Output, )

    def parse(self, scenario):
        lines = deque()

        for line in scenario.split('\n'):
            parsed_line = self._parse_line(line)

            if parsed_line:
                lines.append(parsed_line)

        return lines

    def _parse_line(self, line):
        line = line.strip()

        if len(line) == 0:
            return

        for line_type in self.line_types:
            if line_type.matches(line):
                return line_type(line)

class ScenarioTester:
    def __init__(self, app_class):
        self._set_hooks(app_class)

    def test(self, scenario):
        self.parse(scenario)
        self.app.running = True

        while len(self.lines) > 0:
            self.app.run()
            self.app.running = False

    def parse(self, scenario):
        line_parser = LineParser()
        self.lines = line_parser.parse(scenario)

    def _set_hooks(self, app_class):
        self.app = app_class()

        def input(app):
            if len(self.lines) == 0:
                raise SystemExit

            current_line = self.lines.popleft()
            
            return current_line.check_input(app)

        self.app.input = types.MethodType(input, self.app, app_class)

        def output(app, result):
            current_line = self.lines.popleft()

            return current_line.check_output(result)

        self.app.output = types.MethodType(output, self.app, app_class)
