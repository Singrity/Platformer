import pygame
from settings import *
from level import Level


class Game:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()

        self.test_level = Level(level_map, self.screen)

        self.is_running = False
        self.moving_right = False
        self.moving_left = False
        self.put = False
        self.jump = False
        self.is_open_inventory = False
        self.is_throw = False

        self.flags = []

        self.pos = 0

    def run(self):
        self.is_running = True
        while self.is_running:
            frame_time_ms = self.clock.tick(fps)
            frame_time_s = frame_time_ms / 1000.
            self.handle_events()
            self.draw()
            self.flags = self.test_level.run(self.moving_right, self.moving_left, self.jump, frame_time_ms, self.is_open_inventory, self.pos, self.is_throw)
            self.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
            self._handle_keydownevent(event)

            self._handle_keyupevent(event)

    def _handle_keydownevent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.stop()
            if event.key == pygame.K_RIGHT:
                self.moving_right = True
            elif event.key == pygame.K_LEFT:
                self.moving_left = True
            elif event.key == pygame.K_e:
                if self.is_open_inventory == True:
                    self.is_open_inventory = False
                else:
                    self.is_open_inventory = True

            elif not self.flags[0] and self.flags[1]:
                if event.key == pygame.K_SPACE:
                    self.jump = True

            self.process_inventory_keys(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.put = True

    def _handle_keyupevent(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                self.moving_right = False
            elif event.key == pygame.K_LEFT:
                self.moving_left = False
            elif self.flags[0] and not self.flags[1]:
                if event.key == pygame.K_SPACE:
                    self.jump = False
            elif event.key == pygame.K_g:
                self.is_throw = False
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.put = False

    def process_inventory_keys(self, event):
        if event.key == pygame.K_1:
            self.pos = 0
        elif event.key == pygame.K_2:
            self.pos = 1
        elif event.key == pygame.K_3:
            self.pos = 2
        elif event.key == pygame.K_4:
            self.pos = 3
        elif event.key == pygame.K_5:
            self.pos = 4
        elif event.key == pygame.K_6:
            self.pos = 5
        if not self.is_throw:
            if event.key == pygame.K_g:
                self.is_throw = True

    def draw(self):
        self.screen.fill((0, 0, 0))

    def stop(self):
        self.is_running = False
        pygame.quit()
        exit()

    def update(self):
        self.clock.tick(fps)
        pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()