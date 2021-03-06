from mock import patch
from placidity.application import Application, KeyboardInput
from placidity.scenario_tester import ScenarioTester
from placidity.threads import InputThread

class InputTester(InputThread):
    def get_data(self):
        return None

class ApplicationTester(Application):
    input_source = InputTester

@patch('__builtin__.raw_input')
def test_input_prefix(input_mock):
    # Note that prefix has to be tested separately as scenario tester
    # operates only on pure input. It just happens to use the same syntax
    # for input.
    keyboard_input = KeyboardInput()

    keyboard_input.get_data()

    input_mock.assert_called_with('>>> ')

class TestApplication:
    scenario_tester = ScenarioTester(ApplicationTester)

    def test_math(self):
        scenario = '''
>>> a = 5
>>> b = 10
>>> a + b
15
>>> 15 * 3
45
'''

        self.scenario_tester.test(scenario)

    def test_variables(self):
        scenario = '''
>>> a = 5
>>> b = 10
>>> a
5
>>> c
null
>>> a = c
null
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

    def test_eliza(self):
        scenario = '''
>>> a = 5
>>> a
5
>>> eliza
Hello. How are you feeling today?
>>> a
...
>>> Yeah. Right!
...
>>> quit
...
>>> a
5
'''

        self.scenario_tester.test(scenario)

    def test_quit(self):
        scenario = '''
>>> a = 10
>>> a
10
>>> quit
--- not running
--- restart
>>> a
null
'''

        self.scenario_tester.test(scenario)
