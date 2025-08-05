import pygame
from player import Player
from enemy import *
from sprite_manager import SpriteManager, SpriteKey
from config import Config, ConfigKey
from event import *
from enum import Enum


class GameScene(Enum):
    MAIN_MENU = "main-menu"
    PLAYING = "playing"


class Game:
    def __init__(self):
        self.is_running = True
        pygame.init()

        config = Config()
        display_config = config.display_config()
        font_config = config.font_config()
        asset_config = config.asset_config()
        gameplay_config = config.gameplay_config()
        enemy_config = config.enemy_formation_config()

        self.gameplay_config = gameplay_config
        self.current_scene = GameScene.MAIN_MENU

        self.screen = pygame.display.set_mode(
            (
                display_config[ConfigKey.SCREEN_WIDTH],
                display_config[ConfigKey.SCREEN_HEIGHT],
            )
        )
        self.FPS = display_config[ConfigKey.FPS]
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        self.is_game_over = False
        self.is_pause = False

        self.base_pixel_font = pygame.font.Font(
            font_config[ConfigKey.FONT_PATH], font_config[ConfigKey.BASE_FONT_SIZE]
        )
        self.large_pixel_font = pygame.font.Font(
            font_config[ConfigKey.FONT_PATH], font_config[ConfigKey.LARGE_FONT_SIZE]
        )

        sprite_manager = SpriteManager(asset_config[ConfigKey.SPRITESHEET_PATH])

        player_start_pos = pygame.Vector2(
            self.screen.get_width() / 2,
            self.screen.get_height() - gameplay_config[ConfigKey.PLAYER_START_Y_OFFSET],
        )
        self.playable_area_offset = gameplay_config[ConfigKey.PLAYABLE_AREA_OFFSET]
        player_sprites = sprite_manager.get_sprites(SpriteKey.PLAYER)
        self.player = Player(position=player_start_pos, sprites=player_sprites)

        self.enemy_formation = EnemyFormation(
            left_limit=enemy_config[ConfigKey.ENEMY_SIZE_WIDTH],
            right_limit=self.screen.get_width()
            - enemy_config[ConfigKey.ENEMY_SIZE_WIDTH],
            sprite_manager=sprite_manager,
            config=config,
            enemy_start_pos=pygame.Vector2(5, self.screen.get_height() / 3),
        )

        self.player_bullet_sprites = sprite_manager.get_sprites(SpriteKey.PLAYER_BULLET)
        self.enemy_bullet_sprites = sprite_manager.get_sprites(SpriteKey.ENEMY_BULLET)

    def start(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            match self.current_scene:
                case GameScene.MAIN_MENU:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.current_scene = GameScene.PLAYING
                case GameScene.PLAYING:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        bullet_pos = pygame.Vector2(
                            x=self.player.rect.x + self.player.size[0] / 2,
                            y=self.player.rect.y,
                        )
                        bullet = Bullet(
                            position=bullet_pos,
                            speed=self.gameplay_config[ConfigKey.PLAYER_BULLET_SPEED],
                            sprites=self.player_bullet_sprites,
                        )
                        self.player.shoot(bullet)
                    if event.type == PLAYER_REVIVE_EVENT:
                        self.player.revive()
                        self.is_pause = False

                    if event.type == RESPAWN_ENEMIES_LIST:
                        self.enemy_formation.respawn_enemies_list()

    def update(self):
        if self.is_pause:
            return


        match self.current_scene:
            case GameScene.MAIN_MENU:
               pass
            case GameScene.PLAYING:
                # Bullet
                player_bullets_to_remove = []
                for bullet in self.player.bullets:
                    if bullet.is_out_of_bound(0, self.screen.get_height()):
                        player_bullets_to_remove.append(bullet)
                        continue
                    bullet.move_vertically(self.delta_time * bullet.speed * -1)
                    for col in self.enemy_formation.enemies:
                        collide_list = bullet.rect.collidelistall(col)
                        if len(collide_list) > 0:
                            hit_enemy = col[collide_list[0]]
                            self.player.score += hit_enemy.point
                            col.remove(hit_enemy)
                            player_bullets_to_remove.append(bullet)
                            self.enemy_formation.enemy_count -= 1
                            if self.enemy_formation.enemy_count == 0:
                                self.enemy_formation.despawn_bullets()
                                pygame.time.set_timer(
                                    RESPAWN_ENEMIES_LIST, self.enemy_formation.respawn_timer, 1
                                )
                            break
                for bullet in player_bullets_to_remove:
                    self.player.bullets.remove(bullet)

                enemy_bullets_to_remove = []
                for bullet in self.enemy_formation.bullets:
                    if bullet.is_out_of_bound(0, self.screen.get_height()):
                        enemy_bullets_to_remove.append(bullet)
                        continue
                    bullet.move_vertically(self.delta_time * bullet.speed)
                    if bullet.rect.colliderect(self.player):
                        self.player.lose_life()
                        self.is_pause = True

                        if self.player.lives <= 0:
                            self.delta_time = 0
                            self.is_game_over = True
                        else:
                            pygame.time.set_timer(
                                PLAYER_REVIVE_EVENT, self.player.death_timer_ms, 1
                            )

                        enemy_bullets_to_remove.append(bullet)
                
                for bullet in enemy_bullets_to_remove:
                    self.enemy_formation.bullets.remove(bullet)

                # Player
                keys_pressed = pygame.key.get_pressed()
                if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
                    self.player.move_left(
                        delta_time=self.delta_time, left_limit=self.playable_area_offset
                    )
                if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
                    self.player.move_right(
                        self.delta_time,
                        right_limit=self.screen.get_width()
                        - self.playable_area_offset
                        - self.player.size[0],
                    )

                # Enemy
                self.enemy_formation.auto_move(delta_time=self.delta_time, mode="step")
                self.enemy_formation.auto_shoot(
                    delta_time=self.delta_time, sprites=self.enemy_bullet_sprites, speed=self.gameplay_config[ConfigKey.ENEMY_BULLET_SPEED],
                )

                if self.enemy_formation.collide_player(self.player):
                    self.player.lose_life()
                    if self.player.lives <= 0:
                        self.delta_time = 0
                        self.is_game_over = True

    def render(self):
        self.screen.fill("black")
        match self.current_scene:
            case GameScene.MAIN_MENU:
                play_surface = self.large_pixel_font.render(
                    f"PRESS  ENTER  TO  PLAY", (0, 0, 0, 0), "white"
                )
                self.screen.blit(
                    play_surface,
                    (
                        (self.screen.get_width() - play_surface.get_width())
                        / 2,
                        self.screen.get_height() / 2
                        - play_surface.get_height(),
                    ),
                )
            case GameScene.PLAYING:
                for bullet in self.player.bullets:
                    bullet.render(self.screen)

                for bullet in self.enemy_formation.bullets:
                    bullet.render(self.screen)

                self.player.render(self.screen)

                self.enemy_formation.render(self.screen, delta_time=self.delta_time)

                # UI
                score_surface = self.base_pixel_font.render(
                    f"SCORE {self.player.score}", (0, 0, 0, 0), "white"
                )
                lives_surface = self.base_pixel_font.render(
                    f"LIVES {self.player.lives}", (0, 0, 0, 0), "white"
                )
                game_over_surface = self.large_pixel_font.render(
                    f"GAME OVER!", (0, 0, 0, 0), "white"
                )
                self.screen.blit(score_surface, (0, 0))
                self.screen.blit(
                    lives_surface,
                    (self.screen.get_width() - lives_surface.get_width(), 0),
                )
                if self.is_game_over:
                    self.screen.blit(
                        game_over_surface,
                        (
                            (self.screen.get_width() - game_over_surface.get_width())
                            / 2,
                            self.screen.get_height() / 2
                            - game_over_surface.get_height(),
                        ),
                    )


        pygame.display.flip()

        if not self.is_game_over:
            self.delta_time = self.clock.tick(self.FPS) / 1000


game = Game()
game.start()
