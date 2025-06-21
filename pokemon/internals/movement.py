import math

from pokemon.database import Direction, User
from . import scenes

MOVEMENT_MAP: dict[str, tuple[int, int]] = {
    'w': (0, -1),
    's': (0, 1),
    'a': (-1, 0),
    'd': (1, 0),
}

REVERSED_MOVEMENT_MAP: dict[tuple[int, int], str] = {
    (0, -1): 'back',
    (0, 1): 'front',
    (-1, 0): 'left',
    (1, 0): 'right',
}

def as_movement_tuple(movement: str) -> tuple[int, int]:
    return MOVEMENT_MAP.get(movement, (0, 0))


def move_compound(user: User | None, movements: list[tuple[int, int]]) -> tuple[int, int, Direction] | None:
    if user is None:
        return

    pos_x, pos_y = user.pos_x, user.pos_y
    scene_bounds = scenes.BOUNDS[str(user.scene)]

    for dx, dy in movements:
        if pos_x + dx >= scene_bounds.min_x and pos_x + dx <= scene_bounds.max_x:
            pos_x += dx
        else:
            pos_x += max(min(dx, scene_bounds.max_x - pos_x), scene_bounds.min_x - pos_x)

        if pos_y + dy >= scene_bounds.min_y and pos_y + dy <= scene_bounds.max_y:
            pos_y += dy
        else:
            pos_y += max(min(dy, scene_bounds.max_y - pos_y), scene_bounds.min_y - pos_y)

    last_movement_magnitude = int(math.copysign(1, movements[-1][0])) if movements[-1][0] else 0, int(math.copysign(1, movements[-1][1])) if movements[-1][1] else 0

    direction = Direction(REVERSED_MOVEMENT_MAP.get(last_movement_magnitude, 'front'))

    User.update(pos_x=pos_x, pos_y=pos_y, direction=direction).where(User.id == user.id).execute()

    return pos_x, pos_y, direction  # pyright: ignore

