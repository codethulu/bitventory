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
ITEM_TEXTURES = {
    "grass": load_image("assets/items/grass.png"),
    "string": load_image("assets/items/string.png"),
    "silver_arrow": load_image("assets/items/silver_arrow.png"),
    "amethyst_clump": load_image("assets/items/amethyst_clump.png"),
    "iron_bar": load_image("assets/items/iron_bar.png"),
    "silver_bar": load_image("assets/items/silver_bar.png"),
    "gold_bar": load_image("assets/items/gold_bar.png"),
    "stick": load_image("assets/items/stick.png"),
    "diamond_clump": load_image("assets/items/diamond_clump.png"),
    "bone": load_image("assets/items/bone.png"),
    "flint": load_image("assets/items/flint.png"),
    "arrow": load_image("assets/items/arrow.png"),
    "book": load_image("assets/items/book.png"),
    "gold_sword": load_image("assets/items/gold_sword.png"),
    "iron_sword": load_image("assets/items/iron_sword.png"),
    "bow": load_image("assets/items/bow.png"),
    "gold_bow": load_image("assets/items/gold_bow.png"),
    "scythe": load_image("assets/items/scythe.png"),
}
ITEMS = {
    "grass": load_image("assets/items/grass.png"),
    "string": load_image("assets/items/string.png"),
    "silver_arrow": load_image("assets/items/silver_arrow.png"),
    "amethyst_clump": load_image("assets/items/amethyst_clump.png"),
    "iron_bar": load_image("assets/items/iron_bar.png"),
    "silver_bar": load_image("assets/items/silver_bar.png"),
    "gold_bar": load_image("assets/items/gold_bar.png"),
    "stick": load_image("assets/items/stick.png"),
    "diamond_clump": load_image("assets/items/diamond_clump.png"),
    "bone": load_image("assets/items/bone.png"),
    "flint": load_image("assets/items/flint.png"),
    "arrow": load_image("assets/items/arrow.png"),
    "book": load_image("assets/items/book.png"),

}
WEAPONS = {
    "gold_sword": load_image("assets/items/gold_sword.png"),
    "iron_sword": load_image("assets/items/iron_sword.png"),
    "bow": load_image("assets/items/bow.png"),
    "gold_bow": load_image("assets/items/gold_bow.png"),
    "scythe": load_image("assets/items/scythe.png"),

}
FONT = pygame.font.Font("assets/DTM-Sans.otf", 24)
DUST = [load_image(f"assets/gui/dust_{x}.png") for x in range(5)]
CURSOR_ICONS = {
    "magnet": load_image("assets/gui/magnet_cursor_icon.png"),
}
INVENTORY_SORTING_BUTTONS = {
    "name": load_image("assets/gui/sort_name.jpg"),
    "amount": load_image("assets/gui/sort_amount.jpg"),
    "type": load_image("assets/gui/sort_type.jpg"),

}


