"""
Given a limited set of RAPTOR data structures, provide a vertex coloring
for the network. Here each Route is a vertex and an edge to another Route
exists iff both Routes share a stop.

The output should be a color for each Route.

The test network is defined as follow:

    route_1        3
                   |
    route_0   0 -- 1    2
                   |    |
                   4    5 - 7  route_3
                        |
    route_2             6

The list at index i indicates which routes touch stop_i.
Therefore len(routes_for_stops) == # stops.
    routes_for_stops: [[0], [0, 1], [2], [1], [1], [2, 3], [2], [3]]

The list at index i indicates which stops are on route_i.
Therefore len(stops_for_routes) == # routes.
    stops_for_routes: [[0, 1], [3, 1, 4], [2, 5, 6], [5, 7]]

Which routes share stops?
    route_0 and route_1
    route_2 and route_3

So a possible accurate coloring would be:
    route_colors: [0, 1, 0, 1]

The example happens to be bipartite and the example coloring is chromatic,
but the input need not be and this algorithm will still handle it correctly.
"""
import unittest
from typing import List, Set

ConstraintGraph = List[Set[int]]


def construct_constraint_graph(
    routes_for_stops: List[int],
    stops_for_routes: List[int],
) -> ConstraintGraph:
    """
    Return an undirected graph where each vertex is a route and each edge
    between v1/v2 indicates that v1/v2 share at least one stop.
    """
    constraint_graph = [set() for _ in range(len(stops_for_routes))]
    visited_stop = [False for _ in range(len(routes_for_stops))]

    for route_id, stops_for_route in enumerate(stops_for_routes):
        for stop in stops_for_route:
            if visited_stop[stop]:
                continue
            for other_route_id in routes_for_stops[stop]:
                if other_route_id == route_id:
                    continue
                constraint_graph[other_route_id].add(route_id)
                constraint_graph[route_id].add(other_route_id)
            visited_stop[stop] = True

    return constraint_graph


def get_ordering(graph: ConstraintGraph) -> List[int]:
    """
    Provide an order to traverse route_ids in the ConstraintGraph that
    hopefully provides more optimal greedy coloring. For now, sort
    by number of outgoing edges.
    """
    order = [(i, len(edges)) for i, edges in enumerate(graph)]
    # Decreasing sort by number of neighbors/edges.
    order.sort(key=lambda x: -x[1])
    return [route_id for route_id, _ in order]


def greedy_vertex_color(graph: ConstraintGraph) -> List[int]:
    """
    Return a list of ints indicating the 'color' of each vertex
    in the input ConstraintGraph. Neighboring vertices in the
    ConstraintGraph should never be colored the same.

    Because greedy coloring is used, the output coloring is not
    guaranteed to be optimal/chromatic.
    """
    order = get_ordering(graph)

    coloring = [-1 for _ in range(len(graph))]

    # See http://fileadmin.cs.lth.se/cs/Personal/Andrzej_Lingas/k-m.pdf,
    # Section 1.2.2, "Heuristic methods [...]".
    for route_id in order:
        neighbor_colors = {coloring[neighbor] for neighbor in graph[route_id]}

        # Find a color which doesn't conflict with any neighbors' colors.
        # When none/some of the neighbors haven't been colored then there will
        # be -1 values in neighbor_colors, which is not a problem.
        color = 0
        while True:
            if color not in neighbor_colors:
                break
            color += 1
        coloring[route_id] = color

    return coloring


class TestSolutions(unittest.TestCase):
    def setUp(self):
        self.routes_for_stops = [[0], [0, 1], [2], [1], [1], [2, 3], [2], [3]]
        self.stops_for_routes = [[0, 1], [3, 1, 4], [2, 5, 6], [5, 7]]

    def test_constraint_graph(self):
        constraint_graph = construct_constraint_graph(
            self.routes_for_stops,
            self.stops_for_routes,
        )

        # There must be one set for each route/vertex.
        self.assertTrue(len(constraint_graph) == len(self.stops_for_routes))

        # As described in module docstring.
        self.assertTrue(constraint_graph[0] == {1})
        self.assertTrue(constraint_graph[1] == {0})
        self.assertTrue(constraint_graph[2] == {3})
        self.assertTrue(constraint_graph[3] == {2})

    def test_coloring(self):
        constraint_graph = construct_constraint_graph(
            self.routes_for_stops,
            self.stops_for_routes,
        )
        coloring = greedy_vertex_color(constraint_graph)

        # There must be one color for each route/vertex.
        self.assertTrue(len(coloring) == len(self.stops_for_routes))

        # As described above, neighbors should be different colors.
        self.assertTrue(coloring[0] != coloring[1])
        self.assertTrue(coloring[2] != coloring[3])

if __name__ == '__main__':
    unittest.main()
