from pokemon.database import User
from . import scenes

MOVEMENT_MAP: dict[str, tuple[int, int]] = {
    'w': (0, -1),
    's': (0, 1),
    'a': (-1, 0),
    'd': (1, 0),
}

def as_movement_tuple(movement: str) -> tuple[int, int]:
    return MOVEMENT_MAP.get(movement, (0, 0))


def move_compound(user: User | None, movements: list[tuple[int, int]]) -> None:
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

    User.update(pos_x=pos_x, pos_y=pos_y).where(User.id == user.id).execute()

