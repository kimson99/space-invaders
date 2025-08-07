import pygame
from bullet import Bullet
from config import Config, ConfigKey


class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        sprites: list[pygame.Surface],
        position: tuple[int, int] = None,
        speed: float | None = None,
        size: tuple[int, int] | None = None,
        lives: float | None = None,
    ):
        pygame.sprite.Sprite.__init__(self)

        config = Config()
        player_config = config.player_config()

        self.position = position if position is not None else pygame.Vector2(0, 0)
        self.speed = (
            speed if speed is not None else player_config[ConfigKey.PLAYER_SPEED]
        )
        self.size = (
            size
            if size is not None
            else (
                player_config[ConfigKey.PLAYER_SIZE_WIDTH],
                player_config[ConfigKey.PLAYER_SIZE_HEIGHT],
            )
        )
        self.lives = (
            lives if lives is not None else player_config[ConfigKey.PLAYER_LIVES]
        )

        self.bullets: list[Bullet] = []
        self.score = 0
        self.death_timer_ms = player_config[ConfigKey.PLAYER_DEATH_TIMER_MS]
        self.is_dead = False

        self.sprites = [pygame.transform.scale(sprite, self.size) for sprite in sprites]
        self.max_sprites_index = len(self.sprites) - 1
        self.curr_sprite_index = 0
        self.death_sprite = self.sprites[1]
        self.rect = self.sprites[self.curr_sprite_index].get_rect()
        self.rect.x = position.x
        self.rect.y = position.y

        self.shoot_sound = pygame.mixer.Sound("./assets/audios/shoot.wav")
        self.death_sound = pygame.mixer.Sound("./assets/audios/explosion.wav")

    def move_left(self, delta_time: float, left_limit: float):
        self.rect.x = max(self.rect.x - self.speed * delta_time, left_limit)

    def move_right(self, delta_time: float, right_limit: float):
        self.rect.x = min(self.rect.x + self.speed * delta_time, right_limit)

    def shoot(self, bullet: Bullet):
        # One bullet at a time
        if len(self.bullets) > 0:
            return
        pygame.mixer.Sound.play(self.shoot_sound)
        self.bullets.append(bullet)

    def lose_life(self):
        self.lives -= 1
        self.is_dead = True
        pygame.mixer.Sound.play(self.death_sound)

    def revive(self):
        self.is_dead = False

    def render(self, surface: pygame.Surface):
        surface.blit(
            self.death_sprite if self.is_dead else self.sprites[self.curr_sprite_index],
            self.rect,
        )
