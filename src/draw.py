import hashlib
from typing import List

from graphviz import Graph

from src.color import ConstraintGraph


def int_to_rgb(value: int) -> str:
    """
    Given an int value, return a RGB hex string for a unique color.

    This simplifies the colored graph drawing procedure by avoiding
    having to keep a finite hardcoded list of colors.
    """
    # Get a deterministic hash of value, so that small differences in
    # the input `value` create large hex color differences.
    hashed_val = hashlib.md5(value.to_bytes(8, byteorder='big', signed=True))
    value = int(hashed_val.hexdigest(), 16)

    r = 0xff - (value % 0xce)
    g = 0xff - (value % 0xdd)
    b = 0xff - (value % 0xec)

    return '#%02x%02x%02x' % (r, g, b)


def draw(graph: ConstraintGraph, colors: List[int], view=True) -> None:
    """
    Given a ConstraintGraph, construct two DOT graph visualizations
    of the ConstraintGraph, one which includes coloring and one which
    does not. These are both saves as pngs to /output.
    """
    uncolored = Graph(comment='uncolored', format='png')
    colored = Graph(comment='colored', format='png')

    for route_id, edges in enumerate(graph):
        name = f'route_{route_id}'
        str_route_id = str(route_id)

        uncolored.node(str_route_id, name)
        colored.node(
            str_route_id,
            name,
            color=int_to_rgb(colors[route_id]),
            penwidth="3",
        )

        uncolored.edges([(str_route_id, str(edge_route_id)) for edge_route_id in edges])
        colored.edges([(str_route_id, str(edge_route_id)) for edge_route_id in edges])

    uncolored.render('output/uncolored.gv', view=view)
    colored.render('output/colored.gv', view=view)
