from collections import namedtuple

Bounds = namedtuple('Bounds', ['min_x', 'min_y', 'max_x', 'max_y'])

BOUNDS = {
    'start': Bounds(0, 0, 100, 100),
}
