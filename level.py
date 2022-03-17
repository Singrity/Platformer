import pygame
from tiles import Tile
from settings import *
from player import Player
from object import Object


class Level:

    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.level_data = level_data
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.objects = pygame.sprite.Group()
        self.setup_level(level_data)

        self.world_sift_x = 0
        self.world_sift_y = 0

        self.current_x = 0
        self.current_y = 0

    def setup_level(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = tile_size * col_index
                y = tile_size * row_index
                if cell == 'X':
                    self.tiles.add(Tile((x, y), tile_size))
                if cell == 'P':
                    self.player.add(Player((x, y)))
                if cell == 'O':
                    self.objects.add(Object((x, y), 30, "oil"))
                if cell == 'B':
                    self.objects.add(Object((x, y), 30, "block"))
                # if cell == 'C':
                #     self.objects.add(Object((x, y), 30, "coblestone"))

    def scroll(self, time):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        player_y = player.rect.centery
        direction_y = player.direction.y

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_sift_x = 1
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_sift_x = -1
            player.speed = 0
        else:
            self.world_sift_x = 0
            player.speed = 1

        # if player_y < screen_height / 6 and direction_y < 0:
        #     self.world_sift_y = 1
        # elif player_y > screen_height - (screen_height / 6) and direction_y > 0:
        #     self.world_sift_y = -1
        # else:
        #     self.world_sift_y = 0

    def horizontal_movement_collision(self, time):
        player = self.player.sprite
        player.rect.x += player.direction.x * time * player.speed

        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = tile.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = tile.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        for object in self.objects.sprites():
            if object.rect.colliderect(player.rect):
                player.earn(object)
                self.objects.remove(object)

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collition(self, time):
        player = self.player.sprite

        player.apply_gravity(time)

        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    player.direction.y = 0
                    player.rect.top = tile.rect.bottom
                    player.on_ceiling = True
                elif player.direction.y > 0:
                    player.direction.y = 0
                    player.rect.bottom = tile.rect.top
                    player.is_flying = False
                    player.on_ground = True

            if player.rect.top > level_height:
                player.remove(self.player)
                self.reload_level()

        if player.on_ground and player.is_flying or player.direction.y > 1:
            player.on_ground = False

        if player.on_ceiling and not player.is_flying:
            player.on_ceiling = False

        return player.is_flying, player.on_ground

    def reload_level(self):
        for row_index, row in enumerate(self.level_data):
            for col_index, cell in enumerate(row):
                x = tile_size * col_index
                y = tile_size * row_index
                if cell == 'P':
                    self.player.add(Player((x, y)))
                if cell == 'O':
                    self.objects.add(Object((x, y), 30, "oil"))
                if cell == 'B':
                    self.objects.add(Object((x, y), 30, "block"))
                if cell == 'C':
                    self.objects.add(Object((x, y), 30, "coblestone"))

    def process_inventory(self, is_throw, screen):
        player = self.player.sprite
        if is_throw:
            if not player.is_throwing:
                object_data = player.throw(screen)
                self.objects.add(object_data[1])
                player.is_throwing = True
                print(self.objects)
        else:
            player.is_throwing = False


    def run(self, p_moving_right, p_moving_left, jump, time, open_inventory, mouse_pos, is_throw):
        self.scroll(time)
        self.tiles.update(self.world_sift_x, self.world_sift_y, time)
        self.tiles.draw(self.display_surface)
        self.objects.update(self.world_sift_x, time)
        self.objects.draw(self.display_surface)
        self.player.update(p_moving_right, p_moving_left, jump, time, self.display_surface, open_inventory, mouse_pos)
        self.horizontal_movement_collision(time)
        flags = self.vertical_movement_collition(time)
        self.process_inventory(is_throw, self.display_surface)
        self.player.draw(self.display_surface)

        return flags

