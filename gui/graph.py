import pygame as pg
import sys
import os
from typing import List, Tuple

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.pathfinder import PathFinder
from graph_configs import Configs

config = Configs()
pf = PathFinder()

FG = config.get_color_palette().get("fg")
BG = config.COLOR_PALETTE.get("bg")


class MenuSurface:

    def __init__(self, parent) -> None:
        self.screen = parent
        self.width = self.screen.get_width()
        self.height = 50
        self.menu_rect = pg.Rect(0, 0, self.width, self.height)
        self.active_button = None

    def draw_menu(self):
        self.menu = pg.Surface.subsurface(self.screen, self.menu_rect)
        self.menu.fill(FG)

    def init_menu_buttons(self, num_buttons: int) -> List[Tuple[int, pg.Rect]]:
        self.button_list = []
        w = 100
        h = 40
        spacing = w + (w / 2)
        x = 0
        y = 5
        for i in range(num_buttons):
            if len(self.button_list) < 1:
                x = 100
            else:
                x += spacing
            self.button_rect = pg.Rect(x, y, w, h)
            self.button_list.append((i, self.button_rect))

        return self.button_list

    def draw_buttons(self, button_list: List[Tuple[int, pg.Rect]]) -> None:
        # TODO Add text to buttons
        for i in button_list:
            pg.draw.rect(self.menu, BG, i[1])

    def event_handler(
        self, menu_button_array: List[Tuple[int, pg.Rect]]
    ) -> tuple[int, bool]:
        counter = 0
        counter_array = []
        scale_factor_positive = 2.5
        scale_factor_negative = -2.5
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i in menu_button_array:
                    if i[1].collidepoint(event.pos):
                        counter += 1
                        counter_array.append(counter)
                        self.active_button = i[1]
                        self.active_button.inflate_ip(
                            scale_factor_positive, scale_factor_positive
                        )
                        print(f"Button clicked: ID: {i[0]}")
                        return (counter, True)
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1 and self.active_button != None:
                self.active_button.inflate_ip(
                    scale_factor_negative, scale_factor_negative
                )
                self.active_button = None
                print(f"Button released.")
                return (0, False)
        return (0, False)


class GridSurface:

    def __init__(self, parent: pg.Surface, cell_size: int) -> None:
        # Declare grid and grid dimensions
        self.grid_rect = pg.Rect(100, 100, 800, 600)
        self.grid = parent.subsurface(self.grid_rect)

        # Surface dimensions
        self.width = self.grid.get_width()
        self.height = self.grid.get_height()
        # Size of grid cell edge
        self.cell_size = cell_size
        # Dynamically allocate rows and columns
        self.num_rows = self.height / self.cell_size
        self.num_columns = self.width / self.cell_size

    def get_grid_surface(self):
        return self.grid

    def draw_grid(self):

        def draw_rows():
            y1 = 0.0
            for i in range(int(self.num_rows)):
                x1 = 0.0
                x2 = self.width
                y1 += self.cell_size
                y2 = y1
                pg.draw.lines(
                    surface=self.grid,
                    color=FG,
                    points=((x1, y1), (x2, y2)),
                    closed=True,
                )

        def draw_columns():
            x1 = 0.0
            for i in range(int(self.num_columns)):
                x1 += self.cell_size
                x2 = x1
                y1 = 0.0
                y2 = self.height
                pg.draw.lines(
                    surface=self.grid,
                    color=FG,
                    points=((x1, y1), (x2, y2)),
                    closed=True,
                )

        def draw_left():
            # Draw left most border
            start = (99.0, 99.0)
            stop = (99.0, 699.0)
            pg.draw.lines(
                surface=screen,
                points=(start, stop),
                color=FG,
                closed=True,
            )

        def draw_right():
            # Draw right most border
            start = (899.0, 99.0)
            stop = (899.0, 699.0)
            pg.draw.lines(
                surface=screen,
                points=(start, stop),
                color=FG,
                closed=True,
            )

        def draw_top():
            # Draw top most border
            start = (99.0, 99.0)
            stop = (899.0, 99.0)
            pg.draw.lines(
                surface=screen,
                points=(start, stop),
                color=FG,
                closed=True,
            )

        def draw_bottom():
            # Draw bottom most border
            start = (99.0, 699.0)
            stop = (899.0, 699.0)
            pg.draw.lines(
                surface=screen,
                points=(start, stop),
                color=FG,
                closed=True,
            )

        draw_rows()
        draw_columns()
        draw_left()
        draw_right()
        draw_top()
        draw_bottom()


class GridObjects:

    def __init__(self, parent: pg.Surface) -> None:
        self.grid = parent

        self.active_obj = None
        self.rect_array = []
        self.circle_array = []
    # TODO Add function to create a single object
    # def init_single_rect(self):
        # pass
    def init_rects(
        self,
        num_rects: int,
        x: int,
        y: int,
    ) -> list[tuple[int, pg.Rect]]:
        """
        params:
        """
        for i in range(num_rects):
            y += 100
            rect_obj = pg.Rect(x, y, 100, 50)
            self.rect_array.append((i, rect_obj))

        return self.rect_array

    def draw_rects(self, rect_array: list[tuple[int, pg.Rect]]) -> None:
        for i in rect_array:
            pg.draw.rect(self.grid, color=FG, rect=i[1])

    def event_handler(self, rect_array) -> None:
        # TODO Fix event loop to allow moving objects on grid
        mouse_pos = pg.mouse.get_pos()
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i in rect_array:
                    if i[1].collidepoint(event.pos):
                        self.active_obj = i[1]
                        print(
                            f"Current active rect: {self.active_obj}\n\t{self.active_obj.x}\n\t{self.active_obj.y}"
                        )
        elif event.type == pg.MOUSEMOTION:
            if self.active_obj != None:
                self.active_obj.centerx = mouse_pos[0]
                self.active_obj.centery = mouse_pos[1]
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                self.active_obj = None


if __name__ == "__main__":
    # Load variables
    # Init pygame
    pg.init()
    # Load screen
    screen = pg.display.set_mode(
        (config.ROOT_SURFACE_WIDTH, config.ROOT_SURFACE_HEIGHT)
    )
    # Load grid
    grid = GridSurface(parent=screen, cell_size=50)
    grid_surface = grid.get_grid_surface()
    # Load menu
    menu = MenuSurface(screen)
    # Load menu buttons
    menu_buttons = menu.init_menu_buttons(4)
    # Load grid objects
    grid_obj = GridObjects(grid_surface)
    # Main loop
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # Get button click event and counter
            button_event = menu.event_handler(menu_buttons)
            button_click = button_event[1]
            button_counter = button_event[0]
            if button_click:
                grid_obj_array = grid_obj.init_rects(button_counter, 100, 100)
            grid_obj.event_handler(grid_obj.rect_array)
        # Draw to screen
        screen.fill(BG)
        # Draw grid
        grid.draw_grid()
        # Draw menu
        menu.draw_menu()
        # Draw menu buttons
        menu.draw_buttons(menu_buttons)
        # Generate Objects
        grid_obj.draw_rects(grid_obj.rect_array)
        # Flip display
        pg.display.flip()
