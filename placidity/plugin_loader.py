class PluginLoader:

    def load(self, directory):
        ret = []

        for plugin in directory.children:
            plugin_file = plugin.find(name=plugin.name, type='py')
            plugin_class = plugin_file.classes[plugin.name]

            self._check_attributes(plugin_class)

            plugin_instance = plugin_class()
            ret.append(plugin_instance)

        return ret

    def _check_attributes(self, klass):
        self._check_aliases(klass)
        self._check_matches(klass)
        self._check_priority(klass)

    def _check_aliases(self, klass):
        self._check_attribute(klass, 'aliases', '')

    def _check_matches(self, klass):
        def matches(self, expression):
            if isinstance(self.aliases, str):
                return expression == self.aliases

            return expression in self.aliases

        self._check_attribute(klass, 'matches', matches)

    def _check_priority(self, klass):
        self._check_attribute(klass, 'priority', 'normal')

        if klass.priority not in ('low', 'normal', 'high'):
            klass.priority = 'normal'

    def _check_attribute(self, klass, attribute, value):
        if not hasattr(klass, attribute):
            setattr(klass, attribute, value)