class Dust():
    def __init__(self) -> None:
        self.life = 12

    def update(self, x, y, scale) -> None:
        self.life -= 1
        if self.life > 0:
            image = pygame.transform.scale(
                DUST[4-(self.life // 3)], (16 * scale, 16 * scale))
            win.blit(image, (x + 2 * scale, y + 2 * scale))


class Cursor():
    def __init__(self) -> None:
        self.item = None
        self.position = pygame.mouse.get_pos()
        self.box = pygame.Rect(self.position[0], self.position[1], 1, 1)
        self.cooldown = 0
        self.pressed = None
        self.magnet = False

    def update(self, keys) -> None:
        self.position = pygame.mouse.get_pos()
        self.box = pygame.Rect(self.position[0], self.position[1], 1, 1)
        self.pressed = pygame.mouse.get_pressed()

        if self.item is not None:
            self.item.draw(self.position[0], self.position[1], 3)
        if self.cooldown > 0:
            self.cooldown -= 1

        self.magnet = True if keys[K_LSHIFT] and self.item is not None else False
        if self.magnet:
            image = pygame.transform.scale(
                CURSOR_ICONS["magnet"], (6 * 3, 6 * 3))
            win.blit(image, (self.position[0] +
                     2 * 3, self.position[1] + 12 * 3))

    def set_cooldown(self) -> None:
        self.cooldown = 10


class Item():
    def __init__(self, name, amount) -> None:
        self.name = name
        self.amount = amount
        self.stackable = True
        self.type = "item"

    def draw(self, x, y, scale) -> None:
        image = pygame.transform.scale(
            ITEM_TEXTURES[self.name], (16*scale, 16*scale))
        if self.amount > 1:
            image2 = pygame.transform.rotate(image, 10)
            win.blit(image2, (x + 3 *
                              scale, y))
        if self.amount > 50:
            image2 = pygame.transform.rotate(image, -20)
            win.blit(image2, (x + 1 *
                              scale, y))

        win.blit(image, (x + 2 * scale, y + 2 * scale))

        if self.amount > 1:
            item_count = FONT.render(
                str(self.amount), 1, (255, 255, 255))
            win.blit(item_count, (x + 12 * scale, y + 10 * scale))

    def copy(self):
        return Item(self.name, self.amount)


class Weapon(Item):
    def __init__(self, name, amount) -> None:
        super().__init__(name, amount)
        self.stackable = False
        self.type = "weapon"

    def copy(self):
        return Weapon(self.name, self.amount)


class Cell():

    def __init__(self, item=None) -> None:
        self.item = item
        self.particles = []

    def update(self, x, y, scale, stack_limit, cursor) -> None:
        position = (x, y)

        cell_box = pygame.Rect(
            position[0], position[1], 20 * scale, 20 * scale)

        if cursor.box.colliderect(cell_box):
            image = pygame.transform.scale(
                CELL_SELECTED, (20 * scale, 20 * scale))
        else:
            image = pygame.transform.scale(CELL, (20 * scale, 20 * scale))

        win.blit(image, position)

        if len(self.particles) > 0:
            for p in self.particles:
                p.update(x, y, scale)
                if p.life < 1:
                    self.particles.remove(p)

        if self.item is not None:
            self.item.draw(position[0], position[1], scale)
            if not cursor.box.colliderect(cell_box):
                return
            if cursor.cooldown != 0:
                return

            if cursor.magnet and cursor.item.name == self.item.name and self.item.stackable:
                amount = stack_limit - cursor.item.amount
                if self.item.amount + cursor.item.amount <= stack_limit:
                    cursor.item.amount += self.item.amount
                    self.item = None
                else:
                    cursor.item.amount += amount
                    self.item.amount -= amount

                self.particles.append(Dust())
                cursor.set_cooldown()

            if cursor.item is None:
                if cursor.pressed[0]:
                    cursor.item = self.item
                    self.item = None
                    self.particles.append(Dust())
                    cursor.set_cooldown()
                elif cursor.pressed[2] and self.item.amount > 1:
                    half = self.item.amount//2
                    cursor.item = self.item.copy()
                    cursor.item.amount = half
                    self.item.amount -= half
                    self.particles.append(Dust())
                    cursor.set_cooldown()
            else:
                if cursor.cooldown != 0:
                    return
                if cursor.pressed[0] and cursor.item.name == self.item.name and self.item.amount + cursor.item.amount <= stack_limit and self.item.stackable:
                    self.item.amount += cursor.item.amount
                    cursor.item = None
                    self.particles.append(Dust())
                    cursor.set_cooldown()
                elif cursor.pressed[0] and cursor.item.name == self.item.name and self.item.stackable:
                    amount = stack_limit - self.item.amount
                    self.item.amount += amount
                    cursor.item.amount -= amount
                    self.particles.append(Dust())
                    cursor.set_cooldown()
                elif cursor.pressed[0]:
                    temp = cursor.item.copy()
                    cursor.item = self.item
                    self.item = temp
                    self.particles.append(Dust())
                    cursor.set_cooldown()
        elif cursor.item is not None and cursor.box.colliderect(cell_box) and cursor.cooldown == 0:
            if cursor.pressed[0]:
                self.item = cursor.item
                cursor.item = None
                self.particles.append(Dust())
                cursor.set_cooldown()
            elif cursor.pressed[2] and cursor.item.amount > 1 and cursor.item.stackable:
                half = cursor.item.amount // 2
                self.item = cursor.item.copy()
                self.item.amount = half
                cursor.item.amount -= half
                self.particles.append(Dust())
                cursor.set_cooldown()


class Inventory():
    class Inventory_Sorting_Button():
        def __init__(self, name, inv) -> None:
            self.name = name
            self.image = INVENTORY_SORTING_BUTTONS[name]
            self.parent = inv

        def update(self, x, y, scale, cursor) -> None:
            button_box = pygame.Rect(
                x, y, 10 * scale, 10 * scale)
            if cursor.box.colliderect(button_box):
                if cursor.pressed[0]:
                    self.parent.sort_item_name()
                    match self.name:
                        case "name":
                            self.parent.sort_item_name()
                        case "amount":
                            self.parent.sort_item_amount()
                        case "type":
                            self.parent.sort_item_type()

            image = pygame.transform.scale(
                self.image, (10 * scale, 10 * scale))
            win.blit(image, (x, y))

    def __init__(self, name, rows, columns, x, y, scale=3, stack_limit=99, sorting_active=True) -> None:
        self.name = name
        self.rows = rows
        self.columns = columns
        self.cells = [[Cell() for i in range(columns)] for j in range(rows)]
        self.position = (x, y)
        self.scale = scale
        self.stack_limit = stack_limit
        if self.rows * self.columns >= 6 and self.columns >= 3 and sorting_active:
            self.buttons = [
                self.Inventory_Sorting_Button(x, self) for x in list(INVENTORY_SORTING_BUTTONS.keys())
            ]
        else:
            self.buttons = []

    def add_item(self, item) -> None:

        for row in self.cells:
            for cell in row:
                if cell.item is None:
                    cell.item = item
                    return
                elif item.stackable and cell.item.name == item.name:
                    if cell.item.amount + item.amount <= self.stack_limit:
                        cell.item.amount += item.amount
                        return
                    elif self.stack_limit - cell.item.amount > 0:
                        amount = self.stack_limit - cell.item.amount
                        cell.item.amount += amount
                        item.amount -= amount
                        if item.amount > 0:
                            self.add_item(item.copy())
                        return

        print("Inventory is full")

    def get_item_list(self) -> list:
        item_list = []
        for row in self.cells:
            for cell in row:
                if cell.item is not None:
                    item_list.append(cell.item.copy())
        return item_list

    def clear_inventory(self) -> None:
        for row in self.cells:
            for cell in row:
                cell.item = None

    def sort_item_name(self) -> None:
        item_list = self.get_item_list()
        item_list.sort(key=lambda x: x.name)
        self.clear_inventory()
        for item in item_list:
            self.add_item(item)

    def sort_item_amount(self) -> None:
        item_list = self.get_item_list()
        item_list.sort(key=lambda x: x.amount)
        self.clear_inventory()
        for item in item_list:
            self.add_item(item)

    def sort_item_type(self) -> None:
        item_list = self.get_item_list()
        item_list.sort(key=lambda x: self.get_type_sort_key(x.type))
        self.clear_inventory()
        for item in item_list:
            self.add_item(item)

    def get_type_sort_key(self, type) -> int:
        match type:
            case "weapon":
                return 1
            case "item":
                return 2

    def update(self, cursor) -> None:
        pygame.draw.rect(
            win, (31, 31, 31), (self.position[0], self.position[1], self.columns * 20 * self.scale + 4 * self.scale, self.rows * 20 * self.scale + 18 * self.scale))

        inventory_title = FONT.render(
            self.name, 1, (255, 255, 255))
        win.blit(inventory_title,
                 (self.position[0] + 4 * self.scale, self.position[1] + 4 * self.scale))

        for i, b in enumerate(self.buttons):
            b.update(self.position[0] + 20 * self.columns *
                     self.scale - 9 * self.scale - i * 12 * self.scale, self.position[1] + 4 * self.scale, self.scale, cursor)

        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                cell.update(self.position[0] + (j * 20 * self.scale) + 2 * self.scale,
                            self.position[1] + (i * 20 * self.scale) + 16 * self.scale, self.scale, self.stack_limit, cursor)


def main():
    inventory = Inventory("Large", 6, 10, 50, 100, 3, 99)
    inventory2 = Inventory("3x3", 3, 3, 700, 100, 3, 99)
    inventory3 = Inventory("Small", 1, 3, 700, 400, 3, 99)
    inventory4 = Inventory("Tall", 6, 3, 930, 100, 3, 99)
    inventory5 = Inventory("Tall2", 6, 2, 1170, 100, 3, 99)
    cursor = Cursor()
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
        if keys[K_w]:
            inventory.add_item(Weapon(random.choice(list(WEAPONS.keys())), 1))
        win.fill((0, 0, 0))
        inventory.update(cursor)
        inventory2.update(cursor)
        inventory3.update(cursor)
        inventory4.update(cursor)
        inventory5.update(cursor)
        cursor.update(keys)

        clock.tick(FPS)  # Pauses to keep track with FPS constant
        pygame.display.update()


if __name__ == "__main__":
    main()
