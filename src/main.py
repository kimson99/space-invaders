import pygame
from player import Player
from bullet import Bullet
from enemy import *

pygame.init()
# screen = pygame.display.set_mode((600, 800))
screen = pygame.display.set_mode((100, 200))
clock = pygame.time.Clock()
running = True
delta_time = 0

player_start_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() - 80)
playable_area_offset = 4

player = Player(player_start_pos)
bullets: list[Bullet] = []
enemy_row = 1
enemy_col = 1
enemies: list[list[Enemy]] = [[None] * enemy_col for _ in range(0, enemy_row)]
enemy_size = (20, 20)
enemy_speed = 50
enemy_start_pos = pygame.Vector2(5, 50)

enemy_formation = EnemyFormation(left_limit=0, right_limit=screen.get_width(), move_down_distance=enemy_size[1] + 10, enemies=enemies)



for x in range(0, enemy_row):
    for y in range(0, enemy_col):
        vertical_offset = x * 10 + x * enemy_size[1]
        horizontal_offset = y * 10 + y * enemy_size[0]
        x_pos = enemy_start_pos.x + horizontal_offset
        y_pos = enemy_start_pos.y + vertical_offset
        if x == 0 or x == 1:
            enemies[x][y] = OctupusEnemy(pygame.Vector2(x_pos, y_pos), color='orange', size= enemy_size, speed=enemy_speed)
        elif x == 2 or x == 3:
            enemies[x][y] = CrabEnemy(pygame.Vector2(x_pos, y_pos), color='yellow', size= enemy_size, speed=enemy_speed)
        else:
            enemies[x][y] = SquidEnemy(pygame.Vector2(x_pos, y_pos), color='pink', size= enemy_size, speed=enemy_speed)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            # player.shoot()
            bullet_pos = pygame.Vector2(x=player.rect.x + player.size[0] / 2, y=player.rect.y)
            bullets.append(Bullet(bullet_pos, "white", speed=5))

    screen.fill("black")

    # Render

    # Player
    player.render(screen)
    keys_pressed = pygame.key.get_pressed()
    if (keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]):
        player.move_left(delta_time=delta_time, left_limit=playable_area_offset)
    if (keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]):
        player.move_right(delta_time, right_limit=screen.get_width() - playable_area_offset - player.size[0])
        
    # Bullet
    for bullet in bullets:
        bullet.rect.y -= delta_time * bullet.speed
        bullet.render(screen)

    # Enemy
    enemy_formation.auto_move_horizontally(delta_time=delta_time)

    if (enemy_formation.is_past_bound()):
        enemy_formation.reverse_direction()
        enemy_formation.move_down()

    for row in enemies:
        for enemy in row:
            enemy.render(screen)

    pygame.display.flip()

    delta_time = clock.tick(60)/1000

pygame.quit()