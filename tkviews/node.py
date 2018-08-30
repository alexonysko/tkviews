'''Tkinter widgets nodes'''

from tkinter import Tk
from pyviews import NodeSetup
from pyviews.core.xml import XmlAttr
from pyviews.core.ioc import inject
from pyviews.core.xml import XmlNode
from pyviews.core.node import InstanceNode, Property
from pyviews.rendering.flow import apply_attributes, render_children, apply_attribute
from tkviews.geometry import Geometry

# def get_args(self, inst_type=None):
#     if issubclass(inst_type, Widget):
#         return RenderArgs.Result([self['master']], {})
#     return super().get_args(inst_type)

class Root(InstanceNode):
    '''Wrapper under tkinter Root'''
    def __init__(self, xml_node: XmlNode):
        super().__init__(Tk(), xml_node)
        self._icon = None

    @property
    def state(self):
        '''Widget state'''
        return self.widget.state()

    @state.setter
    def state(self, state):
        self.widget.state(state)

    @property
    def icon(self):
        '''Icon path'''
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value
        self.widget.iconbitmap(default=value)

def get_root_setup():
    '''Returns setup for root'''
    node_setup = NodeSetup(setter=_widget_node_setter, on_destroy=_on_widget_destroy)
    node_setup.render_steps = [
        apply_attributes,
        render_children
    ]
    node_setup.get_child_args = _get_child_args
    return node_setup

def get_widget_setup():
    '''Returns setup for widget'''
    node_setup = NodeSetup()
    node_setup.render_steps = [
        apply_attributes,
        render_children
    ]
    node_setup.setter = _widget_node_setter
    node_setup.properties = {
        'geometry': Property('geometry', _geometry_setter),
        'style': Property('style', _style_setter)
    }
    node_setup.get_child_args = _get_child_args
    node_setup.on_destroy = _on_widget_destroy

def apply_text(node: InstanceNode):
    '''Applies xml node content to WidgetNode'''
    if node.xml_node.text is None or not node.xml_node.text.strip():
        return
    text_attr = XmlAttr('text', node.xml_node.text)
    apply_attribute(node, text_attr)

def _widget_node_setter(node: InstanceNode, key: str, value):
    '''Applies passed attribute'''
    if hasattr(node, key):
        setattr(node, key, value)
    elif hasattr(node.widget, key):
        setattr(node.widget, key, value)
    else:
        node.instance.configure(**{key:value})

def _geometry_setter(node: InstanceNode, geometry: Geometry, previous: Geometry):
    if previous:
        previous.forget()
    if geometry is not None:
        geometry.apply(node.instance)
    return geometry

@inject('apply_styles')
def _style_setter(node: InstanceNode, styles: str, apply_styles=None):
    apply_styles(node, styles)
    return styles

def _get_child_args(node: InstanceNode):
    return {'parent_node': node, 'master': node.instance}

def _on_widget_destroy(node: InstanceNode):
    node.instance.destroy()
