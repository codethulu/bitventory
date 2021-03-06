# program to create item inventory
from operator import length_hint
from signal import default_int_handler
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
BIN_CELL = load_image("assets/gui/tile_bin.jpg")
BIN_CELL_SELECTED = load_image("assets/gui/tile_bin_selected.jpg")
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
    "poison": load_image("assets/items/poison.png"),
    "poison_arrow": load_image("assets/items/poison_arrow.png"),
    "health_potion": load_image("assets/items/health_potion.png"),
    "bronze_bar": load_image("assets/items/bronze_bar.png"),
    "bronze_sword": load_image("assets/items/bronze_sword.png"),
    "glass": load_image("assets/items/glass.png"),
    "glass_bottle": load_image("assets/items/glass_bottle.png"),
    "paper": load_image("assets/items/paper.png"),
    "rose": load_image("assets/items/rose.png"),
    "daisy": load_image("assets/items/daisy.png"),
    "amethyst_arrow": load_image("assets/items/amethyst_arrow.png"),
    "feather": load_image("assets/items/feather.png"),
    "bone_arrow": load_image("assets/items/bone_arrow.png"),
}
ITEMS = {
    "grass": {"name": "Grass", "description": "It's some grass."},
    "string": {"name": "String", "description": ""},
    "silver_arrow": {"name": "Silver Arrow", "description": "A stronger arrow made from silver. Suitable for hunting the supernatural."},
    "amethyst_clump": {"name": "Amethyst Clump", "description": ""},
    "iron_bar": {"name": "Iron Bar", "description": ""},
    "silver_bar": {"name": "Silver Bar", "description": ""},
    "gold_bar": {"name": "Gold Bar", "description": ""},
    "stick": {"name": "Stick", "description": ""},
    "diamond_clump": {"name": "Diamond Clump", "description": ""},
    "bone": {"name": "Bone", "description": ""},
    "flint": {"name": "Flint", "description": ""},
    "arrow": {"name": "Arrow", "description": ""},
    "book": {"name": "Book", "description": ""},
    "poison": {"name": "Poison", "description": ""},
    "poison_arrow": {"name": "Poison Arrow", "description": ""},
    "health_potion": {"name": "Health Potion", "description": ""},
    "bronze_bar": {"name": "Bronze Bar", "description": ""},
    "glass": {"name": "Glass", "description": ""},
    "glass_bottle": {"name": "Glass Bottle", "description": ""},
    "paper": {"name": "Paper", "description": ""},
    "rose": {"name": "Rose", "description": ""},
    "daisy": {"name": "Daisy", "description": ""},
    "amethyst_arrow": {"name": "Amethyst Arrow", "description": ""},
    "feather": {"name": "Feather", "description": ""},
    "bone_arrow": {"name": "Bone Arrow", "description": ""},
}
WEAPONS = {
    "gold_sword": {"name": "Gold Sword", "description": ""},
    "iron_sword": {"name": "Iron Sword", "description": ""},
    "bow": {"name": "Bone Arrow", "description": ""},
    "gold_bow": {"name": "Gold Bow", "description": ""},
    "scythe": {"name": "Scythe", "description": "Used for farming and combat!"},
    "bronze_sword": {"name": "Bronze Sword", "description": ""},

}
FONT = {
    "16": pygame.font.Font("assets/DTM-Sans.otf", 16),
    "24": pygame.font.Font("assets/DTM-Sans.otf", 24)
}
DUST = [load_image(f"assets/gui/dust_{x}.png") for x in range(6)]

CURSOR_ICONS = {
    "cursor": load_image("assets/gui/cursor.png"),
    "grab": load_image("assets/gui/cursor_grab.png"),
    "magnet": load_image("assets/gui/cursor_magnet.png"),
    "move": load_image("assets/gui/cursor_move.png"),
    "text": load_image("assets/gui/cursor_text.png"),           # Added cursor text icon
}
INVENTORY_SORTING_BUTTONS = {
    "name": load_image("assets/gui/sort_name.jpg"),
    "amount": load_image("assets/gui/sort_amount.jpg"),
    "type": load_image("assets/gui/sort_type.jpg"),
    "select": load_image("assets/gui/sort_select.png"),

}

# Search Bar assets (Made temporarily for visual purposes)

SEARCH_BAR = {
    "left": load_image("assets/gui/search_left.png"),
    "middle": load_image("assets/gui/search_middle.png"),
    "right": load_image("assets/gui/search_right.png"),
}

