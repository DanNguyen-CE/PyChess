from pychess import *

def init():
    """ Create Window & Initalize Board & Pieces """
    # Create Window
    window = pyglet.window.Window(WINDOW_SIZE, WINDOW_SIZE, NAME)
    window.set_icon(icon)
    pyglet.gl.glClearColor(44 /255, 52 /255, 66 /255, 1) # Window BG Color

    logo = pyglet.sprite.Sprite(resources.logo, WINDOW_SIZE / 2, WINDOW_SIZE / 2 - 220)

    # Definte batches
    board_batch = pyglet.graphics.Batch()
    pieces_batch = pyglet.graphics.Batch()
    

    board_back = pyglet.shapes.BorderedRectangle( # Create board background
        WINDOW_SIZE//2 -5,
        WINDOW_SIZE//2 +59,
        SQUARE_SIZE*8 +10,
        SQUARE_SIZE*8 +10,
        BORDER_SIZE,
        BOARD_ALT_COLOR,
        BORDER_COLOR,
        board_batch)
    board_back.anchor_position = SQUARE_SIZE * 4, SQUARE_SIZE * 4

    board_squares = [ # Create board alt squares
        pyglet.shapes.Rectangle(
            x*SQUARE_SIZE + BOARD_OFFSET_X, (y * 2 + x % 2)*SQUARE_SIZE + BOARD_OFFSET_Y,
            SQUARE_SIZE, SQUARE_SIZE,
            color=BOARD_COLOR,
            batch=board_batch)
        
        for y in range(4)
        for x in range(8)
    ]

    for square in board_squares: # Center square anchors
        square.anchor_position = SQUARE_SIZE / 2, SQUARE_SIZE / 2

    spritedt = numpy.dtype(pyglet.sprite.Sprite)
    pieces = numpy.empty((8, 8), dtype=spritedt) # Array stores Sprite instances

    def create_piece(piece, pos_x, pos_y): # Add sprite pieces to board
        sprite = get_piece_sprite(piece)
        if sprite:
            pieces[pos_y, pos_x] = pyglet.sprite.Sprite(
                                    sprite,
                                    pos_x*SQUARE_SIZE + BOARD_OFFSET_X,
                                    pos_y*SQUARE_SIZE + BOARD_OFFSET_Y,
                                    batch=pieces_batch)

    for i in range(8):
        for j in range(8):
            create_piece(init_board_state[i][j], j, i)

    @window.event
    def on_draw():
        window.clear()
        board_batch.draw()
        pieces_batch.draw()
        logo.draw()

    pyglet.app.run()

def main():
    init()

if __name__ == "__main__":
    main()