import pygame
from enum import Enum

BulletSource = Enum("BulletSource", [('PLAYER', 1), ("ENEMY", 2)])
class Bullet:
  def __init__(self, position: pygame.Vector2, color: str, size: tuple[int, int] = (2, 15), speed = 50, source: BulletSource = BulletSource.PLAYER.value):
    self.position = position
    self.color = color
    self.size = size
    self.speed = speed
    self.rect = pygame.rect.Rect(self.position, self.size)
    self.source = source

  def is_out_of_bound(self, upper_bound: float, lower_bound: float):
    return self.rect.y < upper_bound or self.rect.y > lower_bound
      

  def move_vertically(self, distance):
    self.rect.y += distance

  def render(self, surface):
    pygame.draw.rect(surface, color=self.color, rect=self.rect)