from unittest.mock import Mock, patch, call

from pytest import mark
from pyviews.core.xml import XmlAttr
from pyviews.pipes import call_set_attr

from tkviews import TtkStyle
from tkviews.rendering import ttk
from tkviews.core.common import TkRenderingContext
from tkviews.rendering.ttk import setup_value_setter, apply_style_attributes, configure


def increment(node, key, value):
    """Increments value"""
    call_set_attr(node, key, value + 1)


class SetupValueSetterTests:
    """setup_value_setter() tests"""

    @staticmethod
    def test_sets_name():
        """should set setter that sets node properties"""
        node = TtkStyle(Mock())
        name = 'some_name'

        setup_value_setter(node, TkRenderingContext())
        node.set_attr('name', name)

        assert node.name == name

    @staticmethod
    @mark.parametrize('values', [
        ({'key': 'value'}),
        ({'key': 'value', 'another_key': 1})
    ])
    def test_sets_values(values: dict):
        """should set setter that sets to "values" property"""
        node = TtkStyle(Mock())

        setup_value_setter(node, TkRenderingContext())
        for key, value in values.items():
            node.set_attr(key, value)

        assert node.values == values


@mark.parametrize('attrs, expected', [
    ([], {}),
    ([('one', '1', None)], {'one': '1'}),
    ([('one', '{1}', None)], {'one': 1}),
    ([('one', '{5}', __name__ + '.increment')], {'one': 6}),
    (
            [
                ('one', '{1 + 1}', None),
                ('two', '{1 + 1}', __name__ + '.increment'),
                ('key', ' string value ', None)
            ],
            {
                'one': 2,
                'two': 3,
                'key': ' string value '
            }
    )
])
def test_apply_style_attributes(attrs: list, expected: dict):
    """should set attribute values"""
    attrs = [XmlAttr(attr[0], attr[1], attr[2]) for attr in attrs]
    xml_node = Mock(attrs=attrs)
    node = TtkStyle(xml_node)
    setup_value_setter(node, TkRenderingContext())

    apply_style_attributes(node, TkRenderingContext())

    assert node.values == expected


@mark.parametrize('name, values', [
    ('name', {}),
    ('Button.Some', {'one': 1}),
    ('Label', {'one': 1, 'two': 'two'})
])
def test_configure_pass_values(name: str, values: dict):
    """configure should call configure on ttk style and pass values"""
    with patch(ttk.__name__ + '.Style') as ttk_style:
        configure_mock = Mock()
        ttk_style.return_value = Mock(configure=configure_mock)
        node = TtkStyle(Mock())
        node.values = values
        node.name = name

        configure(node, TkRenderingContext())

        assert configure_mock.call_args == call(node.full_name, **node.values)
