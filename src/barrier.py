import pygame
from config import Config, ConfigKey


class Barrier(pygame.sprite):
    def __init__(
        self,
        sprites: list[pygame.Surface],
    ):
        config = Config()
        barrier_config = config.barrier_config

        self.size = (
            barrier_config[ConfigKey.BARRIER_WIDTH],
            barrier_config[ConfigKey.BARRIER_HEIGHT],
        )
        self.sprites = [pygame.transform.scale(sprite, self.size) for sprite in sprites]
        self.curr_sprite_index = 0
        self.mask = pygame.mask.from_surface(self.sprites[self.curr_sprite_index])


    def render(self, surface: pygame.Surface):
        surface.blit(
            self.sprites[self.curr_sprite_index],
            self.mask,
        )