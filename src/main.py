import pygame
import random
from player import Player
from bullet import Bullet
from enemy import *

pygame.init()
pixel_font = pygame.font.Font("./assets/fonts/ARCADECLASSIC.TTF", 26)
screen = pygame.display.set_mode((600, 800))
# screen = pygame.display.set_mode((100, 200))
clock = pygame.time.Clock()
running = True
delta_time = 0

is_game_over = False

player_start_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() - 80)
playable_area_offset = 4
player = Player(player_start_pos)
player_bullets: list[Bullet] = []
score = 0

enemy_row = 5
enemy_col = 5
enemies: list[list[Enemy]] = [[None] * enemy_row for _ in range(0, enemy_col)]
enemy_size = (40, 20)
enemy_speed = 50
enemy_start_pos = pygame.Vector2(5, 50)
enemy_bullets: list[Bullet] = []
MIN_FIRING_COOLDOWN_TIME = 2
MAX_FIRING_COOLDOWN_TIME = 5
ENEMY_MAX_BULLET = 3
enemy_firing_cooldown: float = random.randint(MIN_FIRING_COOLDOWN_TIME, MAX_FIRING_COOLDOWN_TIME)
enemy_formation = EnemyFormation(left_limit=0, right_limit=screen.get_width(), move_down_distance=enemy_size[1] + 10, enemies=enemies)
enemy_formation_gap = 20




for col in range(0, enemy_col):
    horizontal_offset = col * enemy_formation_gap + col * enemy_size[0]
    for row in range(0, enemy_row):
        vertical_offset = row * enemy_formation_gap + row * enemy_size[1]
        x_pos = enemy_start_pos.x + horizontal_offset
        y_pos = enemy_start_pos.y - vertical_offset
        if row == 0 or row == 1:
            enemies[col][row] = OctupusEnemy(pygame.Vector2(x_pos, y_pos), color='orange', size= enemy_size, speed=enemy_speed)
        elif row == 2 or row == 3:
            enemies[col][row] = CrabEnemy(pygame.Vector2(x_pos, y_pos), color='yellow', size= enemy_size, speed=enemy_speed)
        else:
            enemies[col][row] = SquidEnemy(pygame.Vector2(x_pos, y_pos), color='pink', size= enemy_size, speed=enemy_speed)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and len(player_bullets) == 0):
            # player.shoot()
            bullet_pos = pygame.Vector2(x=player.rect.x + player.size[0] / 2, y=player.rect.y)
            player_bullets.append(Bullet(bullet_pos, color="white", speed=500))

    screen.fill("black")

    # Render

    # Bullet
    for bullet in player_bullets:
        if (bullet.is_out_of_bound(0, screen.get_height())):
            player_bullets.remove(bullet)
            continue
        bullet.move_vertically(delta_time * bullet.speed * -1)
        for col in enemies:
            collide_list = bullet.rect.collidelistall(col)
            if len(collide_list) > 0:
                hit_enemy = col[collide_list[0]]
                score += hit_enemy.point
                col.remove(hit_enemy)
                player_bullets.remove(bullet)
                break
            
        bullet.render(screen)

    for bullet in enemy_bullets:
        if (bullet.is_out_of_bound(0, screen.get_height())):
            enemy_bullets.remove(bullet)
            continue
        bullet.move_vertically(delta_time * bullet.speed)
            
        bullet.render(screen)

    # Player
    player.render(screen)
    keys_pressed = pygame.key.get_pressed()
    if (keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]):
        player.move_left(delta_time=delta_time, left_limit=playable_area_offset)
    if (keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]):
        player.move_right(delta_time, right_limit=screen.get_width() - playable_area_offset - player.size[0])
        
    # Enemy
    enemy_formation.auto_move()
    enemy_formation.current_step -= delta_time
    
    if (enemy_formation.collide_player(player)):
        delta_time = 0
        is_game_over = True

    for col in enemies:
        for i in range(0, len(col)):
            enemy = col[i]
            if i == 0 and (len(enemy_bullets) < ENEMY_MAX_BULLET or len(enemy_bullets) == 0) and enemy_firing_cooldown < 0:
                can_shoot = bool(random.randint(0, 1))
                if (can_shoot):
                    bullet_pos = pygame.Vector2(x=enemy.rect.x + enemy.size[0] / 2, y=enemy.rect.y)
                    enemy_bullets.append(Bullet(bullet_pos, color="white", speed=100))
                    enemy_firing_cooldown = random.randint(MIN_FIRING_COOLDOWN_TIME, MAX_FIRING_COOLDOWN_TIME)

            enemy.render(screen)

    enemy_firing_cooldown -= delta_time

    # UI
    text_surface = pixel_font.render(f"SCORE {score}", (0, 0, 0, 0), "white")
    screen.blit(text_surface, (0, 0))

    pygame.display.flip()

    if not is_game_over:
        delta_time = clock.tick(60)/1000

pygame.quit()