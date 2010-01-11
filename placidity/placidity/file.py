import inspect
import imp
import os
import sys
from node import TreeNode

class File(TreeNode):

    def __init__(self, path=None, name=None):
        super(File, self).__init__()

        parts = self.__init_attributes(path, name)
        self.__init_structure(parts)
        self.__init_classes(path)

    def __init_attributes(self, path, name=None):
        parts = []
        self.name = name
        self.type = None
        self.classes = {}

        if isinstance(path, str):
            parts = path.split('/')

            if len(parts) == 1:
                parts = path.split('\\')

            last_part_split = parts[-1].split('.')
            self.name = last_part_split[0]

            if len(last_part_split) > 1:
                self.type = last_part_split[1]

        return parts

    def __init_classes(self, path):
        if path is None:
            return

        if os.path.isdir(path):
            for child in os.listdir(path):
                child_path = os.path.join(path, child)
                self.children.append(File(child_path))
        elif self.type == 'py':
            try:
                sys.path.append(os.path.dirname(path))
                module = imp.load_source(os.path.basename(path), path)
            except Exception, e:
                print e
                return

            module_classes = inspect.getmembers(module, inspect.isclass)

            for name, klass in module_classes:
                self.classes[name.lower()] = klass

    def __init_structure(self, parts):
        prev_node = self
        
        for part in reversed(parts[:-1]):
            prev_node.parent = File(name=part)
            prev_node = prev_node.parent

class PluginDirectory(File):

    def __init__(self):
        super(PluginDirectory, self).__init__(self.plugin_path)

    @property
    def plugin_path(self):
        return os.path.join(self.current_directory, 'commands')

    @property
    def current_directory(self):
        # http://code.activestate.com/recipes/474083/#c8
        return os.path.dirname(os.path.realpath(__file__))
