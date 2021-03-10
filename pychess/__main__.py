import pyglet
from pyglet.window import mouse

NAME = 'échecs'

BOARD_COLOR = (96, 96, 96)
BOARD_ALT_COLOR = (128, 128, 128)

WINDOW_SIZE = 640
SQUARE_SIZE = WINDOW_SIZE // 8

def run_demo():
    window = pyglet.window.Window(WINDOW_SIZE, WINDOW_SIZE, NAME)

    label = pyglet.text.Label(f'{NAME}!',
        font_name='Comics Sans',
        font_size=48,
        x = window.width // 2, y = window.height // 2,
        anchor_x='center', anchor_y='center'
    )

    board_batch = pyglet.graphics.Batch()

    board_squares = [
        pyglet.shapes.Rectangle(
            x * SQUARE_SIZE, (y * 2 + x % 2) * SQUARE_SIZE,
            SQUARE_SIZE, SQUARE_SIZE,
            color=BOARD_COLOR,
            batch=board_batch)
        for y in range(4)
        for x in range(8)
    ]

    @window.event
    def on_draw():
        window.clear()
        board_batch.draw()
        label.draw()

    # event_logger = pyglet.window.event.WindowEventLogger()

    # window.push_handlers(event_logger)

    pyglet.app.run()

def main():
    print("Hello World!")
    run_demo()

if __name__ == "__main__":
    main()