from collections import defaultdict, namedtuple
from typing import DefaultDict, Dict, List, Tuple

import pygtfs

from src.color import construct_constraint_graph, greedy_vertex_color
from src.db_loader import DB_FILENAME
from src.draw import draw


def construct_data() -> Tuple[List[List[int]], List[List[int]], List[int]]:
    """
    Create the stops_for_routes and route_for_stops lists from gtfs data.

    RAPTOR expects a "route" to only contain trips that all have the same
    stop sequence. This means we cannot reuse GTFS route objects, because
    they do not obey this constraint because they group both directions as a
    single route AND group trips with different stop sequences as part of
    same route.
    """
    schedule = pygtfs.Schedule(DB_FILENAME)

    # Map from GTFS stop_ids to the raptor int id.
    gtfs_stop_id_to_raptor = {s.stop_id: i for i, s in enumerate(schedule.stops)}

    trip_id_to_stop_ids: DefaultDict[str, List[str]] = defaultdict(lambda: [])
    for st in schedule.stop_times:
        trip_id_to_stop_ids[st.trip_id].append(st.stop_id)

    Route = namedtuple('Route', ['trip_id', 'stop_ids'])

    stop_seq_to_route: Dict[str, Route] = {}
    for trip_id, stop_ids in trip_id_to_stop_ids.items():
        stop_sequence = ''.join(stop_ids)
        if stop_sequence in stop_seq_to_route:
            continue
        stop_seq_to_route[stop_sequence] = Route(trip_id, stop_ids)

    print(f'Done grouping routes, found: {len(stop_seq_to_route)} routes')

    routes_for_stops: List[Set[int]] = [
        set() for _ in range(len(gtfs_stop_id_to_raptor))
    ]
    stops_for_routes: List[List[int]] = [
        [] for _ in range(len(stop_seq_to_route))
    ]
    raptor_id_to_short_name: List[int] = [
        i for i in range(len(stop_seq_to_route))
    ]
    for route_id, route in enumerate(stop_seq_to_route.values()):
        gtfs_route = schedule.routes_by_id(schedule.trips_by_id(route.trip_id)[0].route_id)[0]
        raptor_id_to_short_name[route_id] = gtfs_route.route_short_name

        for stop_id in route.stop_ids:
            raptor_stop = gtfs_stop_id_to_raptor[stop_id]
            routes_for_stops[raptor_stop].add(route_id)
            stops_for_routes[route_id].append(raptor_stop)

    return routes_for_stops, stops_for_routes, raptor_id_to_short_name


def generate_graph() -> None:
    """
    Load GTFS data from local sqlite storage and construct the constraint graph
    and coloring for the network. Output DOT graph visualizations for the network.
    """
    routes_for_stops, stops_for_routes, route_names = construct_data()
    print(f'Done constructing raptor data')

    graph = construct_constraint_graph(routes_for_stops, stops_for_routes)
    print(f'Done constructing constraint graph')

    coloring = greedy_vertex_color(graph)
    print(f'Done coloring graph')

    draw(
        graph=graph,
        colors=coloring,
        # Don't use GTFS route names because it will confuse casual users.
        route_names=None,
        filename_prefix='mta_',
        view=True,
    )


if __name__ == '__main__':
    generate_graph()
