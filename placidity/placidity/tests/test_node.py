# -*- coding: utf-8 -*-
from placidity.node import Node, TreeNode


class TestNode():

    def test_append_children_to_node(self):
        node1, node2 = Node(), Node()

        node1.children.append(node2)

        assert node1.children[0] == node2
        assert node2.parents[0] == node1

    def test_append_parents_to_node(self):
        node1, node2 = Node(), Node()

        node1.parents.append(node2)

        assert node1.parents[0] == node2
        assert node2.children[0] == node1

    def test_append_same_node_as_child_and_parent(self):
        node1, node2 = Node(), Node()

        node1.children.append(node2)
        node1.parents.append(node2)

        assert node1.children[0] == node2
        assert node1.parents[0] == node2

        assert node2.children[0] == node1
        assert node2.parents[0] == node1

    def test_append_same_node_as_child_multiple_times(self):
        node1, node2 = Node(), Node()

        node1.children.append(node2)
        node1.children.append(node2)
        node1.children.append(node2)

        assert node1.children[0] == node2
        assert node2.parents[0] == node1

        assert len(node1.children) == 1
        assert len(node2.parents) == 1

    def test_append_same_node_as_parent_multiple_times(self):
        node1, node2 = Node(), Node()

        node1.parents.append(node2)
        node1.parents.append(node2)
        node1.parents.append(node2)

        assert node1.parents[0] == node2
        assert node2.children[0] == node1

        assert len(node1.parents) == 1
        assert len(node2.children) == 1

    def test_multi_append(self):
        node1, node2, node3 = Node(), Node(), Node()

        node1.children.append(node2, node3)

        assert len(node1.children) == 2
        assert node2 in node1.children
        assert node3 in node1.children

    def test_remove_child_node(self):
        node1, node2 = Node(), Node()

        node1.children.append(node2)
        node1.children.remove(node2)

        assert len(node1.children) == 0
        assert len(node2.parents) == 0

    def test_remove_parent_node(self):
        node1, node2 = Node(), Node()

        node1.parents.append(node2)
        node1.parents.remove(node2)

        assert len(node1.parents) == 0
        assert len(node2.children) == 0

    def test_remove_same_node_multiple_times(self):
        node1, node2 = Node(), Node()

        node1.parents.append(node2)
        node1.parents.remove(node2)
        node1.parents.remove(node2)
        node1.parents.remove(node2)

        assert len(node1.parents) == 0
        assert len(node2.children) == 0

    def test_multi_remove(self):
        node1, node2, node3 = Node(), Node(), Node()

        node1.children.append(node2, node3)
        node1.children.remove(node2, node3)

        assert len(node1.children) == 0

    def test_find_immediate_child_node(self):
        node1, node2 = Node(), Node()
        node2.name = 'node to be found'

        node1.children.append(node2)

        assert node1.find_child(name='node to be found') == node2

    def test_find_child_node_no_results(self):
        node1 = Node()

        assert node1.find_child(name='just some name') == None

    def test_find_child_node_from_node_tree(self):
        node1 = Node()
        node1a = Node()
        node1a1 = Node()
        node1a1.color = 'blue'
        node1a2 = Node()
        node1a2.value = 13
        node1b = Node()
        node1b1 = Node()
        node1b1.find_me = True
        node1b1.color = 'blue'

        node1.children.append(node1a, node1b)
        node1a.children.append(node1a1, node1a2)
        node1b.children.append(node1b1)

        assert node1.find_child(value=13) == node1a2
        assert node1.find_child(find_me=True) == node1b1
        assert node1.find_child(color='blue') == [node1a1, node1b1]

    def test_find_immediate_parent_node(self):
        node1, node2 = Node(), Node()
        node2.name = 'node to be found'

        node1.parents.append(node2)

        assert node1.find_parent(name='node to be found') == node2

    def test_find_parent_node_no_results(self):
        node1 = Node()

        assert node1.find_parent(name='just some name') == None

    def test_find_parent_node_from_node_tree(self):
        node1 = Node()
        node1a = Node()
        node1a1 = Node()
        node1a1.color = 'blue'
        node1a2 = Node()
        node1a2.value = 13
        node1b = Node()
        node1b1 = Node()
        node1b1.find_me = True
        node1b1.color = 'blue'

        node1.parents.append(node1a, node1b)
        node1a.parents.append(node1a1, node1a2)

        node1b.parents.append(node1b1)

        assert node1.find_parent(value=13) == node1a2
        assert node1.find_parent(find_me=True) == node1b1
        assert node1.find_parent(color='blue') == [node1a1, node1b1]
        assert node1.find_parent(find_me=True, color='blue') == node1b1

    def test_find_root(self):
        node1, node1a, node1b, node1a1 = Node(), Node(), Node(), Node()

        node1.children.append(node1a, node1b)
        node1a.children.append(node1a1)

        assert node1.find_root() == None
        assert node1a.find_root() == node1
        assert node1b.find_root() == node1
        assert node1a1.find_root() == node1

    def test_cyclic_find(self):
        node1, node2 = Node(), Node()

        node1.children.append(node2)
        node2.children.append(node1)

        assert node1.find_root() == None
        assert node2.find_root() == None

    def test_find_parent_with_value_name(self):
        node1, node2, node3 = Node(), Node(), Node()
        node3.attribute_to_find = 'find me'

        node1.parents.append(node2)
        node2.parents.append(node3)

        assert node1.find_parent_with_attribute('attribute_to_find') == node3

    def test_walk(self):
        node1, node2, node3, node4 = Node(), Node(), Node(), Node()
        node5 = Node()

        node1.children.append(node2)
        node1.children.append(node5)

        node2.children.append(node3)
        node2.children.append(node4)

        result = (node1, node3, node4, node2, node5 )

        for i, node in enumerate(node1.walk()):
            assert node == result[i], '%s %s %s' % (i, node, result[i])


class TestTreeNode():

    def test_set_parent(self):
        node1, node2 = TreeNode(), TreeNode()

        node1.parent = node2
        assert node1.parent == node2
        assert node2.children == [node1, ]

    def test_set_parent_twice(self):
        node1, node2, node3 = TreeNode(), TreeNode(), TreeNode()

        node1.parent = node2
        node1.parent = node3
        assert node2.children == []
        assert node3.children == [node1, ]

    def test_find(self):
        node1, node2, node3 = TreeNode(), TreeNode(), TreeNode()

        node2.parent = node1
        node3.parent = node1
        node2.name = 'foo'
        node3.name = 'bar'

        assert node1.find(name='foo') == node2
        assert node1.find(name='bar') == node3
        assert node1.find(name='dummy') == None
        assert node2.find(name='foo') == None
