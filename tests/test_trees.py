# tests/test_trees.py
#
# forestry: Python Tree data structures and tools
#
# Copyright (C) 2019  by Dwight D. Cummings
#
# This module is part of `forestry` and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
"""Unit tests for module trees.py"""

# Python Standard Library imports
# Third-party library imports
import pytest
# Import contents of module tested
from forestry.trees import _Node, Tree, EMPTY

##~ Common Snippets
"""
@pytest.fixture(scope='session')
@pytest.fixture(scope='module')
@pytest.mark.parametrize(
    'name, attrs, string',
    [
        ('t', None, '<t></t>'),
        ('t', {'a': 1, 'b': 2}, '<t a="1" b="2"></t>'),
        ('t', {'a': 1, 'b': 2, 's1': {'a': 1, 'b': 2}}
         , '<t a="1" b="2"><s1 a="1" b="2"></s1></t>'),
    ]
)


    with pytest.raises(AssertionError,
                       match='search tag cannot be `None`'):
                       
"""


# Helpers
# Fixtures
# Unit Tests
class Test_NodeClass:
    def test_normal_creation(self):
        assert _Node(value=100, parent='foo') == (100, 'foo')

    def test_creation_with_defaults(self):
        assert _Node(value=200) == (200, EMPTY)

    def test_bad_creation(self):
        with pytest.raises(TypeError):
            # Missing value!
            _Node(parent='bar')
        with pytest.raises(TypeError):
            # Missing value!
            _Node()

    def test_attribute_access(self):
        n = _Node(value=100, parent='foo')
        assert n.value == 100 and n.parent == 'foo'


class TestTreeClass:
    def test_empty_tree_creation(self):
        t = Tree()
        # empty tests
        assert t.is_empty()
        # key lookup
        with pytest.raises(KeyError):
            ignored = t['foo']

        for name in ['parent', 'children', 'ancestors', 'path'
                     'siblings']:
            attr = getattr(t, name)
            with pytest.raises(KeyError):
                ignored = attr('foo')

        assert (
                t.leafs() == [] and
                len(t) == 0 and
                list(t.inorder()) == [] and
                list(t.postorder()) == [] and
                list(t.preorder()) == [] and
                list(t.bfs()) == []
        )

    def test_root_creation(self):
        t = Tree(key='foo', value=100)  # Single node tree
        assert (
                t['foo'] == t[t.root_key] == t.root_value == 100 and
                'foo' in t and
                t.is_leaf(key='foo') and
                t.is_root(key='foo') and
                t.parent(key='foo') is EMPTY and
                t.children(key='foo') == [] and
                t.siblings(key='foo') == [] and
                t.ancestors(key='foo') == [] and
                t.path(key='foo') == ['foo'] and
                t.leaves() == [100] and
                len(t) == 1 and
                list(t.inorder()) == [100] and
                list(t.postorder()) == [100] and
                list(t.preorder()) == [100] and
                list(t.bfs()) == [100]
        )

    def test_appending_to_root_node(self):
        t = Tree()
        t.append(key='foo', value=100)  # Add root node
        t2 = Tree(key='foo', value=100)  # Create with a root node
        assert t == t2
        # Add two children to root
        children = [('bar', 101), ('baz', 201)]
        for k, v in children:
            t.append(key=k, value=v)  # Add child to root
        assert t.siblings('bar') == [201]
        assert t.siblings('baz') == [202]
        # check ancestry
        for k, v in children:
            assert t.parent(key=k) == t.root_value
            assert t.ancestors(key=k) == t.root_value
            assert t.path(key=k) == [t.root_value, t[k]]
            assert t[k] == v

        assert t.leaves() == [v for _, v in children]
        assert len(t) == len(t.leaves()) + 1

        assert (
            not t.is_leaf('foo') and
            list(t.inorder()) == t.leaves()[0] + [t.root_value] + t.leaves()[1:] and
            list(t.postorder()) == t.leaves() + [t.root_value] and
            list(t.preorder()) == [t.root_value] + t.leaves() and
            list(t.bfs()) == [t.root_value] + t.leaves()
        )
        # Extending children
        t2 = Tree(key=t.root_key, value=t.root_value)  # Create with a root node
        t2.extend(children=children)  # Takes iterable of pairs
        assert t2 == t

    def test_ancestry(self):
        t = Tree(key='foo', value=100)
        t.extend(children=[('bar', 101), ('baz', 201)])
        t.append(key='spam', value=301, parent='baz')
        assert (
                t.is_leaf(key='bar') and
                not t.is_leaf(key='baz') and
                t.parent(key='bar') == 100 and
                t.parent(key='spam') == 201 and
                t.children(key='foo') == [101, 201] and
                t.ancestors(key='spam') == [201, 100] and
                t.path(key='spam') == [100, 201, 301] and
                t.leaves == [101, 301] and
                list(t.inorder()) == [101, 100, 301, 201] and
                list(t.postorder()) == [101, 301, 201, 100] and
                list(t.preorder()) == [100, 101, 201, 301] and
                list(t.bfs()) == [100, 101, 201, 301]
        )

    def test_attach_subtrees(self):
        ...

    def test_adding_nodes(self):
        ...

    def test_querying_the_tree(self):
        ...

    def test_traversals(self):
        ...
