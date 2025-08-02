import pygame
import random
from typing import Literal
from bullet import Bullet
from sprite_manager import SpriteManager, SpriteKey
from config import Config, ConfigKey


class Enemy(pygame.sprite.Sprite):
    def __init__(
        self,
        position: pygame.Vector2,
        color: str,
        size: tuple[int, int],
        speed: float,
        point: float,
        sprites: list[pygame.Surface],
    ) -> None:
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
        if self.animation_interval < 0:
            self.curr_sprite_index += 1
            self.animation_interval = 0.5
        if self.curr_sprite_index > self.max_sprites_index:
            self.curr_sprite_index = 0
        self.animation_interval -= delta_time


class OctupusEnemy(Enemy):
    def __init__(
        self,
        position: pygame.Vector2,
        color: str,
        size: tuple[int, int],
        speed: float,
        sprites: list[pygame.Surface],
        point=10,
    ) -> None:
        super().__init__(position, color, size, speed, point, sprites)


class CrabEnemy(Enemy):
    def __init__(
        self,
        position: pygame.Vector2,
        color: str,
        size: tuple[int, int],
        speed: float,
        sprites: list[pygame.Surface],
        point=20,
    ) -> None:
        super().__init__(position, color, size, speed, point, sprites)


class SquidEnemy(Enemy):
    def __init__(
        self,
        position: pygame.Vector2,
        color: str,
        size: tuple[int, int],
        speed: float,
        sprites: list[pygame.Surface],
        point=30,
    ) -> None:
        super().__init__(position, color, size, speed, point, sprites)


STEP_INTERVAL = 0.5
MIN_FIRING_COOLDOWN_TIME = 2
MAX_FIRING_COOLDOWN_TIME = 5
ENEMY_MAX_BULLET = 3


