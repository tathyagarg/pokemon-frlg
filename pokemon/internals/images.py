import os

from PIL import Image

from pokemon.database import Direction

def make_scene_image(scene: str, pos_x: int, pos_y: int, direction: Direction) -> str:
    os.makedirs('tmp', exist_ok=True)

    fname = f'tmp/{scene}_{pos_x}_{pos_y}_{direction.value}.png'

    if os.path.exists(fname):
        return fname

    scene_image_path = f'assets/rooms/{scene}.png'

    with Image.open(scene_image_path) as room:
        player_sprite_path = f'assets/player/male/{direction.value}.png'

        with Image.open(player_sprite_path) as player_sprite:
            print("Pasting at position:", pos_x, pos_y, 'with real coords: ', (pos_x * 16 * 5, pos_y * 16 * 5))
            room.paste(player_sprite, (pos_x * 16 * 5, pos_y * 16 * 5), player_sprite)

        room.save(fname)

    return fname

def get_image_size(image_path: str) -> int:
    if not os.path.exists(image_path):
        return 0

    return os.path.getsize(image_path)
