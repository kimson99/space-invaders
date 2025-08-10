import pygame
from config import Config, ConfigKey


class Barrier(pygame.sprite.Sprite):
    def __init__(
        self,
        sprites: list[pygame.Surface],
        damaged_sprite: pygame.Surface,
        position: tuple[(int, int)] = (0, 0),
    ):
        pygame.sprite.Sprite.__init__(self)
        config = Config()
        barrier_config = config.barrier_config()

        self.size = (
            barrier_config[ConfigKey.BARRIER_WIDTH],
            barrier_config[ConfigKey.BARRIER_HEIGHT],
        )
        self.sprites = [pygame.transform.scale(sprite, self.size) for sprite in sprites]
        # Manually set the color key to (0,0,0) due to (0,0) of this sprite not being black
        self.damaged_sprite = damaged_sprite.copy()
        self.damaged_sprite.set_colorkey((0, 0, 0))
        self.damaged_sprite = pygame.transform.scale(
            self.damaged_sprite,
            (
                barrier_config[ConfigKey.BARRIER_DAMAGED_WIDTH],
                barrier_config[ConfigKey.BARRIER_DAMAGED_HEIGHT],
            ),
        )
        self.curr_sprite_index = 0
        self.rect = self.sprites[self.curr_sprite_index].get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.mask = pygame.mask.from_surface(self.sprites[self.curr_sprite_index])

    def handle_damage(self, collide_point: tuple[int, int]):
        sprite = self.sprites[self.curr_sprite_index]
        x = collide_point[0] - self.damaged_sprite.get_width() // 2
        y = collide_point[1] - self.damaged_sprite.get_width() // 2
        # Draw the damage
        sprite.blit(self.damaged_sprite, (x, y), special_flags=pygame.BLEND_RGBA_SUB)
        # Update the mask to new damaged state
        self.mask = pygame.mask.from_surface(sprite)

    def render(self, surface: pygame.Surface):
        surface.blit(
            self.sprites[self.curr_sprite_index],
            self.rect,
        )

        # DEBUG
        # Damaged sprite
        # surface.blit(
        #     pygame.mask.from_surface(self.damaged_sprite).to_surface(

        #     ),
        #     (200, 50),
        # )

        # Mask
        # surface.blit(
        #     self.mask.to_surface(setcolor=(255, 0, 0, 255)),
        #     self.rect,
        # )