class EnemyFormation:
    def __init__(
        self,
        left_limit: float,
        right_limit: float,
        sprite_manager: SpriteManager,
        config: Config | None = None,
        move_down_distance: float | None = None,
        enemy_col: int | None = None,
        enemy_row: int | None = None,
        enemy_formation_gap: float | None = None,
        enemy_size: tuple[float, float] | None = None,
        enemy_start_pos: pygame.Vector2 | None = None,
        enemy_speed: float | None = None,
    ) -> None:
        # Use config defaults if parameters are None
        if config is None:
            config = Config()

        formation_config = config.enemy_formation_config()

        self.move_down_distance = (
            move_down_distance
            if move_down_distance is not None
            else formation_config[ConfigKey.ENEMY_FORMATION_MOVE_DOWN_DISTANCE]
        )
        enemy_col = (
            enemy_col
            if enemy_col is not None
            else formation_config[ConfigKey.ENEMY_COL]
        )
        enemy_row = (
            enemy_row
            if enemy_row is not None
            else formation_config[ConfigKey.ENEMY_ROW]
        )
        enemy_formation_gap = (
            enemy_formation_gap
            if enemy_formation_gap is not None
            else formation_config[ConfigKey.ENEMY_FORMATION_GAP]
        )
        enemy_size = (
            enemy_size
            if enemy_size is not None
            else (
                formation_config[ConfigKey.ENEMY_SIZE_WIDTH],
                formation_config[ConfigKey.ENEMY_SIZE_HEIGHT],
            )
        )
        enemy_start_pos = (
            enemy_start_pos if enemy_start_pos is not None else pygame.Vector2(50, 50)
        )
        enemy_speed = (
            enemy_speed
            if enemy_speed is not None
            else formation_config[ConfigKey.ENEMY_SPEED]
        )

        self.horizontal_direction = 1
        self.left_limit = left_limit
        self.right_limit = right_limit
        self.enemies: list[list[Enemy]] = [
            [None] * enemy_row for _ in range(0, enemy_col)
        ]
        self.current_step = STEP_INTERVAL
        self.enemy_firing_cooldown: float = random.randint(
            MIN_FIRING_COOLDOWN_TIME, MAX_FIRING_COOLDOWN_TIME
        )
        self.can_move = True

        self.bullets: list[Bullet] = []

        octopus_sprites = sprite_manager.get_sprites(SpriteKey.OCTOPUS_ENEMY)
        crab_sprites = sprite_manager.get_sprites(SpriteKey.CRAB_ENEMY)
        squid_sprites = sprite_manager.get_sprites(SpriteKey.SQUID_ENEMY)

        for col in range(0, enemy_col):
            horizontal_offset = col * enemy_formation_gap + col * enemy_size[0]
            for row in range(0, enemy_row):
                vertical_offset = row * enemy_formation_gap + row * enemy_size[1]
                x_pos = enemy_start_pos.x + horizontal_offset
                y_pos = enemy_start_pos.y - vertical_offset
                if row == 0 or row == 1:
                    self.enemies[col][row] = OctupusEnemy(
                        pygame.Vector2(x_pos, y_pos),
                        color="orange",
                        size=enemy_size,
                        speed=enemy_speed,
                        sprites=octopus_sprites,
                    )
                elif row == 2 or row == 3:
                    self.enemies[col][row] = CrabEnemy(
                        pygame.Vector2(x_pos, y_pos),
                        color="yellow",
                        size=enemy_size,
                        speed=enemy_speed,
                        sprites=crab_sprites,
                    )
                else:
                    self.enemies[col][row] = SquidEnemy(
                        pygame.Vector2(x_pos, y_pos),
                        color="pink",
                        size=enemy_size,
                        speed=enemy_speed,
                        sprites=squid_sprites,
                    )

    def auto_shoot(self, delta_time: float, sprites: list[pygame.Surface]):
        for col in self.enemies:
            for i in range(0, len(col)):
                enemy = col[i]
                if (
                    i == 0
                    and (len(self.bullets) < ENEMY_MAX_BULLET or len(self.bullets) == 0)
                    and self.enemy_firing_cooldown < 0
                ):
                    can_shoot = bool(random.randint(0, 1))
                    if can_shoot:
                        bullet_pos = pygame.Vector2(
                            x=enemy.rect.x + enemy.size[0] / 2, y=enemy.rect.y
                        )
                        self.bullets.append(
                            Bullet(position=bullet_pos, speed=100, sprites=sprites)
                        )
                        self.enemy_firing_cooldown = random.randint(
                            MIN_FIRING_COOLDOWN_TIME, MAX_FIRING_COOLDOWN_TIME
                        )

        self.enemy_firing_cooldown -= delta_time

    def move_by_step(self, delta_time=float):
        if self.current_step > 0:
            self.current_step -= delta_time
            return

        for row in self.enemies:
            for enemy in row:
                enemy.move_horizontally(enemy.size[0] * self.horizontal_direction)

        if self.is_past_horizontal_bound():
            self.reverse_direction()
            self.move_down()
        self.current_step = STEP_INTERVAL

    def move_by_delta_time(self, delta_time: float):
        for row in self.enemies:
            for enemy in row:
                enemy.move_horizontally(
                    enemy.speed * delta_time * self.horizontal_direction
                )

        if self.is_past_horizontal_bound():
            self.reverse_direction()
            self.move_down()

    def auto_move(self, delta_time: float = 0, mode: Literal["step", "delta"] = "step"):
        if self.can_move == False:
            return
        if mode == "step":
            self.move_by_step(delta_time=delta_time)
        else:
            self.move_by_delta_time(delta_time)

    def move_down(self) -> None:
        for row in self.enemies:
            for enemy in row:
                enemy.move_vertically(distance=self.move_down_distance)

    def reverse_direction(self) -> None:
        self.horizontal_direction *= -1

    def is_past_horizontal_bound(self) -> bool:
        enemy_list = list(map((lambda enemy: enemy.rect.x), sum(self.enemies, [])))
        if len(enemy_list) == 0:
            return False
        pos_list = enemy_list
        curr_left = min(pos_list)
        curr_right = max(pos_list)
        if curr_left <= self.left_limit:
            return True
        if curr_right >= self.right_limit:
            return True
        return False

    def collide_player(self, player):
        for row in self.enemies:
            for enemy in row:
                if enemy.rect.colliderect(player):
                    return True
        return False

    def stop_moving(self):
        self.can_move = False

    def resume_moving(self):
        self.can_move = True

    def render(self, surface: pygame.Surface, delta_time: float):
        for col in self.enemies:
            for enemy in col:
                enemy.render(surface, delta_time=delta_time)
