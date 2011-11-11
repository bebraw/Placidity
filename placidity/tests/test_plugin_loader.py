from mock import Mock
from placidity.plugin_loader import PluginLoader

class AbstractTest:
    def load_plugins(self, classes):
        return [self.load_plugin(klass) for klass in classes]

    def load_plugin(self, klass):
        plugin_dir = Mock()
        # TODO: neater without tuple (add test to node for this)
        plugin_dir.children = (self.create_plugin_dir(klass), )

        plugin_loader = PluginLoader()
        plugins = plugin_loader.load(plugin_dir)
        return plugins[0]

    def create_plugin_dir(self, klass):
        plugin_name = klass.__name__.lower()
        plugin_dir = Mock()
        plugin_dir.name = plugin_name
        plugin_dir.children = Mock()

        plugin_file = self.create_plugin_file(plugin_name, klass)

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

class TestAlias(AbstractTest):
    def test_single(self):
        class Alias:
            aliases = 'foo'

        alias = self.load_plugin(Alias)

        assert alias.matches('foo')
        assert not alias.matches('bar')

    def test_no_alias(self):
        class NoAlias:
            pass

        no_alias = self.load_plugin(NoAlias)

        assert no_alias.aliases == ''

    def test_multiple(self):
        class MultipleAliases:
            aliases = ('vars', 'variables')

        multiple_aliases = self.load_plugin(MultipleAliases)

        assert multiple_aliases.matches('vars')
        assert multiple_aliases.matches('variables')
        assert not multiple_aliases.matches('foobar')

class TestLoadPlugins(AbstractTest):
    def test_load_plugins(self):
        def produce_classes(class_names):
            def produce_class(class_name):
                return type(class_name, (), {})

            return [produce_class(class_name) for class_name in class_names]

        class_names = ('bar', 'baz', 'foo', )
        classes = produce_classes(class_names)
        plugins = self.load_plugins(classes)

        for plugin, klass in zip(plugins, classes):
            assert isinstance(plugin, klass)

class TestMatches(AbstractTest):
    def test_matches(self):
        class Matches:
            def matches(self, expression):
                return True

        plugin = self.load_plugin(Matches)

        assert plugin.matches('bar')
        assert plugin.matches('foo')

class TestPriority(AbstractTest):
    def test_valid_priority(self):
        def produce_priorities(priorities):
            def produce_priority(priority):
                return type('Priority', (), {'priority': priority, })

            return [produce_priority(priority) for priority in priorities]

        priorities = ('low', 'normal', 'high', )
        classes = produce_priorities(priorities)
        plugins = self.load_plugins(classes)

        for plugin in plugins:
            assert plugin.priority in priorities

    def test_invalid_priority(self):
        class InvalidPriority:
            priority = 'foobar'

        plugin = self.load_plugin(InvalidPriority)

        assert plugin.priority == 'normal'

    def test_missing_priority(self):
        class MissingPriority:
            pass

        plugin = self.load_plugin(MissingPriority)

        assert plugin.priority == 'normal'
