import pygame
from bullet import Bullet

class Player:
  def __init__(self, position = None, speed = 200, size: tuple[int, int] = (20, 40), lives: float = 3):
    self.position = position if position else pygame.Vector2(0, 0)
    self.speed = speed
    self.size = size
    self.rect = pygame.rect.Rect(self.position, self.size)
    self.lives = lives
    self.bullets: list[Bullet] = []
    self.score = 0
  
  def move_left(self, delta_time: float, left_limit: float):
    self.rect.x = max(self.rect.x - self.speed * delta_time, left_limit)

  def move_right(self, delta_time: float, right_limit: float):
    self.rect.x = min(self.rect.x + self.speed * delta_time, right_limit)

  def shoot(self):
    # One bullet at a time
    if (len(self.bullets) > 0):
      return
    
    bullet_pos = pygame.Vector2(x=self.rect.x + self.size[0] / 2, y=self.rect.y)
    self.bullets.append(Bullet(bullet_pos, color="white", speed=500))

  def lose_life(self):
    self.lives -= 1

  def render(self, surface):
    pygame.draw.rect(surface, color="red", rect=self.rect)