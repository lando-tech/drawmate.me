import pygame as pg
import sys


# Load variables
pg.init()

# Screen dimensions
w_h = (800, 600)
# Game colors
bg = (0, 0, 0)
fg = (255, 255, 255)
# Snake dimensions
x = 100
y = 100
rect_w = 20
rect_h = 20
# Load screen
screen = pg.display.set_mode(w_h)
snake = pg.Rect(x, y, rect_w, rect_h)

# Update variables
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.K_w:
            snake.move(90, 0)
    pg.time.delay(5)
    snake.move_ip(1, 0)
    # Draw variables

    # Draw screen
    screen.fill(bg)

    # Draw snake
    pg.draw.rect(surface=screen, color=fg, rect=snake)
    pg.display.update()
    pg.display.flip()
