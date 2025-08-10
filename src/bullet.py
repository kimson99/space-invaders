import pygame
from enum import Enum

BulletSource = Enum("BulletSource", [("PLAYER", 1), ("ENEMY", 2)])


class Bullet(pygame.sprite.Sprite):
    def __init__(
        self,
        sprites: list[pygame.Surface],
        position: pygame.Vector2,
        size: tuple[int, int] = (5, 15),
        speed=50,
        source: BulletSource = BulletSource.PLAYER.value,
    ):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.size = size
        self.speed = speed
        self.source = source

        self.sprites = [pygame.transform.scale(sprite, size) for sprite in sprites]
        self.curr_sprite_index = 0
        self.rect = self.sprites[self.curr_sprite_index].get_rect()
        self.mask = pygame.mask.from_surface(self.sprites[self.curr_sprite_index])
        self.rect.x = position.x
        self.rect.y = position.y

    def is_out_of_bound(self, upper_bound: float, lower_bound: float):
        return self.rect.y < upper_bound or self.rect.y > lower_bound

    def move_vertically(self, distance):
        self.rect.y += distance

    def render(self, surface):
        surface.blit(self.sprites[self.curr_sprite_index], self.rect)
