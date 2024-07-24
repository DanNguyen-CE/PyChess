from .chess import *
from pyglet.gl import GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_NEAREST
from random import randrange

import pyglet

def init():
    """ Initialize Pyglet window and create PyChess instance """
    # Create Window
    window = pyglet.window.Window(WINDOW_SIZE, WINDOW_SIZE, NAME)
    window.set_icon(icon)
    pyglet.gl.glClearColor(44 /255, 52 /255, 66 /255, 1) # Window BG Color

    # Disable anti-aliasing and smoothing (for crisp pixel art)
    pyglet.gl.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    pyglet.gl.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    # Create PyChess with initial board state
    pychess = PyChess(init_board_state)

    # Window event listeners
    @window.event
    def on_mouse_motion(x, y, dx, dy):
        pychess.highlight(x, y)

    @window.event
    def on_mouse_enter(x, y): 
        pychess.select_square.visible = True

    @window.event
    def on_mouse_leave(x, y):
        pychess.select_square.visible = False

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        pychess.on_click(x, y, button)

    @window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        pychess.on_drag(x, y)

    @window.event
    def on_mouse_release(x, y, button, modifiers):
        pychess.highlight(x, y)
        pychess.on_release(x, y)

    @window.event
    def on_draw(): # Draw to window
        window.clear()
        pychess.main_batch.draw()
        
    # Start music on start
    play_sound(music_player, menu_melody, 1)

    rng = randrange(len(ON_RUN_MESSAGE))
    print(f"\033[92m{ON_RUN_MESSAGE[rng]}\033[0m\n")
    
def main():
    init()
    pyglet.app.run()

if __name__ == "__main__":
    main()