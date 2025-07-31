import pygame
from utils.spritesheet import SpriteSheet


class SpriteManager:
  def __init__(self, spritesheet_path) -> None:
    self.spritesheet = SpriteSheet(spritesheet_path)
    self.sprite_cords = {
      'player': [(1, 49, 16, 8)],
      
      'octopus_enemy': [(1, 1, 16, 8), (1, 11, 16, 8)],
      'crab_enemy': [(19, 1, 16, 8), (19, 11, 16, 8)],
      'squid_enemy': [(37, 1, 16, 8), (37, 11, 16, 8)],

      'player_bullet': [(20, 20, 5, 10)],
      'enemy_bullet': [(1, 20, 5, 10)]
    }

  def get_sprites(self, key: str) -> list[pygame.Surface]:
    if (key not in  self.sprite_cords):
      raise Exception(f"Sprite cords not found for key {key}")

    cords = self.sprite_cords[key]

    images = self.spritesheet.images_at(cords, colorkey=int(-1))

    return images