import sys

import pygtfs

DB_FILENAME = 'gtfs/gtfs_db'


def initialize_schedule(filename=':memory') -> pygtfs.Schedule:
    return pygtfs.Schedule(filename)


def load_gtfs_feed(schedule: pygtfs.Schedule, filename: str) -> None:
    pygtfs.append_feed(schedule, input_filename)


if __name__ == '__main__':
    input_filename = sys.argv[1]
    if input_filename.split('.')[-1] != 'zip':
        print('Invalid input file, GTFS feed must be provided in zip format')
        exit(1)

    schedule = initialize_schedule(DB_FILENAME)
    load_gtfs_feed(schedule, input_filename)
    print(f'Loaded {len(schedule.agencies)} agencies')
    print(f'Loaded {len(schedule.stops)} stops')
