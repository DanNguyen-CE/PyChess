from pychess import *
from random import randrange

def init():
    """ Create Window & Initalize Board & Pieces """
    # Create Window
    window = pyglet.window.Window(WINDOW_SIZE, WINDOW_SIZE, NAME)
    window.set_icon(icon)
    pyglet.gl.glClearColor(44 /255, 52 /255, 66 /255, 1) # Window BG Color

    # Definte batches
    board_batch = pyglet.graphics.Batch()
    pieces_batch = pyglet.graphics.Batch()
    screen_batch = pyglet.graphics.Batch()
    menu_batch = pyglet.graphics.Batch()

    # Create Start Screen Menu Items
    start_menu = [
        pyglet.shapes.Rectangle(WINDOW_SIZE/2, WINDOW_SIZE /2, WINDOW_SIZE, WINDOW_SIZE, BG_COLOR, batch=screen_batch), # BG
        pyglet.sprite.Sprite(resources.logo_large, WINDOW_SIZE / 2, WINDOW_SIZE / 2 + 200, batch=menu_batch), # Logo
        pyglet.text.Label( # Start Label
            '> Click anywhere to play! <', 
            font_name='Minecraft', font_size=20,
            x=WINDOW_SIZE/2, y=WINDOW_SIZE/2,
            anchor_x='center', anchor_y='center',
            batch=menu_batch),
        pyglet.text.Label( # Author Label
            'A simple chess application created by Daniel Nguyen (2021).\nPowered by Pyglet.',
            font_name='Minecraft', font_size=10,
            x=WINDOW_SIZE/2, y=WINDOW_SIZE/2 - 250,
            anchor_x='center', anchor_y='center',
            align='center', multiline=True, width = 500,
            batch=menu_batch)
    ]

    start_menu[0].anchor_position = start_menu[0].width/2, start_menu[0].height/2 # BG Anchor

    # Create Board
    logo = pyglet.sprite.Sprite(resources.logo, WINDOW_SIZE / 2, WINDOW_SIZE / 2 - 220, batch=board_batch)
    board_back = pyglet.shapes.BorderedRectangle( 
        WINDOW_SIZE//2,
        WINDOW_SIZE//2 +65,
        SQUARE_SIZE*8 +10,
        SQUARE_SIZE*8 +10,
        BORDER_SIZE,
        BOARD_ALT_COLOR,
        BORDER_COLOR,
        board_batch)
    board_back.anchor_position = board_back.width / 2, board_back.height / 2

    board_squares = [ # Create board alt squares
        pyglet.shapes.Rectangle(
            x*SQUARE_SIZE + BOARD_OFFSET_X,
            (y * 2 + x % 2)*SQUARE_SIZE + BOARD_OFFSET_Y,
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
    
    select_square = pyglet.shapes.Rectangle( # Add selection highlight square
        0, 0,
        SQUARE_SIZE, SQUARE_SIZE,
        color=(0, 64, 128))

    select_square.anchor_position = SQUARE_SIZE / 2, SQUARE_SIZE / 2
    select_square.opacity = 128
    select_square.visible = False

    @window.event
    def on_mouse_motion(x, y, dx, dy):
        # Floor cursor position to grid. Offsets so grid lines up with board.
        board_x = (x-CURSOR_OFFSET_X) // SQUARE_SIZE + GRID_OFFSET_X
        board_y = (y-CURSOR_OFFSET_Y) // SQUARE_SIZE + GRID_OFFSET_Y

        # Only show selection when within board area.
        if x > BOARD_LIMIT_LO[0] and y > BOARD_LIMIT_LO[1] and x < BOARD_LIMIT_HI[0] and y < BOARD_LIMIT_HI[1]:
            select_square.position = (
                board_x * SQUARE_SIZE,
                board_y * SQUARE_SIZE)
            select_square.visible = True
        else:
            select_square.visible = False

    @window.event
    def on_mouse_enter(x, y): 
        select_square.visible = True

    @window.event
    def on_mouse_leave(x, y):
        select_square.visible = False

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        if button == mouse.LEFT:
            if start_menu[0]._vertex_list: # Check if vertex list is None (means already deleted)
                for item in start_menu: # Delete start screen on first click
                    item.delete()
                music_player.next_source()
                music_player.queue(start_jingle)
                music_player.play()
            
            else:
                aud = [select, place, take, invalid]
                rng = randrange(len(aud))
                music_player.next_source()
                music_player.queue(aud[rng])
                music_player.play()
    
    @window.event
    def on_draw(): # Draw to window
        window.clear()
        board_batch.draw()
        select_square.draw()
        pieces_batch.draw()
        screen_batch.draw()
        menu_batch.draw()
        
    # Start music on start
    music_player.queue(menu_melody)
    music_player.play()

    rng = randrange(len(ON_RUN_MESSAGE))
    print(ON_RUN_MESSAGE[rng])
    pyglet.app.run()

def main():
    init()

if __name__ == "__main__":
    main()