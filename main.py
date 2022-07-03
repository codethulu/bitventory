# program to create item inventory
import pygame
import os
from pygame.locals import *
import random

SCREENWIDTH = 1430
SCREENHEIGHT = 800
FPS = 60
pygame.init()
pygame.display.set_icon(pygame.image.load("icon.jpg"))  # sets program icon
win = pygame.display.set_mode(
    (SCREENWIDTH, SCREENHEIGHT))  # sets size of the window
pygame.display.set_caption("TEST")  # title of project
clock = pygame.time.Clock()


def load_image(image_name):
    return pygame.image.load(image_name).convert_alpha()


CELL = load_image("assets/gui/tile.jpg")
CELL_SELECTED = load_image("assets/gui/tile_selected.jpg")
ITEMS = {
    "grass": load_image("assets/items/grass.png"),
    "string": load_image("assets/items/string.png"),
    "silver_arrow": load_image("assets/items/silver_arrow.png"),
    "amethyst_clump": load_image("assets/items/amethyst_clump.png"),
    "iron_bar": load_image("assets/items/iron_bar.png"),
}
FONT = pygame.font.Font("assets/DTM-Sans.otf", 24)


class Item():
    def __init__(self, name, amount) -> None:
        self.name = name
        self.amount = amount


class Cell():

    def __init__(self, item=None) -> None:
        self.item = item

    def update(self, x, y, scale) -> None:
        position = (x, y)
        cursor_pos = pygame.mouse.get_pos()
        cursor_box = pygame.Rect(cursor_pos[0], cursor_pos[1], 1, 1)
        cell_box = pygame.Rect(position[0], position[1], 20*scale, 20*scale)

        if cursor_box.colliderect(cell_box):
            image = pygame.transform.scale(
                CELL_SELECTED, (20*scale, 20*scale))
        else:
            image = pygame.transform.scale(CELL, (20*scale, 20*scale))

        win.blit(image, position)

        if self.item is not None:
            image = pygame.transform.scale(
                ITEMS[self.item.name], (16*scale, 16*scale))
            if self.item.amount > 1:
                image2 = pygame.transform.rotate(image, 10)
                win.blit(image2, (position[0] + 3 *
                         scale, position[1]))

            win.blit(image, (position[0] + 2*scale, position[1] + 2*scale))

            if self.item.amount > 1:
                item_count = FONT.render(
                    str(self.item.amount), 1, (255, 255, 255))
                win.blit(item_count, (position[0], position[1]))


class Inventory():
    def __init__(self, name, rows, columns, x, y, scale, stack_limit) -> None:
        self.name = name
        self.rows = rows
        self.columns = columns
        self.cells = [[Cell() for i in range(columns)] for j in range(rows)]
        self.position = (x, y)
        self.scale = scale
        self.stack_limit = stack_limit

    def add_item(self, item) -> None:
        for row in self.cells:
            for cell in row:
                if cell.item is None:
                    cell.item = item
                    return
                elif cell.item.name == item.name and cell.item.amount + item.amount <= self.stack_limit:
                    cell.item.amount += item.amount
                    return
        print("Inventory is full")

    def sort_items(self) -> None:
        # order the items in cells by name
        pass

    def update(self) -> None:

        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                cell.update(self.position[0]+(i*20*self.scale),
                            self.position[1]+(j*20*self.scale), self.scale)


def main():
    inventory = Inventory("Test", 10, 6, 100, 100, 3, 99)
    run = True
    while run:
        for event in pygame.event.get():  # Test to see if the usr quits the game, if so, quit
            if event.type == pygame.QUIT:
                print("Program closed by user.")
                pygame.quit()
                os._exit(1)

        pygame.event.get()
        keys = pygame.key.get_pressed()
        if keys[K_c]:
            inventory.add_item(Item(random.choice(list(ITEMS.keys())), 1))

        win.fill((0, 0, 0))
        inventory.update()

        clock.tick(FPS)  # Pauses to keep track with FPS constant
        pygame.display.update()


if __name__ == "__main__":
    main()
