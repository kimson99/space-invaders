import pygame

class Enemy:
  def __init__(self, position: pygame.Vector2, color: str, size: tuple[int, int], speed: float, point: float) -> None:
    self.position = position
    self.color = color
    self.size = size
    self.speed = speed
    self.point = point
    self.rect = pygame.rect.Rect(self.position, self.size)

  def move_horizontally(self, distance: float):
    self.rect.x += distance
    
  def move_vertically(self, distance: float):
    self.rect.y += distance

  def render(self, surface):
    pygame.draw.rect(surface, color=self.color, rect=self.rect)

class OctupusEnemy(Enemy):
  def __init__(self, position: pygame.Vector2, color: str, size: tuple[int, int], speed: float, point = 10) -> None:
    super().__init__(position, color, size, speed, point)

class CrabEnemy(Enemy):
  def __init__(self, position: pygame.Vector2, color: str, size: tuple[int, int], speed: float, point = 20) -> None:
    super().__init__(position, color, size, speed, point)

class SquidEnemy(Enemy):
  def __init__(self, position: pygame.Vector2, color: str, size: tuple[int, int], speed: float, point = 30) -> None:
    super().__init__(position, color, size, speed, point)


STEP_INTERVAL = 0.5
class EnemyFormation:
  def __init__(self, left_limit: float, right_limit: float, move_down_distance: float, enemies: list[list[Enemy]]) -> None:
    self.horizontal_direction = 1
    self.left_limit = left_limit
    self.right_limit = right_limit
    self.move_down_distance = move_down_distance
    self.enemies = enemies
    self.current_step = STEP_INTERVAL

  def move_by_step(self):
    if self.current_step > 0:
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
       
  def auto_move(self, delta_time: float | None = None):
    if (delta_time is None):
      self.move_by_step()
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
