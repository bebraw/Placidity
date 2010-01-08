from placidity.scenario_tester import Input, InputException, MatchException, \
Output, OutputException, ScenarioTester
from py.test import raises

class AbstractApplication:
    def run(self):
        while True:
            input = self.input()

            if input == 'quit':
                break

            result = self.interpret(input)

            if result:
                self.output(result)

class TestScenarioTester:
    def test_passing_test(self):
        class Application(AbstractApplication):
            def interpret(self, input):
                if input == 'a':
                    return '4'

        scenario = '''
>>> a = 4
>>> a
4
>>> quit
'''

        scenario_tester = ScenarioTester(Application)
        scenario_tester.parse(scenario)
        lines = scenario_tester.lines

        assert len(lines) == 4
        self.assert_line(lines, 1, Input, 'a = 4')
        self.assert_line(lines, 2, Input, 'a')
        self.assert_line(lines, 3, Output, '4')
        self.assert_line(lines, 4, Input, 'quit')

        # this should not trigger any asserts
        scenario_tester.test(scenario)

    def test_input_fail(self):
        class Application(AbstractApplication):
            def interpret(self, input):
                pass

        scenario = '''
fail
'''

        scenario_tester = ScenarioTester(Application)
        scenario_tester.parse(scenario)
        lines = scenario_tester.lines

        assert len(lines) == 1
        self.assert_line(lines, 1, Output, 'fail')

        raises(InputException, scenario_tester.test, scenario)

    def test_match_fail(self):
        class Application(AbstractApplication):
            def interpret(self, input):
                if input == 'a':
                    return 42

        scenario = '''
>>> a = 4
>>> a
5
'''

        scenario_tester = ScenarioTester(Application)
        scenario_tester.parse(scenario)
        lines = scenario_tester.lines

        assert len(lines) == 3
        self.assert_line(lines, 1, Input, 'a = 4')
        self.assert_line(lines, 2, Input, 'a')
        self.assert_line(lines, 3, Output, '5')

        raises(MatchException, scenario_tester.test, scenario)

    def test_output_fail(self):
        class Application(AbstractApplication):
            def interpret(self, input):
                return 42

        scenario = '''
>>> fail
>>> fail
'''

        scenario_tester = ScenarioTester(Application)
        scenario_tester.parse(scenario)
        lines = scenario_tester.lines

        assert len(lines) == 2
        self.assert_line(lines, 1, Input, 'fail')
        self.assert_line(lines, 2, Input, 'fail')

        raises(OutputException, scenario_tester.test, scenario)

    def assert_line(self, lines, line_number, line_type, line_content):
        line = lines[line_number - 1]
        assert isinstance(line, line_type)
        assert line.content == line_content
