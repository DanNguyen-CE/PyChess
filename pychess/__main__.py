from pychess import *
from random import randrange

def init():
    """ Create Window & Initialize Board & Pieces """
    # Create Window
    window = pyglet.window.Window(WINDOW_SIZE, WINDOW_SIZE, NAME)
    window.set_icon(icon)
    pyglet.gl.glClearColor(44 /255, 52 /255, 66 /255, 1) # Window BG Color

    # Define batches
    main_batch = pyglet.graphics.Batch()

    # Define groups
    board_group = pyglet.graphics.OrderedGroup(0)
    pieces_group = pyglet.graphics.OrderedGroup(1)
    selected_group = pyglet.graphics.OrderedGroup(2)
    menu_bg_group = pyglet.graphics.OrderedGroup(3)
    menu_group = pyglet.graphics.OrderedGroup(4)

    # Create Start Screen Menu Items
    start_menu = [
        pyglet.shapes.Rectangle(WINDOW_SIZE/2, WINDOW_SIZE /2, WINDOW_SIZE, WINDOW_SIZE, BG_COLOR, batch=main_batch, group=menu_bg_group), # BG
        pyglet.sprite.Sprite(logo_large, WINDOW_SIZE / 2, WINDOW_SIZE / 2 + 200, batch=main_batch, group=menu_group), # Logo
        pyglet.text.Label( # Start Label
            START_LABEL, 
            font_name='Minecraft', font_size=20,
            x=WINDOW_SIZE/2, y=WINDOW_SIZE/2,
            anchor_x='center', anchor_y='center',
            batch=main_batch, group=menu_group),
        pyglet.text.Label( # Author Label
            AUTHOR_LABEL,
            font_name='Minecraft', font_size=10,
            x=WINDOW_SIZE/2, y=WINDOW_SIZE/2 - 250,
            anchor_x='center', anchor_y='center',
            align='center', multiline=True, width = 500,
            batch=main_batch, group=menu_group)
    ]

    start_menu[0].anchor_position = start_menu[0].width/2, start_menu[0].height/2 # BG Anchor

    # Create Board
    logo = pyglet.sprite.Sprite(resources.logo, WINDOW_SIZE / 2, WINDOW_SIZE / 6, batch=main_batch, group=board_group)
    board_back = pyglet.shapes.BorderedRectangle( 
        WINDOW_SIZE/2,
        WINDOW_SIZE/2 + 65,
        SQUARE_SIZE*8 + BORDER_SIZE*2,
        SQUARE_SIZE*8 + BORDER_SIZE*2,
        BORDER_SIZE,
        BOARD_ALT_COLOR,
        BORDER_COLOR,
        batch=main_batch, group=board_group)
    board_back.anchor_position = board_back.width / 2, board_back.height / 2

    pyglet.shapes.Rectangle._anchor_x = SQUARE_SIZE / 2
    pyglet.shapes.Rectangle._anchor_y = SQUARE_SIZE / 2

    board_squares = [ # Create board alt squares
        pyglet.shapes.Rectangle(
            x*SQUARE_SIZE + BOARD_OFFSET_X,
            (y*2 + x%2) * SQUARE_SIZE + BOARD_OFFSET_Y,
            SQUARE_SIZE, SQUARE_SIZE,
            color=BOARD_COLOR,
            batch=main_batch, group=board_group)
        
        for y in range(4)
        for x in range(8)
    ]

    board_squares_flip = [ # Create board alt squares
        pyglet.shapes.Rectangle(
            x*SQUARE_SIZE + BOARD_OFFSET_X,
            (y*2 + (x+1)%2) * SQUARE_SIZE + BOARD_OFFSET_Y,
            SQUARE_SIZE, SQUARE_SIZE,
            color=BOARD_COLOR,
            batch=main_batch, group=board_group)
        
        for y in range(4)
        for x in range(8)
    ]

    for square in board_squares_flip: # Center square anchors
        square.visible = False

    spritedt = numpy.dtype(pyglet.sprite.Sprite)
    board_state = numpy.array([[ # Array stores Sprite instances
        ( # Create board state with initial pieces
        init_board_state[x][y],
        pyglet.sprite.Sprite(
            sprite,
            x*SQUARE_SIZE + BOARD_OFFSET_X,
            y*SQUARE_SIZE + BOARD_OFFSET_Y,
            batch=main_batch, group=pieces_group)
        )
        
        if (sprite := get_piece_sprite(init_board_state[x][y])) else (0, None)
        for y in range(8)
    ]
        for x in range(8)
    ], dtype=spritedt)
    
    select_square = pyglet.shapes.Rectangle( # Add selection highlight square
        0, 0,
        SQUARE_SIZE, SQUARE_SIZE,
        color=(0, 64, 128),
        batch=main_batch, group=board_group)

    # select_square.anchor_position = SQUARE_SIZE / 2, SQUARE_SIZE / 2
    select_square.opacity = 128
    select_square.visible = False

    # White's turn = False, Black's turn = True
    white_turn = True

    @window.event
    def on_mouse_motion(x, y, dx, dy):
        highlight(select_square, x, y)

    @window.event
    def on_mouse_enter(x, y): 
        select_square.visible = True

    @window.event
    def on_mouse_leave(x, y):
        select_square.visible = False

    enabled = True
    selected_x = 8
    selected_y = 8
    old_pos = 0

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        nonlocal old_pos, selected_x, selected_y, enabled

        if button == mouse.LEFT:
            if start_menu[0]._vertex_list:  # Check if vertex list is None (means already deleted)
                for item in start_menu:     # Delete start screen on first click
                    item.delete()
                play_sound(music_player, start_jingle, 1)
            
            else: # Get piece coordinates and position on click
                board_x, board_y = pixel_to_grid(x, y, True)

                if valid_range(board_x, board_y) and board_state[board_x, board_y][1] is not None:
                    enabled = True
                    play_sound(music_player, select, 0.3)
                    selected_x, selected_y = board_x, board_y
                    old_pos = board_state[board_x, board_y][1].position

                    # Change render group to higher order to appear above other pieces
                    board_state[board_x, board_y][1].group = selected_group

    @window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        if not valid_range(selected_x, selected_y):
            return

        if board_state[selected_x, selected_y][1] is not None:
            board_state[selected_x, selected_y][1].position = x, y   # Move piece with cursor position

    @window.event
    def on_mouse_release(x, y, button, modifiers):
        highlight(select_square, x, y)
        nonlocal selected_x, selected_y, enabled, white_turn, board_state
        
        if not valid_range(selected_x, selected_y):
            return
        
        # Return piece to original render group
        board_state[selected_x, selected_y][1].group = pieces_group

        new_x, new_y = pixel_to_grid(x, y, True)

        if (valid_range(new_x, new_y) and board_state[new_x, new_y][1] is None
            and board_state[selected_x, selected_y][1] is not None):
            play_sound(music_player, place, 0.3)
            board_state[selected_x, selected_y][1].position = grid_to_pixel(new_x, new_y)
            board_state[new_x, new_y] = board_state[selected_x, selected_y] # Update piece position in array
            board_state[selected_x, selected_y] = (0, None)                 # Remove old piece

            white_turn = not white_turn
            flip_board(board_squares, board_squares_flip, white_turn)
            board_state = flip_pieces(board_state)
        
        elif board_state[selected_x, selected_y][1] is not None:        # If placed in invalid position
            if (enabled and not                                         # Play sound if enabled and not placed on itself
                (selected_x == new_x and selected_y == new_y)):
                play_sound(music_player, invalid, 0.3)
                enabled = False
            board_state[selected_x, selected_y][1].position = old_pos   # Return to old position
            selected_x = selected_y = 8

    @window.event
    def on_draw(): # Draw to window
        window.clear()
        main_batch.draw()
        
    # Start music on start
    play_sound(music_player, menu_melody, 1)

    rng = randrange(len(ON_RUN_MESSAGE))
    print(f"\033[92m{ON_RUN_MESSAGE[rng]}\033[0m\n")
    pyglet.app.run()

def highlight(select_square, x, y):
    board_x, board_y = pixel_to_grid(x, y)

    # Only show selection when within board area.
    if (x > BOARD_LIMIT_LO[0] and y > BOARD_LIMIT_LO[1] 
        and x < BOARD_LIMIT_HI[0] and y < BOARD_LIMIT_HI[1]):
        select_square.position = grid_to_pixel(board_x, board_y, False)
        
        select_square.visible = True
    else:
        select_square.visible = False

def flip_board(a, b, current):

    for square in a: # Center square anchors
        square.visible = current
    
    for square in b:
        square.visible = not current

def flip_pieces(pieces):

    pieces = numpy.rot90(pieces, 2)

    for x in range(8):
        for y in range(8):
            if (pieces[x, y][1]):
                pieces[x, y][1].position = grid_to_pixel(x, y)

    return pieces

def main():
    init()

if __name__ == "__main__":
    main()