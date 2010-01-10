from collections import deque

class InputError(Exception):
    pass

class MatchError(Exception):
    pass

class OutputError(Exception):
    pass

class Line:
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return self.content

class EllipsisOutput:
    class Content:
        def __eq__(self, other):
            return True

    def __init__(self):
        self.content = self.Content()

class Input(Line):
    pass

class Output(Line):
    pass

class ScenarioTester:
    def __init__(self, app_class):
        self.app = app_class()
        self.app.input = self._input
        self.app.output = self._output

        self.lines = deque()

    def test(self, scenario):
        self.parse(scenario)
        self.app.run()

    def parse(self, scenario):
        self.lines.clear()

        for line in scenario.split('\n'):
            parsed_line = self._parse_line(line)

            if parsed_line:
                self.lines.append(parsed_line)

    def _parse_line(self, line):
        if len(line.strip()) == 0:
            return

        prefix = '>>> '
        if line.startswith(prefix):
            content = line.strip(prefix)
            return Input(content)
        elif line.startswith('...'):
            return EllipsisOutput()
        else:
            content = line
            return Output(content)

    def _input(self):
        if len(self.lines) == 0:
            raise SystemExit

        current_line = self.lines.popleft()

        if isinstance(current_line, Input):
            return str(current_line)
        else:
            raise InputError, 'Expected input but got output instead!' + \
                ' Failed at line "%s".' % current_line

    def _output(self, result):
        line = self.lines.popleft()

        if isinstance(line, Output):
            content = line.content

            if content != str(result):
                raise MatchError, "Output content didn't match!" + \
                    " Expected %s (%s) but got %s (%s) instead." \
                    % (content, type(content), result, type(result))
        elif isinstance(line, EllipsisOutput):
            pass
        else:
            raise OutputError, 'Expected output but got input instead!' + \
                ' Failed at line "%s". Result: %s.' % (line, result)
