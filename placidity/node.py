# -*- coding: utf-8 -*-
class AbstractNode(object):
    def _generic_find(self, node_list_name, **kvargs):
        found_nodes = self._generic_recursion(node_list_name, kvargs, [], [])
        return self._check_found_nodes(found_nodes)

    def _generic_recursion(self, node_list_name, search_clauses, found_nodes,
            visited_nodes):
        visited_nodes.append(self)
        nodes = getattr(self, node_list_name)

        for node in nodes:
            try:
                all_match = True
                for wanted_attribute, wanted_value in search_clauses.items():
                    attribute = getattr(node, wanted_attribute)

                    if attribute != wanted_value:
                        all_match = False
                        break

                if all_match:
                    found_nodes.append(node)
            except AttributeError:
                pass

            if node not in visited_nodes:
                node._generic_recursion(node_list_name, search_clauses,
                    found_nodes, visited_nodes)

        return found_nodes

    def _check_found_nodes(self, found_nodes):
        if len(found_nodes) > 0:
            return found_nodes[0] if len(found_nodes) == 1 else found_nodes

class Node(AbstractNode):

    def __init__(self):
        self.children = NodeContainer(self, complementary_items_name='parents')
        self.parents = NodeContainer(self, complementary_items_name='children')

    def walk(self):
        def _walk(nodes):
            for node in nodes:
                for child in _walk(node.children):
                    yield child

                yield node

        yield self

        for child_walk_node in _walk(self.children):
            yield child_walk_node

    def find_parent_with_attribute(self, attribute):
        return self._find_first_node_with_attribute('parents', attribute, [])

    def _find_first_node_with_attribute(self, node_list_name, attribute,
            visited_nodes):
        visited_nodes.append(self)
        nodes = getattr(self, node_list_name)

        for node in nodes:
            if hasattr(node, attribute):
                return node

            if node not in visited_nodes:
                return node._find_first_node_with_attribute(node_list_name,
                    attribute, visited_nodes)

    def find_child(self, **kvargs):
        return self._generic_find(node_list_name='children', **kvargs)

    def find_parent(self, **kvargs):
        return self._generic_find(node_list_name='parents', **kvargs)

    def find_root(self):
        return self._generic_find(node_list_name='parents', parents=[])


class TreeNode(AbstractNode):

    def __init__(self):
        self.children = NodeContainer(self, complementary_items_name='_parents')
        # XXX: this is bit of a hack but at least it allows to use generic
        # search
        self._parents = NodeContainer(self, complementary_items_name='children')

    @property
    def parent(self):
        return self._parents[0]

    @parent.setter
    def parent(self, value):
        assert len(self._parents) <= 1

        if len(self._parents) == 1:
            self._parents.remove(self._parents[0])
        
        value.children.append(self)

    def find(self, **kvargs):
        return self._generic_find(node_list_name='children', **kvargs)


class NodeContainer(list):

    def __init__(self, owner, complementary_items_name):
        super(NodeContainer, self).__init__()
        self.owner = owner
        self.complementary_items_name = complementary_items_name

    def append(self, *items):
        for item in items:
            if item not in self:
                super(NodeContainer, self).append(item)
                complementary_items = getattr(item,
                    self.complementary_items_name)
                complementary_items.append(self.owner)

    def remove(self, *items):
        for item in items:
            if item in self:
                super(NodeContainer, self).remove(item)
                complementary_items = getattr(item,
                    self.complementary_items_name)
                complementary_items.remove(self.owner)
