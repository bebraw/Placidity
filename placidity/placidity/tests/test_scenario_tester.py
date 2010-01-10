from placidity.scenario_tester import Input, InputError, MatchError, \
Output, OutputError, ScenarioTester
from py.test import raises

class AbstractApplication:
    def run(self):
        try:
            while True:
                input = self.input()

                result = self.interpret(input)

                if result:
                    self.output(result)
        except SystemExit:
            pass

class TestScenarioTester:
    def test_passing_test(self):
        class Application(AbstractApplication):
            def interpret(self, input):
                if input == 'a':
                    return 4

        scenario = '''
>>> a = 4
>>> a
4
'''

        scenario_tester = ScenarioTester(Application)
        scenario_tester.parse(scenario)
        lines = scenario_tester.lines

        assert len(lines) == 3
        self.assert_line(lines, 1, Input, 'a = 4')
        self.assert_line(lines, 2, Input, 'a')
        self.assert_line(lines, 3, Output, '4')

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

        raises(InputError, scenario_tester.test, scenario)

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

        raises(MatchError, scenario_tester.test, scenario)

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

        raises(OutputError, scenario_tester.test, scenario)

    def assert_line(self, lines, line_number, line_type, line_content):
        line = lines[line_number - 1]
        assert isinstance(line, line_type)
        assert line.content == line_content
