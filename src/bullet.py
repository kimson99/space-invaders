import pygame
from enum import Enum

BulletSource = Enum("BulletSource", [('PLAYER', 1), ("ENEMY", 2)])
class Bullet(pygame.sprite.Sprite):
  def __init__(self, sprite: pygame.Surface, position: pygame.Vector2, color: str, size: tuple[int, int] = (5, 15), speed = 50, source: BulletSource = BulletSource.PLAYER.value):
    self.position = position
    self.color = color
    self.size = size
    self.speed = speed
    self.source = source

    self.sprite = pygame.transform.scale(sprite, size)
    self.rect = self.sprite.get_rect()
    self.rect.x = position.x
    self.rect.y = position.y

  def is_out_of_bound(self, upper_bound: float, lower_bound: float):
    return self.rect.y < upper_bound or self.rect.y > lower_bound
      

  def move_vertically(self, distance):
    self.rect.y += distance

  def render(self, surface):
    surface.blit(self.sprite, self.rect)