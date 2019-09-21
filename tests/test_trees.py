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
class TestTreeClass:
    def test_empty_tree_creation(self):
        t = Tree()
        # empty tests
        assert t.is_empty() and len(t) == 0
        # key lookup failure
        with pytest.raises(KeyError):
            ignored = t['foo']

        # Key errors on methods lookup methods
        for name in ['parent', 'children', 'ancestors', 'path',
                     'siblings']:
            method = getattr(t, name)
            with pytest.raises(KeyError):
                ignored = method('foo')
        # Empty list return for method returning sequences or iterables
        for name in ['leaves', 'inorder', 'postorder', 'preorder',
                     'levelorder']:
            method = getattr(t, name)
            assert list(method()) == []

    def test_root_creation(self):
        key, value = 'foo', 100
        t = Tree(key=key, value=value)  # Single node tree
        assert (
                t.root_key == key and
                t.root_value == t[key] == value and
                key in t and
                t.is_leaf(key=key) and
                t.is_root(key=key) and
                t.parent(key=key) is EMPTY and
                t.children(key=key) == [] and
                t.siblings(key=key) == [] and
                t.ancestors(key=key) == [] and
                t.path(key=key) == [value] and
                t.leaves() == [value] and
                len(t) == 1 and
                list(t.inorder()) == [value] and
                list(t.postorder()) == [value] and
                list(t.preorder()) == [value] and
                list(t.levelorder()) == [value]
        )

    def test_appending_to_root_node(self):
        root_key, root_value = 'foo', 100
        t = Tree()
        t.append(key=root_key, value=root_value)  # Add root node
        t2 = Tree(key=root_key, value=root_value)  # Create with a root node
        assert t == t2
        # Add two children to root
        children = [('bar', 101), ('baz', 201)]
        for k, v in children:
            t.append(key=k, value=v)  # Add child to root
        assert t.siblings(children[0][0]) == children[1][1]
        assert t.siblings(children[1][0]) == children[0][1]
        # check ancestry
        for k, v in children:
            assert t.parent(key=k) == t.root_value
            assert t.ancestors(key=k) == [t.root_value]
            assert t.path(key=k) == [t.root_value, t[k]]
            assert t[k] == v

        assert t.leaves() == [v for _, v in children]
        assert len(t) == len(t.leaves()) + 1
        inorder = t.inorder()
        inorder = t.inorder()

        assert (
                not t.is_leaf('foo') and
                list(t.inorder()) == [t.leaves()[0], t.root_value, t.leaves()[1]] and
                list(t.postorder()) == [*t.leaves(), t.root_value] and
                list(t.preorder()) == [t.root_value, *t.leaves()] and
                list(t.levelorder()) == [t.root_value, *t.leaves()]
        )
        # Extending children
        t3 = Tree(key=t.root_key, value=t.root_value)  # Create with a root node
        t3.extend(children=children)  # Takes iterable of pairs
        assert t3 == t
        old_leaf_key = children[0][0]
        new_child_key, new_child_value = 'ham', 401
        t.append(key=new_child_key, value=new_child_value, parent=old_leaf_key)
        assert (
                not t.is_leaf(key=old_leaf_key) and
                t.ancestors(key=new_child_key) == [t[old_leaf_key],
                                                   *t.ancestors(key=old_leaf_key)] and
                t.path(key=new_child_key) == [*t.path(key=old_leaf_key),
                                              t[new_child_key]] and
                list(t.inorder()) == [101, 100, 301, 201] and
                list(t.postorder()) == [101, 301, 201, 100] and
                list(t.preorder()) == [100, 101, 201, 301] and
                list(t.bfs()) == [100, 101, 201, 301]
        )
