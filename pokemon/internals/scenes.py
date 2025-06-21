from collections import namedtuple

Bounds = namedtuple('Bounds', ['min_x', 'min_y', 'max_x', 'max_y'])

BOUNDS = {
    'player-bedroom': Bounds(0, 0, 100, 100),
}
