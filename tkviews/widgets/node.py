"""Tkinter widgets nodes"""

from tkinter import Tk, Widget

from pyviews.core import XmlNode, InstanceNode, InheritedDict, XmlAttr
from pyviews.pipes import apply_attributes, render_children, apply_attribute
from pyviews.rendering import RenderingPipeline, get_type, create_instance

from tkviews.core import TkNode, TkRenderingContext


class Root(InstanceNode, TkNode):
    """Wrapper under tkinter Root"""

    def __init__(self, xml_node: XmlNode):
        super().__init__(Tk(), xml_node)
        self._icon = None
        self._node_styles = InheritedDict()

    @property
    def node_styles(self) -> InheritedDict:
        """Returns node styles set"""
        return self._node_styles

    @property
    def state(self):
        """Widget state"""
        return self.instance.state()

    @state.setter
    def state(self, state):
        self.instance.state(state)

    @property
    def icon(self):
        """Icon path"""
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value
        self.instance.iconbitmap(default=value)

    def bind(self, event, command):
        """Calls widget bind"""
        self.instance.bind(event, command)

    def bind_all(self, event, command):
        """Calls widget bind"""
        self.instance.bind_all(event, command)


def get_root_setup() -> RenderingPipeline:
    """Returns setup for root"""
    return RenderingPipeline(pipes=[
        setup_widget_setter,
        setup_widget_destroy,
        apply_attributes,
        render_widget_children
    ])


class WidgetNode(InstanceNode, TkNode):
    """Wrapper under tkinter widget"""

    def __init__(self, widget: Widget, xml_node: XmlNode,
                 node_globals: InheritedDict = None, node_styles: InheritedDict = None):
        super().__init__(widget, xml_node, node_globals=node_globals)
        self._node_styles = InheritedDict(node_styles)

    @property
    def node_styles(self) -> InheritedDict:
        """Returns node styles set"""
        return self._node_styles

    def bind(self, event, command):
        """Calls widget bind"""
        self.instance.bind(event, command)

    def bind_all(self, event, command):
        """Calls widget bind"""
        self.instance.bind_all(event, command)


def get_widget_setup():
    """Returns setup for widget"""
    return RenderingPipeline([
        setup_widget_setter,
        setup_widget_destroy,
        apply_attributes,
        apply_text,
        render_widget_children
    ], create_node=_create_widget_node)


def setup_widget_setter(node: WidgetNode, _: TkRenderingContext):
    """Sets up setter"""
    node.attr_setter = _widget_node_setter


def _widget_node_setter(node: WidgetNode, key: str, value):
    """Applies passed attribute"""
    if hasattr(node, key):
        setattr(node, key, value)
    elif hasattr(node.instance, key):
        setattr(node.instance, key, value)
    else:
        node.instance.configure(**{key: value})


def setup_widget_destroy(node: WidgetNode, _: TkRenderingContext):
    """Sets up on destroy method"""
    node.on_destroy = _on_widget_destroy


def _on_widget_destroy(node: WidgetNode):
    node.instance.destroy()


def render_widget_children(node: WidgetNode, context: TkRenderingContext):
    render_children(node, context, _get_child_context)


def _get_child_context(xml_node: XmlNode, node: WidgetNode, _: TkRenderingContext):
    """Renders child widgets"""
    child_context = TkRenderingContext()
    child_context.xml_node = xml_node
    child_context.parent_node = node
    child_context.master = node.instance
    child_context.node_globals = InheritedDict(node.node_globals)
    child_context.node_styles = InheritedDict(node.node_styles)
    return child_context


def _create_widget_node(context: TkRenderingContext):
    inst_type = get_type(context.xml_node)
    inst = create_instance(inst_type, context)
    return create_instance(WidgetNode, {'widget': inst, **context})


def apply_text(node: WidgetNode, _: TkRenderingContext):
    """Applies xml node content to WidgetNode"""
    if node.xml_node.text is None or not node.xml_node.text.strip():
        return
    text_attr = XmlAttr('text', node.xml_node.text)
    apply_attribute(node, text_attr)
