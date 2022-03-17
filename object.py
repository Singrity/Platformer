import pygame
from support import import_folder


class Object(pygame.sprite.Sprite):
    def __init__(self, pos, size, type):
        super().__init__()
        self.type = type
        self.image = pygame.Surface((size, size))
        self.color = "white"

        self.rect = self.image.get_rect(topleft=pos)
        self.images = []
        self.import_assets()
        self.initialize_images(type)

    def import_assets(self):
        path = 'D:/Programs/Python/Platformer/Images/items'
        self.images = import_folder(path)

    def initialize_images(self, type):
        if type == 'oil':
            self.image = self.images[0]
        if type == 'block':
            self.image = self.images[1]
        if type == 'coblestone':
            self.color = 'gray'
            self.image.fill(self.color)

    def update(self, x_shift, time):
        self.rect.x += x_shift * time

    def redrow(self, pos):
        self.rect.x = pos




