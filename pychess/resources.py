import pyglet
from .constants import PIECE_SIZE
from itertools import chain

def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

def resize_image(image, x, y):
    """Resizes image by width x and height y"""
    image.width = x
    image.height = y

def scale_image(image, width):
    """Resizes image by width, keeping the aspect ratio"""
    wpercent = (width/float(image.width))
    h = int((float(image.height)*float(wpercent)))
    image.width = width
    image.height = h

pyglet.resource.path = [ # Define resource file paths (Note: is not recursive, so all subdirectories are specified)
    './assets/img/',
    './assets/img/black_pieces/',
    './assets/img/white_pieces/',
    './assets/audio/',
    './assets/fonts/']

pyglet.resource.reindex() # Must reindex when we change the path

# Load Image Resources
icon = pyglet.resource.image('icon.png')
logo = pyglet.resource.image('logo_full.png'); scale_image(logo, 300); center_image(logo)
logo_large = pyglet.resource.image('logo_full_large.png'); scale_image(logo_large, 500); center_image(logo_large)

# Load Audio Resources
music_player = pyglet.media.Player()
menu_melody = pyglet.resource.media('Melody.mp3')
start_jingle = pyglet.resource.media('Start.mp3')
end_jingle = pyglet.resource.media('End.mp3')
select = pyglet.resource.media('Select.mp3')
place = pyglet.resource.media('Place.mp3')
capture = pyglet.resource.media('Capture.mp3')
invalid = pyglet.resource.media('Invalid.mp3')

# Load Font Resources
font = pyglet.resource.add_font('Minecraft.ttf')

# Load Chess Pieces
white_pieces = [
    pyglet.resource.image('pawn_white.png'),
    pyglet.resource.image('rook_white.png'),
    pyglet.resource.image('knight_white.png'),
    pyglet.resource.image('bishop_white.png'),
    pyglet.resource.image('queen_white.png'),
    pyglet.resource.image('king_white.png')
]

black_pieces = [
    pyglet.resource.image('pawn_black.png'),
    pyglet.resource.image('rook_black.png'),
    pyglet.resource.image('knight_black.png'),
    pyglet.resource.image('bishop_black.png'),
    pyglet.resource.image('queen_black.png'),
    pyglet.resource.image('king_black.png')
]

for img in chain(white_pieces, black_pieces):
    resize_image(img, PIECE_SIZE, PIECE_SIZE)
    center_image(img)

def get_piece_sprite(piece):
    """Gets chess piece sprite from index of range(-6, 6).
       Returns None if piece index does not exist
    """
    switcher = {
        6: white_pieces[5],
        5: white_pieces[4],
        4: white_pieces[3],
        3: white_pieces[2],
        2: white_pieces[1],
        1: white_pieces[0],
        -1: black_pieces[0],
        -2: black_pieces[1],
        -3: black_pieces[2],
        -4: black_pieces[3],
        -5: black_pieces[4],
        -6: black_pieces[5],
    }

    return switcher.get(piece, None)