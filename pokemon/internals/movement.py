from pokemon.database import User
from . import scenes

def move_compound(user: User | None, movements: list[tuple[int, int]]) -> None:
    if user is None:
        return

    pos_x, pos_y = user.pos_x, user.pos_y
    scene_bounds = scenes.BOUNDS[str(user.scene)]

    for dx, dy in movements:
        if pos_x + dx >= scene_bounds.min_x and pos_x + dx <= scene_bounds.max_x:
            pos_x += dx

        if pos_y + dy >= scene_bounds.min_y and pos_y + dy <= scene_bounds.max_y:
            pos_y += dy

    User.update(pos_x=pos_x, pos_y=pos_y).where(User.id == user.id).execute()

