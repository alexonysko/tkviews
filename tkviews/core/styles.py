'''Nodes for storing config options for widgets'''

from typing import Any, Callable
from pyviews.core.xml import XmlNode
from pyviews.core import CoreError
from pyviews.core.node import Node
from pyviews.core.observable import InheritedDict

class StyleItem:
    '''Wrapper under option'''
    def __init__(self, setter: Callable[[Node, str, Any], None], name: str, value: Any):
        self._setter = setter
        self._name = name
        self._value = value

    @property
    def setter(self):
        '''Returns setter'''
        return self._setter

    @property
    def name(self):
        '''Returns name'''
        return self._name

    @property
    def value(self):
        '''Returns value'''
        return self._value

    def apply(self, node: Node):
        '''Applies option to passed node'''
        self._setter(node, self._name, self._value)

    def __hash__(self):
        return hash((self._name, self._setter))

    def __eq__(self, other):
        return hash(self) == hash(other)

class Style(Node):
    '''Node for storing config options'''
    def __init__(self, xml_node: XmlNode, node_globals: InheritedDict = None):
        super().__init__(xml_node, node_globals)
        self.name = None
        self.items = {}

    def destroy(self):
        '''Removes self from styles'''
        self._destroy_bindings()

class StyleError(CoreError):
    '''Error for style'''
    pass