SEARCH_BAR_SELECTED = {
    "left": load_image("assets/gui/search_sel_left.png"),
    "middle": load_image("assets/gui/search_sel_middle.png"),
    "right": load_image("assets/gui/search_sel_right.png"),
}


class Dust():
    def __init__(self) -> None:
        self.life = 20

    def update(self, x, y, scale) -> None:
        self.life -= 1
        if self.life > 0:
            image = pygame.transform.scale(
                DUST[5 - (self.life // 4)], (16 * scale, 16 * scale))
            win.blit(image, (x + 2 * scale, y + 2 * scale))


class Cursor_Context_Box():
    def __init__(self, name, description, flip) -> None:
        self.name = name
        self.description = description
        self.flip = flip

    def update(self, x, y, scale) -> None:
        footer = False

        height = 0.55 * 20 * scale
        width = 4 * 20 * scale
        offset = {"x": 0, "y": 0}

        if x > SCREENWIDTH - width:
            offset["x"] = -width

        if y > SCREENHEIGHT - height:
            offset["y"] = -height

        desc = [""]
        line = 0

        words = self.description.split(' ')
        if len(words) > 1:
            height += 0.26 * 20 * scale
            footer = True

        for i, word in enumerate(words):
            if not len(word) + len(desc[line]) > 30:
                desc[line] += (" " if i != 0 else "") + word
            else:
                desc.append("")
                line += 1
                desc[line] += word
                height += 0.26 * 20 * scale

        if footer:
            height += 0.2 * 20 * scale

        pygame.draw.rect(
            win, (255, 255, 255), (x+12 + offset["x"], y+12 + offset["y"], width, height))
        pygame.draw.rect(
            win, (31, 31, 31), (x+15 + offset["x"], y+15 + offset["y"], width - 6, height - 6))

        inventory_title = FONT["24"].render(
            self.name, 1, (255, 255, 255))
        win.blit(inventory_title,
                 (x + 7 * 3 + offset["x"], y + 4 * 3 + offset["y"]))

        line = 0
        for d in desc:
            description = FONT["16"].render(d, 1, (180, 180, 180))
            win.blit(description, (x + 7 * 3 + offset["x"],
                     y + 1.5 * 20 + 4 * 3 + line * 5 + offset["y"]))
            line += 3


class Cursor():
    def __init__(self) -> None:
        self.item = None
        self.position = pygame.mouse.get_pos()
        self.box = pygame.Rect(*self.position, 1, 1)
        self.cooldown = 0
        self.pressed = None
        self.magnet = False
        self.move = False
        self.text = False
        self.context = None

    def update(self, keys, search_bar_pos, search_bar_scale) -> None:
        self.position = pygame.mouse.get_pos()
        self.box = pygame.Rect(*self.position, 1, 1)
        self.pressed = pygame.mouse.get_pressed()

        if self.item is not None:
            self.item.draw(*self.position, 3)
        if self.cooldown > 0:
            self.cooldown -= 1

        search_box = pygame.Rect(search_bar_pos[0], search_bar_pos[1] + 16 * search_bar_scale, 21 * 20 * search_bar_scale, 20 * search_bar_scale)
        self.text = self.box.colliderect(search_box)                # Colliding with search box changes cursor to text
        self.magnet = keys[K_LSHIFT] and self.item is not None
        self.move = keys[K_LSHIFT] and not self.magnet

        if self.context is not None:
            self.context.update(*self.position, 3)
            self.context = None

        if self.magnet:
            image = pygame.transform.scale(
                CURSOR_ICONS["magnet"], (9 * 3, 10 * 3))
        elif self.move:
            image = pygame.transform.scale(
                CURSOR_ICONS["move"], (9 * 3, 10 * 3))
        elif self.item is not None:
            image = pygame.transform.scale(
                CURSOR_ICONS["grab"], (9 * 3, 10 * 3))
        elif self.text:
            image = pygame.transform.scale(
                CURSOR_ICONS["text"], (9 * 3, 10 * 3))          # Added cursor text icon
        else:
            image = pygame.transform.scale(
                CURSOR_ICONS["cursor"], (9 * 3, 10 * 3))

        win.blit(image, (self.position[0], self.position[1]))

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
            ITEM_TEXTURES[self.name], (16 * scale, 16 * scale))
        if self.amount > 1:
            image2 = pygame.transform.rotate(image, 10)
            win.blit(image2, (x + 3 *
                              scale, y))
        if self.amount > 24:
            image2 = pygame.transform.rotate(image, -20)
            win.blit(image2, (x + 1 *
                              scale, y))
        if self.amount > 50:
            image2 = pygame.transform.rotate(image, 30)
            win.blit(image2, (x - 2 *
                              scale, y - 1 * scale))

        win.blit(image, (x + 2 * scale, y + 2 * scale))

        if self.amount > 1:
            item_count = FONT["24"].render(
                str(self.amount), 1, (255, 255, 255))
            win.blit(item_count, (x + 12 * scale, y + 10 * scale))

    def copy(self):
        return Item(self.name, self.amount)

    def get_name(self):
        return ITEMS[self.name]["name"]

    def get_description(self):
        return ITEMS[self.name]["description"]


class Weapon(Item):
    def __init__(self, name, amount) -> None:
        super().__init__(name, amount)
        self.stackable = False
        self.type = "weapon"

    def copy(self):
        return Weapon(self.name, self.amount)

    def get_name(self):
        return WEAPONS[self.name]["name"]

    def get_description(self):
        return WEAPONS[self.name]["description"]


class Cell():

    def __init__(self, item=None) -> None:
        self.item = item
        self.particles = []

    def draw(self, scale, selected):
        match selected:
            case 1:
                image = pygame.transform.scale(
                    CELL_SELECTED, (20 * scale, 20 * scale))
            case 0:
                image = pygame.transform.scale(CELL, (20 * scale, 20 * scale))
        return image

    def update(self, x, y, scale, stack_limit, inventory_id, inventory_list, cursor) -> None:
        position = (x, y)

        cell_box = pygame.Rect(
            *position, 20 * scale, 20 * scale)

        if cursor.box.colliderect(cell_box):
            image = self.draw(scale, 1)
        else:
            image = self.draw(scale, 0)

        win.blit(image, position)

        if len(self.particles) > 0:
            for p in self.particles:
                p.update(x, y, scale)
                if p.life < 1:
                    self.particles.remove(p)

        if self.item is not None:
            self.item.draw(*position, scale)
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
                cursor.context = Cursor_Context_Box(
                    self.item.get_name(), self.item.get_description(), 0 if True else 1)
                if cursor.pressed[0] and cursor.move:
                    index = inventory_id
                    for i in range(len(inventory_list)):
                        index = index + \
                            1 if index < len(inventory_list) - 1 else 0
                        if index == inventory_id:
                            break
                        if inventory_list[index].capacity != inventory_list[index].item_count:
                            break
                    temp = self.item.copy()
                    self.item = None
                    inventory_list[index].add_item(temp)
                    self.particles.append(Dust())
                    cursor.set_cooldown()

                elif cursor.pressed[0]:
                    cursor.item = self.item
                    self.item = None
                    self.particles.append(Dust())
                    cursor.set_cooldown()
                elif cursor.pressed[2] and self.item.amount > 1:
                    half = self.item.amount // 2
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
            elif cursor.pressed[2] and cursor.item.stackable:
                if cursor.item.amount > 1:
                    half = cursor.item.amount // 2
                    self.item = cursor.item.copy()
                    self.item.amount = half
                    cursor.item.amount -= half
                else:
                    self.item = cursor.item
                    cursor.item = None

                self.particles.append(Dust())
                cursor.set_cooldown()


class Bin(Cell):
    def __init__(self, item=None) -> None:
        super().__init__(item)

    def draw(self, scale, selected):
        match selected:
            case 1:
                image = pygame.transform.scale(
                    BIN_CELL_SELECTED, (20 * scale, 20 * scale))
            case 0:
                image = pygame.transform.scale(
                    BIN_CELL, (20 * scale, 20 * scale))
        return image


class Inventory():
    class Inventory_Sorting_Button():
        def __init__(self, name, inv) -> None:
            self.name = name
            self.image = INVENTORY_SORTING_BUTTONS[name]
            self.parent = inv

        def update(self, x, y, scale, cursor) -> None:
            image = pygame.transform.scale(
                self.image, (10 * scale, 10 * scale))
            win.blit(image, (x, y))

            button_box = pygame.Rect(
                x, y, 10 * scale, 10 * scale)
            if cursor.box.colliderect(button_box):
                image = pygame.transform.scale(
                    INVENTORY_SORTING_BUTTONS["select"], (10 * scale, 10 * scale))
                win.blit(image, (x, y))
                if cursor.pressed[0]:
                    self.parent.sort_item_name()
                    match self.name:
                        case "name":
                            self.parent.sort_item_name()
                        case "amount":
                            self.parent.sort_item_amount()
                        case "type":
                            self.parent.sort_item_type()

    def __init__(self, name, rows, columns, x, y, scale=3, stack_limit=99, sorting_active=True, bin_active=False) -> None:
        self.name = name
        self.rows = rows
        self.columns = columns
        self.cells = [[Cell() for i in range(columns)] for j in range(rows)]
        self.position = (x, y)
        self.scale = scale
        self.stack_limit = stack_limit
        self.capacity = rows * columns
        self.item_count = 0
        self.bin = bin_active
        if self.capacity >= 6 and self.columns >= 3 and sorting_active:
            self.buttons = [
                self.Inventory_Sorting_Button(x, self) for x in list(INVENTORY_SORTING_BUTTONS.keys()) if x != "select"
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

    def get_item_count(self) -> int:
        item_count = 0
        for row in self.cells:
            for cell in row:
                if cell.item is not None:
                    item_count += 1
        return item_count

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

    def update(self, inventory_id, inventory_list, cursor, text) -> None:
        self.item_count = self.get_item_count()
        pygame.draw.rect(
            win, (31, 31, 31), (*self.position, self.columns * 20 * self.scale + 4 * self.scale, self.rows * 20 * self.scale + 18 * self.scale + (20 * self.scale if self.bin else 0)))

        inventory_title = FONT["24"].render(
            self.name, 1, (255, 255, 255))
        win.blit(inventory_title,
                 (self.position[0] + 4 * self.scale, self.position[1] + 4 * self.scale))

        for i, b in enumerate(self.buttons):
            b.update(self.position[0] + 20 * self.columns *
                     self.scale - 9 * self.scale - i * 12 * self.scale, self.position[1] + 4 * self.scale, self.scale, cursor)

        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                cell.update(self.position[0] + (j * 20 * self.scale) + 2 * self.scale,
                            self.position[1] + (i * 20 * self.scale) + 16 * self.scale, self.scale, self.stack_limit, inventory_id, inventory_list, cursor)
        bin_cell = Bin()
        if self.bin:
            bin_cell.update(self.position[0] + ((len(self.cells[0]) - 1) * 20 * self.scale) + 2 * self.scale,
                            self.position[1] + (len(self.cells) * 20 * self.scale) + 16 * self.scale, self.scale, self.stack_limit, inventory_id, inventory_list, cursor)

        # search shading and highlighting red (graphics not fully implemented but just the POC here)
        if text != "":
            for i, row in enumerate(self.cells):
                for j, cell in enumerate(row):
                    if cell.item is not None and text in cell.item.name:
                        pygame.draw.rect(
                            win, (255, 0, 0), (self.position[0] + (j * 20 * self.scale) + 2 * self.scale,
                                               self.position[1] + (i * 20 * self.scale) + 16 * self.scale, 4 * self.scale, 4 * self.scale))
                    else:
                        shade = pygame.Surface((16 * self.scale, 16 * self.scale))
                        shade.set_alpha(128)
                        shade.fill((0, 0, 0))
                        win.blit(shade,
                                 (self.position[0] + (j * 20 * self.scale) + 2 * self.scale + 2 * self.scale, self.position[1] + (i * 20 * self.scale) + 16 * self.scale + 2 * self.scale))


class Inventory_Engine():
    def __init__(self, inventory_list) -> None:
        self.inventory_list = inventory_list

    def update(self, cursor, text) -> None:
        for i, inventory in enumerate(self.inventory_list):
            inventory.update(i, self.inventory_list, cursor, text)

# Search bar class *Xini

class Search_Bar():
    def __init__(self, width, x, y, scale=3) -> None:
        self.width = width
        self.position = (x, y)
        self.scale = scale
        self.clicked = 0
        self.blink = 0
        self.text_pos = 0
        self.text = ""
    
    def draw(self, selected):
        images = [pygame.Surface] * self.width
        match selected:
            case 1:
                for i in range(self.width):
                    if i == 0:
                        images[i] = pygame.transform.scale(SEARCH_BAR_SELECTED["left"], (20 * self.scale, 20 * self.scale))
                    elif i == self.width - 1:
                        images[i] = pygame.transform.scale(SEARCH_BAR_SELECTED["right"], (20 * self.scale, 20 * self.scale))
                    else:
                        images[i] = pygame.transform.scale(SEARCH_BAR_SELECTED["middle"], (20 * self.scale, 20 * self.scale))
            case 0:
                for i in range(self.width):
                    if i == 0:
                        images[i] = pygame.transform.scale(SEARCH_BAR["left"], (20 * self.scale, 20 * self.scale))
                    elif i == self.width - 1:
                        images[i] = pygame.transform.scale(SEARCH_BAR["right"], (20 * self.scale, 20 * self.scale))
                    else:
                        images[i] = pygame.transform.scale(SEARCH_BAR["middle"], (20 * self.scale, 20 * self.scale))
        return images
    
    def update(self, cursor) -> None:
        pygame.draw.rect(
            win, (31, 31, 31), (*self.position, self.width * 20 * self.scale + 4 * self.scale, 20 * self.scale + 18 * self.scale))

        search_bar_title = FONT["24"].render(
            "Search:", 1, (255, 255, 255))
        win.blit(search_bar_title, (self.position[0] + 4 * self.scale, self.position[1] + 4 * self.scale))

        search_box = pygame.Rect(
            self.position[0], self.position[1] + 16 * self.scale, self.width * 20 * self.scale, 20 * self.scale)

        if cursor.box.colliderect(search_box):
            images = self.draw(1)
        else:
            images = self.draw(0)

        for i in range(len(images)):
            win.blit(images[i], (self.position[0] + (i * 20 * self.scale) + 2 * self.scale, self.position[1] + 16 * self.scale))
        
        text = FONT["24"].render(
            self.text, 1, (255, 255, 255))
        win.blit(text, (self.position[0] + 4 * self.scale + 3 * self.scale, self.position[1] + 16 * self.scale + 4 * self.scale, 4 * self.scale, self.scale))

        if self.blink == 60:
            self.blink = 0
        elif self.blink > 30:
            self.blink += 1
        elif self.clicked == 1:
            pygame.draw.rect(
                win, (255, 255, 255), (self.position[0] + 4 * self.scale + 3 * self.scale + self.text_pos * 4 * self.scale, self.position[1] + 16 * self.scale + 13 * self.scale, 4 * self.scale, self.scale))
            self.blink += 1

        if cursor.pressed is None:
            self.clicked = 0
        elif cursor.box.colliderect(search_box) and cursor.pressed[0]:
            self.clicked = 1
        elif cursor.pressed[0]:
            self.clicked = 0
    
    def handle_event(self, event) -> None:
        if self.clicked == 1:
            if event.key == pygame.K_BACKSPACE:
                if self.text_pos > 0:
                    self.text_pos -= 1
                    self.text = self.text[:-1]
            else:
                self.text_pos += 1
                self.text += event.unicode

def main():
    inventory_list = [
        Inventory("Large", 6, 10, 50, 100, 3, 99, bin_active=True),
        Inventory("3x3", 3, 3, 700, 100, 3, 99),
        Inventory("Small", 1, 3, 700, 400, 3, 99),
        Inventory("Tall", 6, 3, 930, 100, 3, 99),
        Inventory("Tall2", 6, 2, 1170, 100, 3, 99)
    ]
    inventory_engine = Inventory_Engine(inventory_list)

    search_bar = Search_Bar(21, 50, 600, 3)                         # Search bar width, x, y, scale

    cursor = Cursor()

    run = True
    while run:
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():  # Test to see if the usr quits the game, if so, quit
            if event.type == pygame.QUIT:
                print("Program closed by user.")
                pygame.quit()
                os._exit(1)
            # handling event of searching
            if event.type == pygame.KEYDOWN:
                search_bar.handle_event(event)

        pygame.event.get()
        keys = pygame.key.get_pressed()                             # Should only react to c and w when not selected on Search Bar
        if keys[K_c] and search_bar.clicked == 0:
            inventory_engine.inventory_list[0].add_item(
                Item(random.choice(list(ITEMS.keys())), 1))
        if keys[K_w] and search_bar.clicked == 0:
            inventory_engine.inventory_list[0].add_item(
                Weapon(random.choice(list(WEAPONS.keys())), 1))
        win.fill((0, 0, 0))
        search_bar.update(cursor)                                   # Search bar's update function here
        inventory_engine.update(cursor, search_bar.text)            # Added new parameters to accomodate search
        cursor.update(keys, search_bar.position, search_bar.scale)  # Added new parameters to accomodate search

        clock.tick(FPS)  # Pauses to keep track with FPS constant
        pygame.display.update()


if __name__ == "__main__":
    main()
