import numpy

NAME = 'PyChess'
START_LABEL = '> Click anywhere to play! <'
AUTHOR_LABEL = ('A simple chess application created by Daniel Nguyen (2021).\n'
                'Arcade Music by joshuaempyre (freesound.org).\n'
                'Powered by Pyglet.')


BG_COLOR = (44, 52, 66)
BOARD_COLOR = (63, 74, 89)
BOARD_ALT_COLOR = (200, 200, 200)
BORDER_COLOR = (0, 0, 0)
BORDER_SIZE = 5
WINDOW_SIZE = 640
BOARD_SIZE = 400
SQUARE_SIZE = BOARD_SIZE // 8
PIECE_SIZE = SQUARE_SIZE - 10
BOARD_OFFSET_X = (BOARD_SIZE // 2) - SQUARE_SIZE - 5
BOARD_OFFSET_Y = (BOARD_SIZE // 2) + SQUARE_SIZE // 5

# Constants used for grid highlighting
GRID_OFFSET_X = (BOARD_OFFSET_X / SQUARE_SIZE) % 1
GRID_OFFSET_Y = (BOARD_OFFSET_Y / SQUARE_SIZE) % 1
CURSOR_OFFSET_X = BOARD_OFFSET_X - SQUARE_SIZE * (BOARD_OFFSET_X//SQUARE_SIZE) - SQUARE_SIZE/2
CURSOR_OFFSET_Y = BOARD_OFFSET_Y - SQUARE_SIZE * (BOARD_OFFSET_Y//SQUARE_SIZE) - SQUARE_SIZE/2
BOARD_LIMIT_LO = (BOARD_OFFSET_X - SQUARE_SIZE/2, BOARD_OFFSET_Y - SQUARE_SIZE/2)
BOARD_LIMIT_HI = (BOARD_LIMIT_LO[0] + SQUARE_SIZE*8, BOARD_LIMIT_LO[1] + SQUARE_SIZE*8)
NORMALIZE_X = 2.9 # The bottom left corner board_x coordinate
NORMALIZE_Y = 4.2 # The bottom left corner board_y coordinate

# print(CURSOR_OFFSET_X, CURSOR_OFFSET_Y)

# Piece positions range from 0-7 on both axis, starting from the bottom left:
#   ...      ...      ...
#  [0,2]    [1,2]    [2,2]    ...
#  [0,1]    [1,1]    [2,1]    ...
#  [0,0]    [1,0]    [2,0]    ...

# White = Positive
# Black = Negative
# Pawn = 1
# Rook = 2
# Knight = 3
# Bishop = 4
# Queen = 5
# King = 6

init_board_state = numpy.array( # The initial board state
    [
        [-2, -3, -4, -5, -6, -4, -3, -2],
        [-1, -1, -1, -1, -1, -1, -1, -1],
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 1,  1,  1,  1,  1,  1,  1,  1],
        [ 2,  3,  4,  5,  6,  4,  3,  2],
    ]
)

spec_board_state = numpy.array( # A special board state
    [
        [ 0,  0,  0, -1, -2, -3, -4, -6],
        [ 0,  0,  0,  0, -1, -1, -5, -3],
        [ 0,  0,  0,  0,  0, -1, -1, -4],
        [ 1,  0,  0,  0,  0,  0, -1, -2],
        [ 2,  1,  0,  0,  0,  0,  0, -1],
        [ 4,  1,  1,  0,  0,  0,  0,  0],
        [ 3,  5,  1,  1,  0,  0,  0,  0],
        [ 6,  4,  3,  2,  1,  0,  0,  0],
    ]
)

print('Creating Board State...')
print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
    for row in init_board_state]))

# Board states are set up like this for readability.
# Rotate array clockwise 90 degrees to fit board coordinates.
init_board_state = numpy.rot90(init_board_state, -1)
spec_board_state = numpy.rot90(spec_board_state, -1)

ON_RUN_MESSAGE = [
    'PyChess is now running! NOTE: This is a WIP version of the application.',
    'Hover over the chessboard to see highlighting!',
    'Click and drag pieces to move them. You can also click to move as well.',
    '[\'hip\', \'hip\'] (hip hip array!)',
    '(╯°□°)╯︵ ┻━┻',
    '( ͡° ͜ʖ ͡°)',
    '¯\_(ツ)_/¯',
    'ಠ ∩ ಠ'
]