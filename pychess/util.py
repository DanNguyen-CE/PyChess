from .constants import *

def pixel_to_grid(x, y, normalize=False):
    """Floor pixel position to grid. Offsets so grid lines up with board.
       If normalize=True, normalize the result for grid indexing.
    """
    new_x = (x-CURSOR_OFFSET_X) // SQUARE_SIZE + GRID_OFFSET_X
    new_y = (y-CURSOR_OFFSET_Y) // SQUARE_SIZE + GRID_OFFSET_Y

    if normalize:
        new_x, new_y, = round(new_x - NORMALIZE_X), round(new_y - NORMALIZE_Y)
    
    return new_x, new_y

def valid_range(x, y):
    """If coordinates are within standard chess board dimensions (0,0) to (7,7)."""
    if x >= 0 and y >= 0 and x <= 7 and y <= 7:
        return True
    else:
        return False

def play_sound(player, source, volume):
    """Plays audio source immediately. Will cancel currently playing audio."""
    player.next_source()
    player.queue(source)
    player.volume = volume
    player.play()