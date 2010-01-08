from collections import deque
from placidity.application import Application

class Line:
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return self.content

class Input(Line):
    pass

class Output(Line):
    pass

def parse_line(line):
    if len(line.strip()) == 0:
        return

    prefix = '>>> '
    if line.startswith(prefix):
        content = line.strip(prefix)
        return Input(content)
    else:
        content = line
        return Output(content)

class ScenarioTester:
    def __init__(self):
        self.app = Application()
        self.app.input = self._input
        self.app.output = self._output

        self.lines = deque()

    def test(self, scenario):
        self._parse_scenario(scenario)
        self.app.run()

    def _parse_scenario(self, scenario):
        self.lines.clear()

        for line in scenario.split():
            parsed_line = parse_line(line)

            if parsed_line:
                self.lines.append(parsed_line)

    def _input(self):
        current_line = self.lines.popleft()

        if isinstance(current_line, Input):
            return current_line

        assert False, 'Expected input but got output instead!' + \
            ' Failed at line "%s".' % current_line

    def _output(self, result):
        current_line = self.lines.popleft()

        if isinstance(current_line, Output):
            assert result == current_line, \
                "Output content didn't match!' + \
                'Expected %s but got %s instead." \
                % (current_line, result)

        assert False, 'Expected output but got input instead!'

class TestApplication:
    scenario_tester = ScenarioTester()

    def test_math(self):
        scenario = '''
>>> 15 * 3
45
>>> a = 5
>>> b = 10
>>> a + b
15
'''

        self.scenario_tester.test(scenario)

    def test_variables(self):
        scenario = '''
>>> a = 5
>>> b = 10
>>> vars
Stored variables:
a=5
b=10
>>> clean
>>> vars
No stored variables
'''

        self.scenario_tester.test(scenario)

    def test_help(self):
        scenario = '''
>>> help clean
Cleans up stored variables
'''

        self.scenario_tester.test(scenario)
