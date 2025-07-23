import pygame

class Bullet:
  def __init__(self, position: pygame.Vector2, color: str, size: tuple[int, int] = (10, 15), speed = 100):
    self.position = position
    self.color = color
    self.size = size
    self.speed = speed
    self.rect = pygame.rect.Rect(self.position, self.size)

  def render(self, surface):
    pygame.draw.rect(surface, color=self.color, rect=self.rect)