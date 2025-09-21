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
        config: Config | None = None,
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

        # Use config for animation interval
        if config is None:
            config = Config()
        formation_config = config.enemy_formation_config()
        self.animation_interval = formation_config[ConfigKey.ENEMY_ANIMATION_INTERVAL]
        self.animation_interval_reset = formation_config[
            ConfigKey.ENEMY_ANIMATION_INTERVAL
        ]

    def move_horizontally(self, distance: float):
        self.rect.x += distance

    def move_vertically(self, distance: float):
        self.rect.y += distance

    def render(self, surface: pygame.Surface, delta_time: float):
        surface.blit(self.sprites[self.curr_sprite_index], self.rect)
        if self.animation_interval < 0:
            self.curr_sprite_index += 1
            self.animation_interval = self.animation_interval_reset
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
        config: Config | None = None,
    ) -> None:
        super().__init__(position, color, size, speed, point, sprites, config)


class CrabEnemy(Enemy):
    def __init__(
        self,
        position: pygame.Vector2,
        color: str,
        size: tuple[int, int],
        speed: float,
        sprites: list[pygame.Surface],
        point=20,
        config: Config | None = None,
    ) -> None:
        super().__init__(position, color, size, speed, point, sprites, config)


class SquidEnemy(Enemy):
    def __init__(
        self,
        position: pygame.Vector2,
        color: str,
        size: tuple[int, int],
        speed: float,
        sprites: list[pygame.Surface],
        point=30,
        config: Config | None = None,
    ) -> None:
        super().__init__(position, color, size, speed, point, sprites, config)


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
        self.config = config  # Store config for passing to enemies

        self.move_down_distance = (
            move_down_distance
            if move_down_distance is not None
            else formation_config[ConfigKey.ENEMY_FORMATION_MOVE_DOWN_DISTANCE]
        )
        # To prevent moving down immediately on start
        self.can_move_down = False

        self.enemy_col = (
            enemy_col
            if enemy_col is not None
            else formation_config[ConfigKey.ENEMY_COL]
        )
        self.enemy_row = (
            enemy_row
            if enemy_row is not None
            else formation_config[ConfigKey.ENEMY_ROW]
        )
        self.enemy_formation_gap = (
            enemy_formation_gap
            if enemy_formation_gap is not None
            else formation_config[ConfigKey.ENEMY_FORMATION_GAP]
        )
        self.enemy_size = (
            enemy_size
            if enemy_size is not None
            else (
                formation_config[ConfigKey.ENEMY_SIZE_WIDTH],
                formation_config[ConfigKey.ENEMY_SIZE_HEIGHT],
            )
        )
        self.enemy_start_pos = (
            enemy_start_pos if enemy_start_pos is not None else pygame.Vector2(50, 50)
        )
        self.enemy_speed = (
            enemy_speed
            if enemy_speed is not None
            else formation_config[ConfigKey.ENEMY_SPEED]
        )

        self.horizontal_direction = 1
        self.left_limit = left_limit
        self.right_limit = right_limit
        self.enemies: list[list[Enemy]] = [
            [None] * self.enemy_row for _ in range(0, self.enemy_col)
        ]
        self.step_interval = formation_config[ConfigKey.ENEMY_STEP_INTERVAL]
        self.current_step = formation_config[ConfigKey.ENEMY_STEP_INTERVAL]
        self.wave_count = 0

        self.can_move = True
        self.enemy_count = self.enemy_col * self.enemy_row
        self.respawn_timer = formation_config.get(ConfigKey.ENEMY_RESPAWN_TIMER_MS)

        self.bullets: list[Bullet] = []
        self.max_bullets = formation_config[ConfigKey.ENEMY_MAX_BULLETS]
        self.min_firing_cooldown: float = formation_config[
            ConfigKey.ENEMY_MIN_FIRING_COOLDOWN
        ]
        self.max_firing_cooldown: float = formation_config[
            ConfigKey.ENEMY_MAX_FIRING_COOLDOWN
        ]
        self.enemy_firing_cooldown = random.uniform(
            self.min_firing_cooldown, self.max_firing_cooldown
        )

        octopus_sprites = sprite_manager.get_sprites(SpriteKey.OCTOPUS_ENEMY)
        crab_sprites = sprite_manager.get_sprites(SpriteKey.CRAB_ENEMY)
        squid_sprites = sprite_manager.get_sprites(SpriteKey.SQUID_ENEMY)
        self.sprites = {
            SpriteKey.OCTOPUS_ENEMY: octopus_sprites,
            SpriteKey.CRAB_ENEMY: crab_sprites,
            SpriteKey.SQUID_ENEMY: squid_sprites,
        }

        sound_config = config.sound_config()
        self.move_sounds = [
            pygame.mixer.Sound(sound_config[ConfigKey.ENEMY_MOVE_SOUND_1]),
            pygame.mixer.Sound(sound_config[ConfigKey.ENEMY_MOVE_SOUND_2]),
            pygame.mixer.Sound(sound_config[ConfigKey.ENEMY_MOVE_SOUND_3]),
            pygame.mixer.Sound(sound_config[ConfigKey.ENEMY_MOVE_SOUND_4]),
        ]
        self.move_sound_index = 0
        self.move_sound_max_index = len(self.move_sounds) - 1

        self.create_enemies_list()

    def respawn_enemies_list(self):
        self.horizontal_direction = 1
        self.enemy_count = self.enemy_col * self.enemy_row
        self.enemies = [[None] * self.enemy_row for _ in range(0, self.enemy_col)]
        self.can_move_down = False
        self.wave_count = self.wave_count + 1
        self.create_enemies_list()

    def despawn_bullets(self):
        self.bullets = []

    def create_enemies_list(self):
        for col in range(0, self.enemy_col):
            horizontal_offset = (
                col * self.enemy_formation_gap + col * self.enemy_size[0]
            )
            for row in range(0, self.enemy_row):
                vertical_offset = (
                    row * self.enemy_formation_gap + row * self.enemy_size[1]
                )
                x_pos = self.enemy_start_pos.x + horizontal_offset
                y_pos = self.enemy_start_pos.y - vertical_offset
                if row == 0 or row == 1:
                    self.enemies[col][row] = OctupusEnemy(
                        pygame.Vector2(x_pos, y_pos),
                        color="orange",
                        size=self.enemy_size,
                        speed=self.enemy_speed,
                        sprites=self.sprites[SpriteKey.OCTOPUS_ENEMY],
                        config=self.config,
                    )
                elif row == 2 or row == 3:
                    self.enemies[col][row] = CrabEnemy(
                        pygame.Vector2(x_pos, y_pos),
                        color="yellow",
                        size=self.enemy_size,
                        speed=self.enemy_speed,
                        sprites=self.sprites[SpriteKey.CRAB_ENEMY],
                        config=self.config,
                    )
                else:
                    self.enemies[col][row] = SquidEnemy(
                        pygame.Vector2(x_pos, y_pos),
                        color="pink",
                        size=self.enemy_size,
                        speed=self.enemy_speed,
                        sprites=self.sprites[SpriteKey.SQUID_ENEMY],
                        config=self.config,
                    )

    def auto_shoot(self, delta_time: float, sprites: list[pygame.Surface], speed=100):
        for col in self.enemies:
            for i in range(0, len(col)):
                enemy = col[i]
                if (
                    i == 0
                    and len(self.bullets) < self.max_bullets
                    and self.enemy_firing_cooldown < 0
                ):
                    can_shoot = bool(random.randint(0, 1))
                    if can_shoot:
                        bullet_pos = pygame.Vector2(
                            x=enemy.rect.x + enemy.size[0] / 2, y=enemy.rect.y
                        )
                        self.bullets.append(
                            Bullet(position=bullet_pos, speed=speed, sprites=sprites)
                        )
                        self.enemy_firing_cooldown = random.uniform(
                            self.min_firing_cooldown, self.max_firing_cooldown
                        )

        self.enemy_firing_cooldown -= delta_time

    def move_by_step(self, delta_time=float):
        if self.current_step > 0:
            self.current_step -= delta_time + self.wave_count * self.enemy_speed
            return

        if self.is_past_horizontal_bound() and self.can_move_down:       
            self.reverse_direction()
            self.move_down()
            self.can_move_down = False
        else:
            for row in self.enemies:
                for enemy in row:
                    enemy.move_horizontally(enemy.size[0] * self.horizontal_direction)
                    pygame.mixer.Sound.play(self.move_sounds[self.move_sound_index])
            self.move_sound_index += 1
            if self.move_sound_index > self.move_sound_max_index:
                self.move_sound_index = 0
            self.can_move_down = True

        self.current_step = self.step_interval

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
