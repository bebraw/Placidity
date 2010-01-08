from placidity.scenario_tester import ScenarioTester

# TODO: test exceptions!

class TestScenarioTester:
    def test_test(self):
        class Application:
            def run(self):
                input = self.input()
                result = self.interpret(input)

                if result:
                    self.output(result)

            def interpret(self, input):
                if input == 'a':
                    return 4
        
        scenario = '''
>>> a = 4
>>> a
4
        '''

        scenario_tester = ScenarioTester(Application)

        scenario_tester.test(scenario)
