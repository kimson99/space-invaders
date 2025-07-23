import pygame

class Player:
  def __init__(self, position = None, speed = 200, size: tuple[int, int] = (20, 40)):
    self.position = position if position else pygame.Vector2(0, 0)
    self.speed = speed
    self.size = size
    self.rect = pygame.rect.Rect(self.position, self.size)
  
  def move_left(self, delta_time: float, left_limit: float):
    self.rect.x = max(self.rect.x - self.speed * delta_time, left_limit)

  def move_right(self, delta_time: float, right_limit: float):
    self.rect.x = min(self.rect.x + self.speed * delta_time, right_limit)

  def shoot(self):
      print("Shoot")

  def render(self, surface):
    pygame.draw.rect(surface, color="red", rect=self.rect)