class PluginLoader:

    def load(self, directory):
        ret = []

        for plugin in directory.children:
            plugin_file = plugin.find(name=plugin.name, type='py')
            plugin_class = plugin_file.classes[plugin.name]

            if not hasattr(plugin_class, 'matches'):
                def matches(self, expression):
                    if isinstance(self.aliases, str):
                        return expression == self.aliases

                    return expression in self.aliases

                plugin_class.matches = matches

            plugin_instance = plugin_class()
            ret.append(plugin_instance)

        return ret
