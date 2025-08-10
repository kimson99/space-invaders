import pygame
from enum import Enum
from utils.spritesheet import SpriteSheet


class SpriteKey(Enum):
    PLAYER = "player"
    OCTOPUS_ENEMY = "octopus_enemy"
    CRAB_ENEMY = "crab_enemy"
    SQUID_ENEMY = "squid_enemy"
    PLAYER_BULLET = "player_bullet"
    ENEMY_BULLET = "enemy_bullet"
    BARRIER = "barrier"
    BARRIER_DAMAGED = "barrier-damaged"


class SpriteManager:
    def __init__(self, spritesheet_path) -> None:
        self.spritesheet = SpriteSheet(spritesheet_path)
        self.sprite_cords: dict[SpriteKey, list[tuple[int, int, int, int]]] = {
            SpriteKey.PLAYER: [(1, 49, 16, 8), (19, 49, 16, 8)],
            SpriteKey.OCTOPUS_ENEMY: [(1, 1, 16, 8), (1, 11, 16, 8)],
            SpriteKey.CRAB_ENEMY: [(19, 1, 16, 8), (19, 11, 16, 8)],
            SpriteKey.SQUID_ENEMY: [(37, 1, 16, 8), (37, 11, 16, 8)],
            SpriteKey.PLAYER_BULLET: [(20, 20, 5, 10)],
            SpriteKey.ENEMY_BULLET: [(1, 20, 5, 10)],
            SpriteKey.BARRIER: [(46, 31, 22, 16)],
            SpriteKey.BARRIER_DAMAGED: [(58, 49, 8, 8)],
        }

    def get_sprites(self, key: SpriteKey) -> list[pygame.Surface]:
        if key not in self.sprite_cords:
            raise Exception(f"Sprite cords not found for key {key}")

        cords = self.sprite_cords[key]

        images = self.spritesheet.images_at(cords, colorkey=int(-1))

        return images
