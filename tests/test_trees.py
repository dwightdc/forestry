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
from collections import namedtuple, deque
import random
from uuid import uuid4
# Third-party library imports
import pytest
# Import contents of module being tested
from forestry.trees import Tree, EMPTY

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
Node = namedtuple('Node', 'key value')
MAXINT = 100_000_000_000


# Fixtures
@pytest.fixture(scope='function')
def get_random_nodes_gen():
    """Returns a function which returns a sequence of random nodes."""

    def _get_random_nodes(n_nodes):
        for ignored in range(n_nodes):
            rand_key = str(uuid4())
            rand_value = random.randint(0, MAXINT)
            yield Node(rand_key, rand_value)

    return _get_random_nodes


@pytest.fixture(scope='function')
def get_random_nodes_list():
    """Returns a function which returns a sequence of random nodes."""

    def _get_random_nodes(n_nodes):
        random_nodes = []
        for ignored in range(n_nodes):
            rand_key = str(uuid4())
            rand_value = random.randint(0, MAXINT)
            random_nodes.append(Node(rand_key, rand_value))

        return random_nodes

    return _get_random_nodes


@pytest.fixture(scope='function')
def random_node(get_random_nodes_gen):
    """Returns a single random node."""
    return next(get_random_nodes_gen(1))
    # rand_key = str(uuid4())
    # rand_value = random.randint(0, MAXINT)
    # return Node(rand_key, rand_value)


@pytest.fixture(scope='module')
def empty_tree():
    """Return tree with no nodes"""
    return Tree()


@pytest.fixture(scope='function')
def single_node_tree(random_node):
    """Return tree with a single node and its key value pair"""
    t = Tree(key=random_node.key, value=random_node.value)
    return t, random_node


@pytest.fixture(scope='function')
def multi_level_tree(get_random_nodes_list):
    """Return multi level tree.

    Randomize arity per node to make for a varied tree
    each time
    """
    # arity = random.randint(1, 4)
    # n_levels = random.randint(2, 100)
    # n_nodes = sum(arity ** level for level in range(n_levels))
    n_nodes = random.randint(3, 100)
    random_nodes = get_random_nodes_list(n_nodes)
    first_node = random_nodes[0]
    t = Tree(key=first_node.key, value=first_node.value)
    queue = deque()
    enqueue = queue.append
    dequeue = queue.popleft
    current_arity = 0
    target_arity = random.randint(1, 10)
    assert current_arity <= target_arity
    target_node_key = first_node.key
    # print()
    for node in random_nodes[1:]:  # Remaining nodes after first
        # print([t[e] for e in queue])
        if current_arity < target_arity:
            t.append(key=node.key, value=node.value, parent=target_node_key)
            enqueue(node.key)
            current_arity += 1
            continue

        target_node_key = dequeue()
        t.append(key=node.key, value=node.value, parent=target_node_key)
        enqueue(node.key)
        current_arity = 1
        target_arity = random.randint(1, 10)

    return t, random_nodes


@pytest.fixture(scope='function')
def multi_level_tree2(get_random_nodes_list):
    """Return multi level tree.

    Randomize arity per node to make for a varied tree
    each time
    """
    deq = deque()
    random_nodes = get_random_nodes_list(random.randint(3, 25))
    first_node = random_nodes[0]
    t = Tree(key=first_node.key, value=first_node.value)
    target_node_key = first_node.key
    for node in random_nodes[1:]:
        t.append(key=node.key, value=node.value, parent=target_node_key)
        deq.append(node.key)
        # flip a coin to keep the same target node or change targets
        if random.randint(0, 2) == 1:  # change target
            target_node_key = deq.popleft()

    return t, random_nodes


# add the root
# target = root
# arity = 0
# for node in nodes:
#   if arit < 2:
#       add node
#       enque node
#       arity+= 1
#       continue
#
#   target = deque(q)
#   arity = 0
#
#
#   if current_arity == 2
#     target = dequeue(q)
#     add to target
#     push node to q
#     curent_arity = 1
#     continue
#
#   add to target
#   push node to q
#   curent_arity += 1


# Unit Tests
class TestTreeClass:
    def test_empty_tree(self, empty_tree, random_node):
        # empty tests
        assert empty_tree.is_empty() and len(empty_tree) == 0
        # key lookup failure
        with pytest.raises(KeyError):
            ignored = empty_tree[random_node.key]

        # Key errors on methods lookup methods
        for name in ['ancestors', 'children', 'level', 'parent', 'path',
                     'siblings']:
            method = getattr(empty_tree, name)
            with pytest.raises(KeyError):
                ignored = method(random_node.key)
        # Empty list return for method returning sequences or iterables
        for name in ['leaves', 'inorder', 'postorder', 'preorder',
                     'levelorder']:
            method = getattr(empty_tree, name)
            assert list(method()) == []

    def test_single_node_tree(self, single_node_tree):
        t, node = single_node_tree
        assert (
                t.root_key == node.key
                and t.root_value == t[node.key] == node.value
                and node.key in t
                and t.is_leaf(key=node.key)
                and t.is_root(key=node.key)
                and t.level(key=node.key) == 1
                and t.parent(key=node.key) is EMPTY
                and t.children(key=node.key) == []
                and t.siblings(key=node.key) == []
                and t.ancestors(key=node.key) == []
                and t.path(key=node.key) == [node.value]
                and t.leaves() == [node.value]
                and len(t) == 1
                and list(t.inorder()) == [node.value]
                and list(t.postorder()) == [node.value]
                and list(t.preorder()) == [node.value]
                and list(t.levelorder()) == [node.value]
        )

    def test_multi_level_tree(self, multi_level_tree2):
        t, nodes = multi_level_tree2
        print()
        print('tree=', t)
        print('nodes=', [v.value for v in nodes])
        t.display()

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
