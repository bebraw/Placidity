from placidity.application import Application

class TestApplication:
    scenario_tester = ScenarioTester(Application)

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
