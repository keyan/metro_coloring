import unittest

from src.color import construct_constraint_graph, greedy_vertex_color
from src.draw import draw, int_to_rgb


class TestColoring(unittest.TestCase):
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


class TestDraw(unittest.TestCase):
    def setUp(self):
        self.routes_for_stops = [[0], [0, 1], [2], [1], [1], [2, 3], [2], [3]]
        self.stops_for_routes = [[0, 1], [3, 1, 4], [2, 5, 6], [5, 7]]

    def test_int_to_rgb(self):
        res1 = int_to_rgb(1)
        res2 = int_to_rgb(2)

        self.assertTrue(isinstance(res1, str))
        self.assertTrue(res1 != res2)

    def test_draw(self):
        constraint_graph = construct_constraint_graph(
            self.routes_for_stops,
            self.stops_for_routes,
        )
        coloring = greedy_vertex_color(constraint_graph)
        nodes = draw(constraint_graph, coloring)

        self.assertEqual(4, nodes)


if __name__ == '__main__':
    unittest.main()
