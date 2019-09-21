# forestry/trees.py
#
# forestry: Python Tree data structures and tools
#
# Copyright (C) 2019  by Dwight D. Cummings
#
# This module is part of `forestry` and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php
"""Provides A Tree class definition"""

# Standard library imports
from collections import defaultdict, deque
from typing import (
    Any, NamedTuple, Optional, Dict, Union, Iterable, Tuple, Callable
)

# Third-party module imports
# Local application module imports

# Global variables
EMPTY = object()


# Classes
class _Node(NamedTuple):
    """Encapsulates Tree node data.

    An internal helper class supporting Tree class definition
    """
    value: Any  # The data stored at the node
    parent: Union[str, object] = EMPTY  # The key (tag, label) of parent


class Tree:
    """Used to create and query Tree data structures.

    Trees are hierarchical collections of nodes. Trees
    are build starting from a root node. Each node stores
    arbitrary data, its "value", and a label, name
    or node identifier, called a "tag".

    Values in the tree can be accessed by looking up the
    nodes' tags.

    Examples:
        >>> t = Tree(value=1, tag='a')
        >>> assert t['a'] == 1
        >>> t.add(value=2, tag='b')  # Adds a child to the root node by default
        >>> assert t['b'] == 2
        >>> t.add(value=3, tag='c')  # Add a child to the root node
        >>> t('b')
        <Tree; value=1; tag='b'>
        >>> t('c').parent == 1
        >>> t('a').children == [1, 2]
        >>> t('b').add(value=4, tag='d')  # Add a child node to node (sub-tree) at 'b'
        >>> assert t('d').ancestors == [2, 1]
        >>> assert t('d').path == [1, 2, 4]  # Traverse from root to node

    t.preorder() t.inorder() t.postorder() return iterables over the node values

    Attributes:
        _root (str): tag of root node
        _nodes (Dict[str, _Node]): Mapping from node tags to node data
        _children (defaultdict): Mapping from node tags to children
    """

    version = '0.1'  # Version number of class

    def __init__(self, key: Optional[str] = None,
                 value: Any = EMPTY) -> None:
        """This method initializes instance variables.

        Args:
            value (Any): The data value stored at the node.
            key (Union[str, object]): tag or name of the node
        """
        self._children = defaultdict(list)
        self._nodes = {} if value is EMPTY else {key: _Node(value)}
        self.root_key = key

    def __contains__(self, item) -> bool:
        return item in self._nodes

    def __getitem__(self, item) -> Any:
        return self._nodes[item].value

    def __len__(self):
        return len(self._nodes)

    @property
    def root_value(self) -> Union[Any, object]:
        """Return the value stored at root"""
        return self._nodes.get(self.root_key, EMPTY)

    def ancestors(self, key: str, reverse: bool = False) -> list:
        """Returns a list of parent and recursive parents.

        Args:
            key (str): the key whose ancestors are returned
            reverse (bool): build ancestry from the root down
        """
        self.verify_key_in(key)
        deq = deque()
        current_key = key
        while not self.is_root(current_key):
            current_key = self._nodes[current_key].parent
            add_to_deq = deq.appendleft if reverse else deq.append
            add_to_deq(self[current_key])

        return list(deq)

    def append(self, key: str, value: Any, parent: str = None):
        """Adds a child node to the root node.

        Args:
            key (str): tag or name of the node
            value (Any): The data value stored at the node.
            parent (str): The parent to append the child to
        """
        parent = parent or self.root_key
        self.verify_key_out(key)
        self._nodes[key] = _Node(value, parent)
        self._children[self.root_key].append(key)

    def children(self, key: str):
        """Return the list of child nodes."""
        self.verify_key_in(key)
        return [self[child_key] for child_key in self._children[key]]

    def extend(self, children: Iterable[Tuple[str, Any]],
               parent: str = None):
        """Adds a child node to the root node.

        Args:
            children (Iterable[Tuple[str, Any]]): Iterable of key-value pairs
            parent (str): The parent to append the children to
        """
        for key, value in children:
            self.append(key, value, parent)

    def is_empty(self):
        """True if tree is empty, else false."""
        return self.root_value is EMPTY

    def is_root(self, key: str):
        """Returns true if given key is root_key"""
        self.verify_key_in(key)
        return key == self.root_key

    def leaves(self):
        """Return values of those nodes that have no children."""
        return [
            self[key] for key in self._nodes
            if self._children[key] == []
        ]

    leafs = leaves

    def parent(self, key: str):
        """Return the value of the parent node"""
        parent_key = self._nodes[key].parent
        return self._nodes[parent_key].value

    def path(self, key: str) -> list:
        """Returns a ancestry from root to not at `key` including
        the give node.

        Args:
            key (str): the key whose ancestors are returned
        """
        # The call to `ancestors` check for key errors.
        return self.ancestors(key, reverse=True) + [self[key]]

    def preorder(self, start_key: str = None):
        """Visits each node in "preorder" and call the visit
        function.

        Args:
            start_key (str): the key of the node to start the traversal
        """
        start_key = start_key or self.root_key
        if start_key in self:
            yield self[start_key]
            for child in self._children[start_key]:
                self.preorder(start_key=child)

    def postorder(self, start_key=None):
        """Visits each node in "postorder" and call the visit
        function.

        Args:
            visitor (Callable): function called on the visted nodes
            start_key (str): the key of the node to start the traversal
        """
        start_key = start_key or self.root_key
        if start_key in self:
            for child in self._children[start_key]:
                self.postorder(start_key=child)
            yield self[start_key]

    def inorder(self, start_key=None):
        """Visits each node in "inorder" and call the visit
        function.

        Args:
            start_key (str): the key of the node to start the traversal
        """
        start_key = start_key or self.root_key
        if start_key in self:
            first = self._children[start_key][0:1]
            rest = self._children[start_key][1:]
            if first:
                self.inorder(start_key=first[0])

            yield self[start_key]
            for child in rest:
                self.inorder(start_key=child)

    def levelorder(self, start_key=None):
        """Visits each node in "levelorder" and call the visit
        function.

        Args:
            start_key (str): the key of the node to start the traversal
        """
        start_key = start_key or self.root_key
        if start_key in self:
            deq = deque([start_key])
            while deq:
                key = deq.popleft()
                yield self[key]
                deq.extend(self._children[key])

    def verify_key_in(self, key: str) -> None:
        """Raise KeyError if key missing.
        Args:
            key (str): the key to verify
        """
        if key not in self:
            raise KeyError(f'Key "{key}" already added')

    def verify_key_out(self, key: str) -> None:
        """Raise KeyError if key present.
        Args:
            key (str): the key to verify
        """

        if key in self:
            raise KeyError(f'Key "{key}" already added')

    def demo(self, ):
        """This method performs .

        Class methods are similar to regular functions.

        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            param1: The first parameter.
            param2: The second parameter.

        Returns:
            True if successful, False otherwise.

        """


class _SubTree(NamedTuple):
    root_key: str
    tree: Tree
# Module level functions
