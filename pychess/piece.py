from .constants import *
import pyglet

class Piece():
    def __init__(self, x, y, index, image, batch, group):
        self.index = index

        self.sprite = pyglet.sprite.Sprite(
            image,
            x*SQUARE_SIZE + BOARD_OFFSET_X,
            y*SQUARE_SIZE + BOARD_OFFSET_Y,
            batch=batch, group=group
        )

        self.type = abs(index)
        self.is_white = True if index > 0 else False

    def on_release(self, collision):
        if (collision == 0):
            None

        # No Friendly Fire
        if (self.type * collision > 0):
            return


    def Pawn(self):
        return None