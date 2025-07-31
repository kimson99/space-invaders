import pygame
from bullet import Bullet

class Player(pygame.sprite.Sprite):
  def __init__(self,
               sprites: list[pygame.Surface], 
               position = None, 
               speed = 200, 
               size: tuple[int, int] = (40, 20), 
               lives: float = 3):
    pygame.sprite.Sprite.__init__(self)
    self.position = position if position else pygame.Vector2(0, 0)
    self.speed = speed
    self.size = size
   
    self.lives = lives
    self.bullets: list[Bullet] = []
    self.score = 0
    self.death_timer_ms = 2000
    self.is_dead = False

    self.sprites = [pygame.transform.scale(sprite, size) for sprite in sprites]
    self.max_sprites_index = len(self.sprites) - 1
    self.curr_sprite_index = 0
    self.death_sprite = self.sprites[1]
    self.rect = self.sprites[self.curr_sprite_index].get_rect()
    self.rect.x = position.x
    self.rect.y = position.y
  
  def move_left(self, delta_time: float, left_limit: float):
    self.rect.x = max(self.rect.x - self.speed * delta_time, left_limit)

  def move_right(self, delta_time: float, right_limit: float):
    self.rect.x = min(self.rect.x + self.speed * delta_time, right_limit)

  def shoot(self, bullet: Bullet):
    # One bullet at a time
    if (len(self.bullets) > 0):
      return
    
    self.bullets.append(bullet)

  def lose_life(self):
    self.lives -= 1
    self.is_dead = True

  def revive(self):
    self.is_dead = False

  def render(self, surface: pygame.Surface):
     surface.blit(self.death_sprite if self.is_dead else self.sprites[self.curr_sprite_index], self.rect)