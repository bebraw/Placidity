from placidity.scenario_tester import EllipsisOutput, Input, InputError, \
NotRunningError, MatchError, Meta, Output, OutputError, RunningError, \
ScenarioTester
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

    def interpret(self, input):
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

    def test_running(self):
        class Application(AbstractApplication):
            pass
        
        scenario = '''
>>> a = 4
--- running
>>> b = 5
--- running
'''

        scenario_tester = ScenarioTester(Application)
        scenario_tester.parse(scenario)
        lines = scenario_tester.lines

        assert len(lines) == 4
        self.assert_line(lines, 1, Input, 'a = 4')
        self.assert_line(lines, 2, Meta, 'running')
        self.assert_line(lines, 3, Input, 'b = 5')
        self.assert_line(lines, 4, Meta, 'running')

        # this should not trigger any asserts
        scenario_tester.test(scenario)

    def test_running_fail(self):
        class Application(AbstractApplication):
            def interpret(self, input):
                if input == 'quit':
                    raise SystemExit

        scenario = '''
>>> a = 4
--- running
>>> quit
--- running
'''

        scenario_tester = ScenarioTester(Application)
        scenario_tester.parse(scenario)
        lines = scenario_tester.lines

        assert len(lines) == 4
        self.assert_line(lines, 1, Input, 'a = 4')
        self.assert_line(lines, 2, Meta, 'running')
        self.assert_line(lines, 3, Input, 'quit')
        self.assert_line(lines, 4, Meta, 'running')

        raises(NotRunningError, scenario_tester.test, scenario)

    def test_not_running(self):
        class Application(AbstractApplication):
            def interpret(self, input):
                if input == 'quit':
                    raise SystemExit

        scenario = '''
>>> quit
--- not running
'''

        scenario_tester = ScenarioTester(Application)
        scenario_tester.parse(scenario)
        lines = scenario_tester.lines

        assert len(lines) == 2
        self.assert_line(lines, 1, Input, 'quit')
        self.assert_line(lines, 2, Meta, 'not running')

        # this should not trigger any asserts
        scenario_tester.test(scenario)

    def test_not_running_fail(self):
        class Application(AbstractApplication):
            pass

        scenario = '''
>>> a = 5
--- not running
'''

        scenario_tester = ScenarioTester(Application)
        scenario_tester.parse(scenario)
        lines = scenario_tester.lines

        assert len(lines) == 2
        self.assert_line(lines, 1, Input, 'a = 5')
        self.assert_line(lines, 2, Meta, 'not running')

        raises(RunningError, scenario_tester.test, scenario)

    def test_restart(self):
        class Application(AbstractApplication):
            def interpret(self, input):
                if input == 'quit':
                    raise SystemExit

        scenario = '''
>>> quit
--- not running
--- restart
--- running
--- restart
--- running
'''

        scenario_tester = ScenarioTester(Application)
        scenario_tester.parse(scenario)
        lines = scenario_tester.lines

        assert len(lines) == 6
        self.assert_line(lines, 1, Input, 'quit')
        self.assert_line(lines, 2, Meta, 'not running')
        self.assert_line(lines, 3, Meta, 'restart')
        self.assert_line(lines, 4, Meta, 'running')
        self.assert_line(lines, 5, Meta, 'restart')
        self.assert_line(lines, 6, Meta, 'running')

        # this should not trigger any asserts
        scenario_tester.test(scenario)

    def test_ellipsis(self):
        class Application(AbstractApplication):
            def interpret(self, input):
                if input == 'a':
                    return 5

        scenario = '''
>>> a = 5
>>> a
...
'''

        scenario_tester = ScenarioTester(Application)
        scenario_tester.parse(scenario)
        lines = scenario_tester.lines

        assert len(lines) == 3
        self.assert_line(lines, 1, Input, 'a = 5')
        self.assert_line(lines, 2, Input, 'a')
        self.assert_line(lines, 3, EllipsisOutput, None)

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
