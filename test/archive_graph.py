import pygame
import sys
import toml

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.pathfinder import PathFinder
from gui.graph_configs import Configs  

configs = Configs()
pf = PathFinder()


# Drawing Functions
def get_configs():
    """
    Pass
    """
    with open(pf.GRAPH_CONFIG_TOML, "r", encoding="utf-8") as file:
        configs_array = []
        configs = toml.load(file)

        for k, v in configs.items():
            configs_array.append((k, v))

        return configs_array


def draw_grid(cell_length: float, color: tuple[int, int, int]):
    """
    Draw gridlines. Utilize the screen width and height to ensure dynamic
    sizing.
    """
    width = grid.get_width()
    height = grid.get_height()
    num_rows = height / cell_length
    num_columns = width / cell_length

    def draw_rows():
        """
        Pass
        """
        y1 = 0.0
        for i in range(int(num_rows)):
            x1 = 0.0
            x2 = width
            y1 += cell_length
            y2 = y1
            pygame.draw.lines(
                surface=grid,
                color=color,
                points=((x1, y1), (x2, y2)),
                closed=True,
            )

    def draw_columns():
        """
        Pass
        """
        x1 = 0.0
        for i in range(int(num_columns)):
            x1 += cell_length
            x2 = x1
            y1 = 0.0
            y2 = height
            pygame.draw.lines(
                surface=grid,
                color=color,
                points=((x1, y1), (x2, y2)),
                closed=True,
            )

    draw_rows()
    draw_columns()


def draw_grid_border():
    """
    Pass
    """

    def draw_left():
        # Draw left most border
        start = (99.0, 99.0)
        stop = (99.0, 699.0)
        pygame.draw.lines(
            surface=screen, points=(start, stop), color=grid_color_fg, closed=True
        )

    def draw_right():
        # Draw right most border
        start = (899.0, 99.0)
        stop = (899.0, 699.0)
        pygame.draw.lines(
            surface=screen, points=(start, stop), color=grid_color_fg, closed=True
        )

    def draw_top():
        # Draw top most border
        start = (99.0, 99.0)
        stop = (899.0, 99.0)
        pygame.draw.lines(
            surface=screen, points=(start, stop), color=grid_color_fg, closed=True
        )

    def draw_bottom():
        # Draw bottom most border
        start = (99.0, 699.0)
        stop = (899.0, 699.0)
        pygame.draw.lines(
            surface=screen, points=(start, stop), color=grid_color_fg, closed=True
        )

    # Draw borders by calling subfunctions
    draw_left()
    draw_right()
    draw_top()
    draw_bottom()


def draw_buttons(
    button_1: pygame.Rect,
    button_2: pygame.Rect,
    button_3: pygame.Rect,
    button_4: pygame.Rect,
):
    """
    Pass
    """

    def init_b_1():
        button_one = menu.subsurface(button_1)
        button_one.fill(button_color)

        font = pygame.font.SysFont("calibri", 15, bold=True)
        label = font.render("Button One", True, grid_color_bg)
        label_rect = label.get_rect()
        label_x = int(50)
        label_y = int(20)
        label_rect.centerx = label_x
        label_rect.centery = label_y
        button_one.blit(label, label_rect)

    def init_b_2():
        button_two = menu.subsurface(button_2)
        button_two.fill(button_color)

        font = pygame.font.SysFont("calibri", 15, bold=True)
        label = font.render("Button Two", True, grid_color_bg)
        label_rect = label.get_rect()
        label_x = int(50)
        label_y = int(20)
        label_rect.centerx = label_x
        label_rect.centery = label_y
        button_two.blit(label, label_rect)

    def init_b_3():
        button_three = menu.subsurface(button_3)
        button_three.fill(button_color)

        font = pygame.font.SysFont("calibri", 15, bold=True)
        label = font.render("Button Three", True, grid_color_bg)
        label_rect = label.get_rect()
        label_x = int(50)
        label_y = int(20)
        label_rect.centerx = label_x
        label_rect.centery = label_y
        button_three.blit(label, label_rect)

    def init_b_4():
        button_four = menu.subsurface(button_4)
        button_four.fill(button_color)

        font = pygame.font.SysFont("calibri", 15, bold=True)
        label = font.render("Button Four", True, grid_color_bg)
        label_rect = label.get_rect()
        label_x = int(50)
        label_y = int(20)
        label_rect.centerx = label_x
        label_rect.centery = label_y
        button_four.blit(label, label_rect)

    init_b_1()
    init_b_2()
    init_b_3()
    init_b_4()


# Load variables
width = configs.ROOT_SURFACE_WIDTH
height = configs.ROOT_SURFACE_HEIGHT

# Colors
grid_color_fg = (171, 178, 191)
grid_color_bg = (40, 44, 52)
rect_color = (209, 154, 102)
menu_color = (76, 82, 99)
button_color = (97, 175, 239)

# Init pygame
pygame.init()
pygame.font.init()

# Load root screen
screen = pygame.display.set_mode((width, height))

# Load grid surface
grid_rect = pygame.Rect(100, 100, 800, 600)
grid = screen.subsurface(grid_rect)

# Load menu surface
menu_rect = pygame.Rect(0, 0, width, 50)
menu = screen.subsurface(menu_rect)

# Load menu_button rects
active_button = None
button_one_rect = pygame.Rect(100, 5, 100, 40)
button_two_rect = pygame.Rect(300, 5, 100, 40)
button_three_rect = pygame.Rect(600, 5, 100, 40)
button_four_rect = pygame.Rect(800, 5, 100, 40)

button_list = [button_one_rect, button_two_rect, button_three_rect, button_four_rect]

# Load graph objects
active_rect = None
r = pygame.Rect(100, 100, 100, 50)

# Declare mouse variable for event processing
mouse = pygame.mouse.get_pressed()


# Mainloop and draw
while True:
    for event in pygame.event.get():
        # Check for exit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Check for mouse button down
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if r.collidepoint(event.pos):
                    active_rect = r
        # Check for mouse motion on screen
        elif event.type == pygame.MOUSEMOTION:
            if active_rect != None:
                r.centerx = pygame.mouse.get_pos()[0]
                r.centery = pygame.mouse.get_pos()[1]
        # Check if mouse button is released
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                active_rect = None

    # Fill main screen
    screen.fill(grid_color_bg)
    # Draw grid
    grid.fill(grid_color_bg)
    # Draw gridlines
    draw_grid(cell_length=50, color=grid_color_fg)
    # Draw graph objects
    pygame.draw.rect(surface=screen, rect=r, color=rect_color)
    # Draw main menu
    menu.fill(menu_color)
    # Draw buttons
    draw_buttons(button_one_rect, button_two_rect, button_three_rect, button_four_rect)
    # Draw grid_border
    draw_grid_border()
    # Flip display
    pygame.display.flip()
