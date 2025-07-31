import pygame
from player import Player
from enemy import *
from sprite_manager import SpriteManager



PLAYER_REVIVE_EVENT = pygame.event.custom_type()

class Game:
    def __init__(self):
        self.is_running = True
        pygame.init()
        self.base_pixel_font = pygame.font.Font("./assets/fonts/ARCADECLASSIC.TTF", 26)
        self.large_pixel_font = pygame.font.Font("./assets/fonts/ARCADECLASSIC.TTF", 40)
        self.screen = pygame.display.set_mode((600, 800))
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        self.is_game_over = False
        self.FPS = 60
        self.is_pause = False

        sprite_manager = SpriteManager('./assets/sprites/SpaceInvadersSpriteSheet.png')

        player_start_pos = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() - 80)
        self.playable_area_offset = 10
        player_sprites = sprite_manager.get_sprites("player")
        self.player = Player(position=player_start_pos
        , sprites=player_sprites)

        enemy_row = 5
        enemy_col = 5
        self.enemies: list[list[Enemy]] = [[None] * enemy_row for _ in range(0, enemy_col)]
        enemy_size = (40, 20)
        enemy_speed = 10

        self.enemy_formation = EnemyFormation(
            left_limit=0, 
            right_limit=self.screen.get_width(), 
            move_down_distance=10, 
            enemies=self.enemies, 
            enemy_size=enemy_size,
            enemy_speed=enemy_speed,
            enemy_start_pos=pygame.Vector2(5, self.screen.get_height() / 3),
            enemy_row = enemy_row,
            enemy_col = enemy_col,
            enemy_formation_gap = 20,
            sprite_manager=sprite_manager  
        )

        self.player_bullet_sprites = sprite_manager.get_sprites("player_bullet")

        self.enemy_bullet_sprites = sprite_manager.get_sprites("enemy_bullet")

    def start(self):
        while(self.is_running):
            self.update()
            self.render()
        pygame.quit()


    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                bullet_pos = pygame.Vector2(x=self.player.rect.x + self.player.size[0] / 2, y=self.player.rect.y)
                bullet = Bullet(position=bullet_pos, speed=500, sprites=self.player_bullet_sprites)
                self.player.shoot(bullet)
            if (event.type == PLAYER_REVIVE_EVENT):
                self.player.revive()
                self.is_pause = False

        self.screen.fill("black")
        if (self.is_pause):
            return

        # Bullet
        for bullet in self.player.bullets:
            if (bullet.is_out_of_bound(0, self.screen.get_height())):
                self.player.bullets.remove(bullet)
                continue
            bullet.move_vertically(self.delta_time * bullet.speed * -1)
            for col in self.enemies:
                collide_list = bullet.rect.collidelistall(col)
                if len(collide_list) > 0:
                    hit_enemy = col[collide_list[0]]
                    self.player.score += hit_enemy.point
                    col.remove(hit_enemy)
                    self.player.bullets.remove(bullet)
                    break

        for bullet in self.enemy_formation.bullets:
            if (bullet.is_out_of_bound(0, self.screen.get_height())):
                self.enemy_formation.bullets.remove(bullet)
                continue
            bullet.move_vertically(self.delta_time * bullet.speed)
            if (bullet.rect.colliderect(self.player)):
                self.player.lose_life()
                self.is_pause = True

                if (self.player.lives <= 0):
                    self.delta_time = 0
                    self.is_game_over = True
                else:
                    pygame.time.set_timer(PLAYER_REVIVE_EVENT, self.player.death_timer_ms)

                self.enemy_formation.bullets.remove(bullet)

        # Player
        keys_pressed = pygame.key.get_pressed()
        if (keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]):
            self.player.move_left(delta_time=self.delta_time, left_limit=self.playable_area_offset)
        if (keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]):
            self.player.move_right(self.delta_time, right_limit=self.screen.get_width() - self.playable_area_offset - self.player.size[0])
            
        # Enemy
        self.enemy_formation.auto_move(delta_time=self.delta_time, mode="step")
        self.enemy_formation.auto_shoot(delta_time=self.delta_time, sprites=self.enemy_bullet_sprites)
        
        if (self.enemy_formation.collide_player(self.player)):
            self.player.lose_life()
            if (self.player.lives <= 0):
                delta_time = 0
                self.is_game_over = True

        # UI
        self.score_surface = self.base_pixel_font.render(f"SCORE {self.player.score}", (0, 0, 0, 0), "white")
        self.lives_surface = self.base_pixel_font.render(f"LIVES {self.player.lives}", (0, 0, 0, 0), "white")
        self.game_over_surface = self.large_pixel_font.render(f"GAME OVER!", (0, 0, 0, 0), "white")

    def render(self):
        # Render
        for bullet in self.player.bullets:
            bullet.render(self.screen)

        for bullet in self.enemy_formation.bullets:
            bullet.render(self.screen)

        self.player.render(self.screen)

        self.enemy_formation.render(self.screen, delta_time=self.delta_time)

        self.screen.blit(self.score_surface, (0, 0))
        self.screen.blit(self.lives_surface, (self.screen.get_width() - self.lives_surface.get_width(), 0))
        if (self.is_game_over):
            self.screen.blit(self.game_over_surface, ((self.screen.get_width() - self.game_over_surface.get_width()) / 2, self.screen.get_height() / 2 - self.game_over_surface.get_height()))

        pygame.display.flip()

        if not self.is_game_over:
            self.delta_time = self.clock.tick(self.FPS)/1000
    
game = Game()
game.start()
    

    

