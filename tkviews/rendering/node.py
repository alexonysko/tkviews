# """Node creation"""
#
# from tkinter import Entry, Checkbutton, Radiobutton
# from tkinter.ttk import Widget as TtkWidget
# from typing import Any
#
# from pyviews.core import Node, XmlNode
# from pyviews.rendering import get_type, create_instance
#
# from tkviews.ttk import TtkWidgetNode
# from tkviews.widgets import WidgetNode, EntryNode, CheckbuttonNode, RadiobuttonNode
# from tkviews.core.common import TkRenderingContext
#
#
# def create_widget_node(xml_node: XmlNode, context: TkRenderingContext) -> WidgetNode:
#     """Creates node from xml node using namespace as module and tag name as class name"""
#     inst_type = get_type(xml_node)
#     context['xml_node'] = xml_node
#     inst = create_instance(inst_type, context)
#     if not isinstance(inst, Node):
#         inst = _convert_to_node(inst, context)
#     return inst
#
#
# def _convert_to_node(inst: Any, context: TkRenderingContext) -> WidgetNode:
#     context['widget'] = inst
#     node_class = WidgetNode
#     if isinstance(inst, Entry):
#         node_class = EntryNode
#     elif isinstance(inst, Checkbutton):
#         node_class = CheckbuttonNode
#     elif isinstance(inst, Radiobutton):
#         node_class = RadiobuttonNode
#     elif isinstance(inst, TtkWidget):
#         node_class = TtkWidgetNode
#     return create_instance(node_class, context)
