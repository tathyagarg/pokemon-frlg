import os

from PIL import Image

from pokemon.database import Direction

TILE_SIZE = 16
SCALE_FACTOR = 5

SCREN_TILES_X = 15
SCREN_TILES_Y = 10

def make_scene_image(scene: str, pos_x: int, pos_y: int, direction: Direction) -> str:
    os.makedirs('tmp', exist_ok=True)

    fname = f'tmp/{scene}_{pos_x}_{pos_y}_{direction.value}.png'

    if os.path.exists(fname):
        return fname

    scene_image_path = f'assets/rooms/{scene}.png'

    with Image.open(scene_image_path) as room:
        player_sprite_path = f'assets/player/male/{direction.value}.png'

        with Image.open(player_sprite_path) as player_sprite:
            room.paste(player_sprite, (pos_x * TILE_SIZE * SCALE_FACTOR, pos_y * TILE_SIZE * SCALE_FACTOR), player_sprite)

        player_screen_x = pos_x * TILE_SIZE * SCALE_FACTOR + (TILE_SIZE * SCALE_FACTOR // 2)
        player_screen_y = pos_y * TILE_SIZE * SCALE_FACTOR + 3 * (TILE_SIZE * SCALE_FACTOR // 2)

        paste_x = (SCREN_TILES_X * TILE_SIZE * SCALE_FACTOR) // 2 - player_screen_x
        paste_y = (SCREN_TILES_Y * TILE_SIZE * SCALE_FACTOR) // 2 - player_screen_y

        with Image.new('RGB', (SCREN_TILES_X * TILE_SIZE * SCALE_FACTOR, SCREN_TILES_Y * TILE_SIZE * SCALE_FACTOR), (0, 0, 0)) as background:
            background.paste(room, (paste_x, paste_y))
            background.save(fname)

    return fname

def get_image_size(image_path: str) -> int:
    if not os.path.exists(image_path):
        return 0

    return os.path.getsize(image_path)
