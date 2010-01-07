from mock import Mock
from placidity.plugin_loader import PluginLoader

class Alias:
    aliases = 'foo'

class Matches:
    def matches(self, expression):
        return True

class MultipleAliases:
    aliases = ('vars', 'variables')

class TestPluginLoader:

    def setup_method(self, method):
        plugin_dir = Mock()
        alias_dir = self.create_plugin_dir('alias', Alias)
        matches_dir = self.create_plugin_dir('matches', Matches)
        multiplealiases_dir = self.create_plugin_dir('multiplealiases',
            MultipleAliases)
        plugin_dir.children = (alias_dir, matches_dir,
            multiplealiases_dir)

        plugin_loader = PluginLoader()
        self.plugins = plugin_loader.load(plugin_dir)

    def test_load_plugins(self):
        classes = [Alias, Matches, MultipleAliases]

        for plugin, klass in zip(self.plugins, classes):
            assert isinstance(plugin, klass)

    def test_alias(self):
        alias = self.plugins[0]

        assert alias.matches('foo')
        assert not alias.matches('bar')

    def test_matches(self):
        matches = self.plugins[1]

        assert matches.matches('bar')
        assert matches.matches('foo')

    def test_multiple_aliases(self):
        multiple_aliases = self.plugins[2]

        assert multiple_aliases.matches('vars')
        assert multiple_aliases.matches('variables')
        assert not multiple_aliases.matches('foobar')

    def create_plugin_dir(self, plugin_name, plugin_class):
        plugin_dir = Mock()
        plugin_dir.name = plugin_name
        plugin_dir.children = Mock()

        plugin_file = self.create_plugin_file(plugin_name, plugin_class)

        def find(name, type):
            assert type == 'py'
            if name is plugin_name:
                return plugin_file

        plugin_dir.find = find

        return plugin_dir

    def create_plugin_file(self, name, klass):
        plugin_file = Mock()
        plugin_file.classes = {name: klass, }

        return plugin_file
