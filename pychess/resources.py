import pyglet
from .constants import PIECE_SIZE

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

# Load all chess piece images. Scale to correct size, and center anchor. TODO: NEEDS REFACTORING
class Black():
    king = pyglet.resource.image('king_black.png'); resize_image(king, PIECE_SIZE, PIECE_SIZE); center_image(king)
    queen = pyglet.resource.image('queen_black.png'); resize_image(queen, PIECE_SIZE, PIECE_SIZE); center_image(queen)
    bishop = pyglet.resource.image('bishop_black.png'); resize_image(bishop, PIECE_SIZE, PIECE_SIZE); center_image(bishop)
    knight = pyglet.resource.image('knight_black.png'); resize_image(knight, PIECE_SIZE, PIECE_SIZE); center_image(knight)
    rook = pyglet.resource.image('rook_black.png'); resize_image(rook, PIECE_SIZE, PIECE_SIZE); center_image(rook)
    pawn = pyglet.resource.image('pawn_black.png'); resize_image(pawn, PIECE_SIZE, PIECE_SIZE); center_image(pawn)

class White():
    king = pyglet.resource.image('king_white.png'); resize_image(king, PIECE_SIZE, PIECE_SIZE); center_image(king)
    queen = pyglet.resource.image('queen_white.png'); resize_image(queen, PIECE_SIZE, PIECE_SIZE); center_image(queen)
    bishop = pyglet.resource.image('bishop_white.png'); resize_image(bishop, PIECE_SIZE, PIECE_SIZE); center_image(bishop)
    knight = pyglet.resource.image('knight_white.png'); resize_image(knight, PIECE_SIZE, PIECE_SIZE); center_image(knight)
    rook = pyglet.resource.image('rook_white.png'); resize_image(rook, PIECE_SIZE, PIECE_SIZE); center_image(rook)
    pawn = pyglet.resource.image('pawn_white.png'); resize_image(pawn, PIECE_SIZE, PIECE_SIZE); center_image(pawn)

def get_piece_sprite(piece):
    """Gets chess piece sprite from index of range(-6, 6).
       Returns None if piece index does not exist
    """
    switcher = {
        6: White.king,
        5: White.queen,
        4: White.bishop,
        3: White.knight,
        2: White.rook,
        1: White.pawn,
        -1: Black.pawn,
        -2: Black.rook,
        -3: Black.knight,
        -4: Black.bishop,
        -5: Black.queen,
        -6: Black.king,
    }

    return switcher.get(piece, None)