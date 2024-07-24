from pychess import *

class PyChess:
    def __init__(self, state):
        self.init_board_state = state
        
        # Define batches
        self.main_batch = pyglet.graphics.Batch()

        # Define groups
        self.board_group = pyglet.graphics.OrderedGroup(0)
        self.pieces_group = pyglet.graphics.OrderedGroup(1)
        self.selected_group = pyglet.graphics.OrderedGroup(2)
        self.menu_bg_group = pyglet.graphics.OrderedGroup(3)
        self.menu_group = pyglet.graphics.OrderedGroup(4)

        # UI
        self.start_menu = []
        self.logo = pyglet.sprite.Sprite
        self.board_back = pyglet.shapes.Rectangle
        self.board_squares_white = []
        self.board_squares_black = []
        self.select_square = pyglet.shapes.Rectangle

        # Board Values
        self.board_state = numpy.array([[]])
        self.enabled = True
        self.selected_x = 8
        self.selected_y = 8
        self.old_pos = 0
        self.white_turn = True

        self.create_ui()

    def create_ui(self):

        # Create start menu UI
        self.start_menu = [
            pyglet.shapes.Rectangle( # BG
                WINDOW_SIZE/2, WINDOW_SIZE /2, WINDOW_SIZE,
                WINDOW_SIZE, BG_COLOR,
                batch=self.main_batch, group=self.menu_bg_group),
            
            pyglet.sprite.Sprite( # Logo
                logo_large, WINDOW_SIZE//2, WINDOW_SIZE//2 + 200,
                batch=self.main_batch, group=self.menu_group),
            
            pyglet.text.Label( # Start Label
                START_LABEL, 
                font_name='Minecraft', font_size=20,
                x=WINDOW_SIZE//2, y=WINDOW_SIZE//2,
                anchor_x='center', anchor_y='center',
                batch=self.main_batch, group=self.menu_group),
            
            pyglet.text.Label( # Author Label
                AUTHOR_LABEL,
                font_name='Minecraft', font_size=10,
                x=WINDOW_SIZE//2, y=WINDOW_SIZE//2 - 250,
                anchor_x='center', anchor_y='center',
                align='center', multiline=True, width = 500,
                batch=self.main_batch, group=self.menu_group)
        ]

        self.start_menu[0].anchor_position = self.start_menu[0].width/2, self.start_menu[0].height/2 # BG Anchor

        # Create Board
        self.logo = pyglet.sprite.Sprite(resources.logo, WINDOW_SIZE//2, WINDOW_SIZE//6, batch=self.main_batch, group=self.board_group)
        self.board_back = pyglet.shapes.BorderedRectangle( 
            WINDOW_SIZE/2,
            WINDOW_SIZE/2 + 65,
            SQUARE_SIZE*8 + BORDER_SIZE*2,
            SQUARE_SIZE*8 + BORDER_SIZE*2,
            BORDER_SIZE,
            BOARD_ALT_COLOR,
            BORDER_COLOR,
            batch=self.main_batch, group=self.board_group)
        self.board_back.anchor_position = self.board_back.width/2, self.board_back.height/2

        pyglet.shapes.Rectangle._anchor_x = SQUARE_SIZE/2
        pyglet.shapes.Rectangle._anchor_y = SQUARE_SIZE/2

        # Create checkerboard patterns for white and black side of board
        self.board_squares_white = self.create_checkerboard(white=True)
        self.board_squares_black = self.create_checkerboard(white=False)

        for square in self.board_squares_black:
            square.visible = False

        # print('Creating Board State...')
        # print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
        #     for row in self.init_board_state]))
        
        # Array stores piece type and Sprite instances
        self.board_state = numpy.array([[
            (
            self.init_board_state[x][y],
            pyglet.sprite.Sprite(
                sprite,
                x*SQUARE_SIZE + BOARD_OFFSET_X,
                y*SQUARE_SIZE + BOARD_OFFSET_Y,
                batch=self.main_batch, group=self.pieces_group)
            )
            # Piece(x, y, self.init_board_state[x][y], sprite, self.main_batch, self.pieces_group)
            
            if (sprite := get_piece_sprite(self.init_board_state[x][y])) else (0, None)
            for y in range(8)
        ]
            for x in range(8)
        ])
        
        # Create hover highlight square
        self.select_square = pyglet.shapes.Rectangle( 
            0, 0,
            SQUARE_SIZE, SQUARE_SIZE,
            color=(0, 64, 128),
            batch=self.main_batch, group=self.board_group)

        self.select_square.opacity = 128
        self.select_square.visible = False

        self.white_turn = True
    
    def on_click(self, x, y, button):
        if button == mouse.LEFT:
            if self.start_menu[0]._vertex_list:  # Check if vertex list is None (means already deleted)
                for item in self.start_menu:     # Delete start screen on first click
                    item.delete()
                play_sound(music_player, start_jingle, 1)
            
            else: # Get piece coordinates and position on click
                board_x, board_y = pixel_to_grid(x, y, True)

                if valid_range(board_x, board_y) and self.board_state[board_x, board_y][1] is not None:
                    self.enabled = True
                    play_sound(music_player, select, 0.3)
                    self.selected_x, self.selected_y = board_x, board_y
                    self.old_pos = self.board_state[board_x, board_y][1].position

                    # Change render group to higher order to appear above other pieces
                    self.board_state[board_x, board_y][1].group = self.selected_group

    def on_drag(self, x: int, y: int):
        if not valid_range(self.selected_x, self.selected_y):
            return
        
        # Move piece with cursor position
        if self.board_state[self.selected_x, self.selected_y][1] is not None:
            self.board_state[self.selected_x, self.selected_y][1].position = x, y

    def on_release(self, x: int, y: int):
        if not valid_range(self.selected_x, self.selected_y):
            return
        
        # Return piece to original render group
        self.board_state[self.selected_x, self.selected_y][1].group = self.pieces_group

        new_x, new_y = pixel_to_grid(x, y, True)

        if (valid_range(new_x, new_y) and self.board_state[new_x, new_y][1] is None
            and self.board_state[self.selected_x, self.selected_y][1] is not None):

            play_sound(music_player, place, 0.3)
            self.board_state[self.selected_x, self.selected_y][1].position = grid_to_pixel(new_x, new_y)
            self.board_state[new_x, new_y] = self.board_state[self.selected_x, self.selected_y] # Update piece position in array
            self.board_state[self.selected_x, self.selected_y] = (0, None)                      # Remove old piece
            
            self.next_turn()
        
        elif self.board_state[self.selected_x, self.selected_y][1] is not None: # If placed in invalid position
            
            if (self.enabled and not                                            # Play sound if enabled and not placed on itself
                (self.selected_x == new_x and self.selected_y == new_y)):
                play_sound(music_player, invalid, 0.3)
                self.enabled = False
            
            self.board_state[self.selected_x, self.selected_y][1].position = self.old_pos   # Return to old position
            self.selected_x = self.selected_y = 8

    def create_checkerboard(self, white: bool):
        '''Create checkerboard pattern for white or black facing side'''
        board_squares = [
            pyglet.shapes.Rectangle(
            x*SQUARE_SIZE + BOARD_OFFSET_X,
            (y*2 + (x + (0 if white==True else 1)) % 2) * SQUARE_SIZE + BOARD_OFFSET_Y,
            SQUARE_SIZE, SQUARE_SIZE,
            color=BOARD_COLOR,
            batch=self.main_batch, group=self.board_group)

            for y in range(4)
            for x in range(8)
        ]

        return board_squares

    def highlight(self, x: int, y: int):
        '''Highlight tile under cursor'''

        board_x, board_y = pixel_to_grid(x, y)

        # Only show selection when within board area.
        if (x > BOARD_LIMIT_LO[0] and y > BOARD_LIMIT_LO[1] 
            and x < BOARD_LIMIT_HI[0] and y < BOARD_LIMIT_HI[1]):

            self.select_square.position = grid_to_pixel(board_x, board_y, False)
            self.select_square.visible = True
            
        else:
            self.select_square.visible = False

    def next_turn(self):
        '''Change board for next player's turn'''

        self.white_turn = not self.white_turn

        # Flip board squares
        for square in self.board_squares_white:
            square.visible = self.white_turn
        
        for square in self.board_squares_black:
            square.visible = not self.white_turn

        # Rotate pieces
        self.board_state = numpy.rot90(self.board_state, 2)

        # Update Sprite positions to new board state
        for x in range(8):
            for y in range(8):
                if (self.board_state[x, y][1]):
                    self.board_state[x, y][1].position = grid_to_pixel(x, y)