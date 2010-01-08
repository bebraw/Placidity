from placidity.application import Application
from placidity.scenario_tester import ScenarioTester

class TestApplication:
    scenario_tester = ScenarioTester(Application)

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

# TODO: figure out why 'a = 5' etc. fail!
# test
#>>> c
#null
    def test_variables(self):
        scenario = '''
>>> a=5
>>> b=10
>>> a
5
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
