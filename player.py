import pygame
from support import import_folder
from inventory import Inventory


class Player(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()

        self.inventory = Inventory()

        self.animations = {}

        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.08
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # dust particles
        self.dust_run_particles = import_folder('None')
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.08
        #self.display_surface = surface

        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 1
        self.speed_y = 0
        self.gravity = 0.1
        self.jump_speed = -2.1

        # player status
        self.is_flying = False
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        self.is_throwing = False

    def import_character_assets(self):
        character_path = 'D:/Programs/Python/Platformer/Images/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder('D:/Programs/Python/Platformer/Images/dust_run')

    def animate(self, time):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index > len(animation):
            self.frame_index = 0
        else:
            image = animation[int(self.frame_index)]

            if self.facing_right:
                self.image = image
            else:
                flipped_image = pygame.transform.flip(image, True, False)
                self.image = flipped_image

        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

    def run_dust_animation(self, surface):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                pos = self.rect.bottomleft - pygame.Vector2(18, 18)
                surface.blit(dust_particle, pos)

    def apply_gravity(self, time):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y * time

    def move(self, moving_right, moving_left, jump):
        if moving_right:
            self.direction.x = 1
            self.facing_right = True
        elif moving_left:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0
        if jump and not self.is_flying:
            self.jump()

    def jump(self):
        self.direction.y = self.jump_speed
        self.is_flying = True

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def earn(self, object):
        self.inventory.add(object)

    def throw(self, screen):
        if not self.is_throwing:
            object_data = self.inventory.throw((self.rect.centerx + self.rect.width + 40, self.rect.centery))
        return object_data

    def update(self, moving_right, moving_left, jump, time, surface, open_inventory, pos):
        self.move(moving_right, moving_left, jump)
        self.get_status()
        self.animate(time)
        self.run_dust_animation(surface)
        self.inventory.draw(surface)
        self.inventory.update(open_inventory, pos, surface)
        #pygame.draw.rect(surface, (255, 0, 0), self.rect, 1)





