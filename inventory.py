import pygame as py
from settings import screen_width, screen_height
from object import Object

DEFAULT_SURFACE = py.Surface((180, 30))
DEFAULT_SURFACE_POS = (520, 700)


class Inventory:
    def __init__(self):
        py.font.init()
        self.font = py.font.SysFont('Comic Sans MS', 20)
        self.surface = DEFAULT_SURFACE
        self.border = py.image.load('D:/Programs/Python/Platformer/Images/border.png')
        self.slots = {}
        self.things = []
        self.object_images = []
        self.count = 1
        self.text = None
        self.pos = 0
        self.surface_pos = DEFAULT_SURFACE_POS
        self.selected_item = None

    def add(self, object):

        if object.type in self.slots:
            self.slots[object.type]["count"] += 1
            self.slots[object.type]["objects"].append(object)
            self.text = self.font.render(str(self.slots[object.type]["count"]), False, (0, 0, 255))

        else:
            image = object.image
            self.object_images.append(image)
            pos = len(self.slots.keys()) * object.rect.size[0]
            self.slots.update({object.type: {"count": self.count, "pos": pos, "image": image, "objects": [object]}})

    def throw(self, pos):
        print(self.slots)
        print(f"Throw!: {self.selected_item} at: {pos}")
        if not self.slots[self.selected_item]["count"] <= 0:
            self.slots[self.selected_item]["count"] -= 1
            self.slots[self.selected_item]["objects"][self.slots[self.selected_item]["count"] - 1].rect.x, self.slots[self.selected_item]["objects"][self.slots[self.selected_item]["count"] - 1].rect.y = pos
            return pos, self.slots[self.selected_item]["objects"][self.slots[self.selected_item]["count"] - 1]

    def draw(self, surface):

        self.surface.fill((0, 0, 0))
        for object_type in self.slots.keys():
            self.text = self.font.render(str(self.slots[object_type]["count"]), False, (0, 0, 255))
            self.surface.blit(self.slots[object_type]["image"], (self.slots[object_type]["pos"], 0))
            self.surface.blit(self.text, (self.slots[object_type]["pos"], 0))
        self.surface.blit(self.border, (self.pos, 0))
        surface.blit(self.surface, self.surface_pos)

    def open(self, surface):
        self.surface_pos = (520, 400)
        self.surface = py.Surface((180, 300))

    def process_open(self, is_open, surface):
        if is_open:
            self.open(surface)
        else:
            self.surface = DEFAULT_SURFACE
            self.surface_pos = DEFAULT_SURFACE_POS

    def select(self, pos):
        for item in self.slots.keys():
            self.pos = pos * self.slots[item]["objects"][0].rect.width
            if self.pos == self.slots[item]["pos"]:
                self.selected_item = item

    def update(self, is_open, pos, surface):
        self.select(pos)
        self.process_open(is_open, surface)







