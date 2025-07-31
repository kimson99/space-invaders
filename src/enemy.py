import pygame
import random
from typing import Literal
from bullet import Bullet
from sprite_manager import SpriteManager

class Enemy(pygame.sprite.Sprite):
  def __init__(self, position: pygame.Vector2, color: str, size: tuple[int, int], speed: float, point: float, sprites: list[pygame.Surface]) -> None:
    pygame.sprite.Sprite.__init__(self)
    self.position = position
    self.color = color
    self.size = size
    self.speed = speed
    self.point = point

    self.sprites = [pygame.transform.scale(sprite, size) for sprite in sprites]
    self.max_sprites_index = len(self.sprites) - 1
    self.curr_sprite_index = 0
    self.rect = self.sprites[self.curr_sprite_index].get_rect()
    self.rect.x = position.x
    self.rect.y = position.y
    
    self.animation_interval = 0.5

  def move_horizontally(self, distance: float):
    self.rect.x += distance
    
  def move_vertically(self, distance: float):
    self.rect.y += distance

  def render(self, surface: pygame.Surface, delta_time: float):
    surface.blit(self.sprites[self.curr_sprite_index], self.rect)
    if (self.animation_interval < 0):
      self.curr_sprite_index +=1
      self.animation_interval = 0.5
    if (self.curr_sprite_index > self.max_sprites_index):
       self.curr_sprite_index = 0
    self.animation_interval -= delta_time

class OctupusEnemy(Enemy):
  def __init__(self, position: pygame.Vector2, color: str, size: tuple[int, int], speed: float, sprites: list[pygame.Surface], point = 10, ) -> None:
    super().__init__(position, color, size, speed, point, sprites)

class CrabEnemy(Enemy):
  def __init__(self, position: pygame.Vector2, color: str, size: tuple[int, int], speed: float, sprites: list[pygame.Surface], point = 20) -> None:
    super().__init__(position, color, size, speed, point, sprites)

class SquidEnemy(Enemy):
  def __init__(self, position: pygame.Vector2, color: str, size: tuple[int, int], speed: float, sprites: list[pygame.Surface],point = 30) -> None:
    super().__init__(position, color, size, speed, point, sprites)


STEP_INTERVAL = 0.5
MIN_FIRING_COOLDOWN_TIME = 2
MAX_FIRING_COOLDOWN_TIME = 5
ENEMY_MAX_BULLET = 3

class EnemyFormation:
  def __init__(self, 
               left_limit: float, 
               right_limit: float, 
               move_down_distance: float, 
               enemies: list[list[Enemy]], 
               sprite_manager: SpriteManager,
               enemy_col: int = 11, enemy_row: int = 5, enemy_formation_gap: float = 20, enemy_size: tuple[float, float] = (40, 20), enemy_start_pos: pygame.Vector2 = pygame.Vector2(50, 50), enemy_speed: float = 10) -> None:
    self.horizontal_direction = 1
    self.left_limit = left_limit
    self.right_limit = right_limit
    self.move_down_distance = move_down_distance
    self.enemies = enemies
    self.current_step = STEP_INTERVAL
    self.enemy_firing_cooldown: float = random.randint(MIN_FIRING_COOLDOWN_TIME, MAX_FIRING_COOLDOWN_TIME)

    self.bullets: list[Bullet] = []
  
    
    octopus_sprites = sprite_manager.get_sprites('octopus_enemy')
    crab_sprites = sprite_manager.get_sprites('crab_enemy')
    squid_sprites = sprite_manager.get_sprites('squid_enemy')

    for col in range(0, enemy_col):
      horizontal_offset = col * enemy_formation_gap + col * enemy_size[0]
      for row in range(0, enemy_row):
          vertical_offset = row * enemy_formation_gap + row * enemy_size[1]
          x_pos = enemy_start_pos.x + horizontal_offset
          y_pos = enemy_start_pos.y - vertical_offset
          if row == 0 or row == 1:
            enemies[col][row] = OctupusEnemy(pygame.Vector2(x_pos, y_pos), color='orange', size= enemy_size, speed=enemy_speed, sprites=octopus_sprites)
          elif row == 2 or row == 3:
            enemies[col][row] = CrabEnemy(pygame.Vector2(x_pos, y_pos), color='yellow', size= enemy_size, speed=enemy_speed, sprites=crab_sprites)
          else:
            enemies[col][row] = SquidEnemy(pygame.Vector2(x_pos, y_pos), color='pink', size= enemy_size, speed=enemy_speed,sprites=squid_sprites)

  def auto_shoot(self, delta_time: float, sprites: list[pygame.Surface]):
    for col in self.enemies:
        for i in range(0, len(col)):
            enemy = col[i]
            if i == 0 and (len(self.bullets) < ENEMY_MAX_BULLET or len(self.bullets) == 0) and self.enemy_firing_cooldown < 0:
                can_shoot = bool(random.randint(0, 1))
                if (can_shoot):
                    bullet_pos = pygame.Vector2(x=enemy.rect.x + enemy.size[0] / 2, y=enemy.rect.y)
                    self.bullets.append(Bullet(position=bullet_pos, speed=100, sprites=sprites))
                    self.enemy_firing_cooldown = random.randint(MIN_FIRING_COOLDOWN_TIME, MAX_FIRING_COOLDOWN_TIME)

    self.enemy_firing_cooldown -= delta_time

  def move_by_step(self,delta_time=float):
    if self.current_step > 0:
      self.current_step -= delta_time
      return
    
    for row in self.enemies:
      for enemy in row:
          enemy.move_horizontally(enemy.size[0] * self.horizontal_direction)

    if (self.is_past_horizontal_bound()):
      self.reverse_direction()
      self.move_down()
    self.current_step = STEP_INTERVAL
 

  def move_by_delta_time(self, delta_time: float):
    for row in self.enemies:
      for enemy in row:
        enemy.move_horizontally(enemy.speed * delta_time * self.horizontal_direction)

    if (self.is_past_horizontal_bound()):
      self.reverse_direction()
      self.move_down()
       
  def auto_move(self, delta_time: float = 0, mode: Literal["step", "delta"] = "step"):
    if (mode == "step"):
      self.move_by_step(delta_time=delta_time)
    else:
      self.move_by_delta_time(delta_time)
    

  def move_down(self) -> None:
    for row in self.enemies:
      for enemy in row:
          enemy.move_vertically(distance=self.move_down_distance)

  def reverse_direction(self) -> None:
      self.horizontal_direction *=-1  
  
  def is_past_horizontal_bound(self) -> bool:
    enemy_list = list(map((lambda enemy: enemy.rect.x), sum(self.enemies,[])))
    if (len(enemy_list) == 0):
      return False
    pos_list = enemy_list
    curr_left = min(pos_list)
    curr_right = max(pos_list)
    if (curr_left <= self.left_limit):
        return True
    if (curr_right >= self.right_limit):
        return True
    return False
  
  def collide_player(self, player):
    for row in self.enemies:
      for enemy in row:
          if (enemy.rect.colliderect(player)):
            return True
    return False
  
  def render(self, surface: pygame.Surface, delta_time: float):
    for col in self.enemies:
        for enemy in col:
            enemy.render(surface, delta_time=delta_time)
