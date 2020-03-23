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


def draw(
    graph: ConstraintGraph,
    colors: List[int],
    route_names: List[int] = None,
    filename_prefix: str = '',
    view: bool = True,
) -> None:
    """
    Given a ConstraintGraph, construct two DOT graph visualizations
    of the ConstraintGraph, one which includes coloring and one which
    does not. These are both saves as pngs to /output.
    """
    uncolored = Graph(comment='colored', format='png', graph_attr={'rankdir': 'LR'})
    colored = Graph(comment='colored', format='png', graph_attr={'rankdir': 'LR'})

    for route_id, edges in enumerate(graph):
        node_label = str(route_id)

        # If a GTFS route name mapping is provided use it to make the visualization nice.
        if route_names is not None:
            name = route_names[route_id]
        else:
            name = f'route_{route_id}'

        uncolored.node(node_label, name)

        color = int_to_rgb(colors[route_id])
        colored.node(
            node_label,
            name,
            color=color,
            fillcolor=color,
            style='filled',
            penwidth="3",
        )

        uncolored.edges([(node_label, str(edge_route_id)) for edge_route_id in edges])
        colored.edges([(node_label, str(edge_route_id)) for edge_route_id in edges])

    uncolored.render(f'output/{filename_prefix}uncolored.gv', view=view)
    colored.render(f'output/{filename_prefix}colored.gv', view=view)
