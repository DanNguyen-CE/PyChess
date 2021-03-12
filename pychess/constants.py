import numpy

NAME = 'PyChess'
BG_COLOR = (44, 52, 66)
BOARD_COLOR = (63, 74, 89)
BOARD_ALT_COLOR = (200, 200, 200)
BORDER_COLOR = (0, 0, 0)
BORDER_SIZE = 5
WINDOW_SIZE = 640
SQUARE_SIZE = 400 // 8
PIECE_SIZE = SQUARE_SIZE - 10
BOARD_OFFSET_X = 145
BOARD_OFFSET_Y = 210

# Constants used for grid hightlighting
GRID_OFFSET_X = (BOARD_OFFSET_X / SQUARE_SIZE) % 1
GRID_OFFSET_Y = (BOARD_OFFSET_Y / SQUARE_SIZE) % 1
CURSOR_OFFSET_X = BOARD_OFFSET_X - SQUARE_SIZE * (BOARD_OFFSET_X//SQUARE_SIZE) - SQUARE_SIZE/2
CURSOR_OFFSET_Y = BOARD_OFFSET_Y - SQUARE_SIZE * (BOARD_OFFSET_Y//SQUARE_SIZE) - SQUARE_SIZE/2
BOARD_LIMIT_MARGIN = 5
BOARD_LIMIT_LO = (BOARD_OFFSET_X-SQUARE_SIZE/2 + BOARD_LIMIT_MARGIN, BOARD_OFFSET_Y-SQUARE_SIZE/2 + BOARD_LIMIT_MARGIN)
BOARD_LIMIT_HI = (BOARD_LIMIT_LO[0] + SQUARE_SIZE*8 - BOARD_LIMIT_MARGIN, BOARD_LIMIT_LO[1] + SQUARE_SIZE*8 - BOARD_LIMIT_MARGIN)

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

init_board_state = numpy.array( # The inital board state
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

# Flipping the array here because array coordinates and board coordinates are flipped.
init_board_state = numpy.flipud(init_board_state)
spec_board_state = numpy.flipud(spec_board_state)

ON_RUN_MESSAGE = [
    'PyChess is now running! NOTE: This is a WIP version of the application.',
    'Hover over the chessboard to see highlighting!',
    '[\'hip\', \'hip\'] (hip hip array!)',
    '(╯°□°)╯︵ ┻━┻',
    '( ͡° ͜ʖ ͡°)',
    '¯\_(ツ)_/¯',
    'ಠ ∩ ಠ'
]