import pygame
from player import Player
from enemy import *

pygame.init()
base_pixel_font = pygame.font.Font("./assets/fonts/ARCADECLASSIC.TTF", 26)
large_pixel_font = pygame.font.Font("./assets/fonts/ARCADECLASSIC.TTF", 40)
screen = pygame.display.set_mode((600, 800))
clock = pygame.time.Clock()
running = True
delta_time = 0
is_game_over = False

player_start_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() - 80)
playable_area_offset = 4
player = Player(player_start_pos)

enemy_row = 5
enemy_col = 5
enemies: list[list[Enemy]] = [[None] * enemy_row for _ in range(0, enemy_col)]
enemy_size = (40, 20)
enemy_speed = 50
enemy_start_pos = pygame.Vector2(5, 50)

enemy_formation = EnemyFormation(
    left_limit=0, 
    right_limit=screen.get_width(), 
    move_down_distance=enemy_size[1] + 10, 
    enemies=enemies, 
    enemy_size=(40, 20),
    enemy_speed=20,
    enemy_start_pos=pygame.Vector2(5, screen.get_height() / 3),
    enemy_row = enemy_row,
    enemy_col = enemy_col,
    enemy_formation_gap = 20   
)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            player.shoot()

    screen.fill("black")

    # Bullet
    for bullet in player.bullets:
        if (bullet.is_out_of_bound(0, screen.get_height())):
            player.bullets.remove(bullet)
            continue
        bullet.move_vertically(delta_time * bullet.speed * -1)
        for col in enemies:
            collide_list = bullet.rect.collidelistall(col)
            if len(collide_list) > 0:
                hit_enemy = col[collide_list[0]]
                player.score += hit_enemy.point
                col.remove(hit_enemy)
                player.bullets.remove(bullet)
                break

    for bullet in enemy_formation.bullets:
        if (bullet.is_out_of_bound(0, screen.get_height())):
            enemy_formation.bullets.remove(bullet)
            continue
        bullet.move_vertically(delta_time * bullet.speed)
        if (bullet.rect.colliderect(player)):
            player.lose_life()
            if (player.lives <= 0):
                delta_time = 0
                is_game_over = True
            enemy_formation.bullets.remove(bullet)

    # Player
    keys_pressed = pygame.key.get_pressed()
    if (keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]):
        player.move_left(delta_time=delta_time, left_limit=playable_area_offset)
    if (keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]):
        player.move_right(delta_time, right_limit=screen.get_width() - playable_area_offset - player.size[0])
        
    # Enemy
    enemy_formation.auto_move(delta_time=delta_time, mode="step")
    enemy_formation.auto_shoot(delta_time=delta_time)
    
    if (enemy_formation.collide_player(player)):
        player.lose_life()
        if (player.lives <= 0):
            delta_time = 0
            is_game_over = True
    # UI
    score_surface = base_pixel_font.render(f"SCORE {player.score}", (0, 0, 0, 0), "white")
    lives_surface = base_pixel_font.render(f"LIVES {player.lives}", (0, 0, 0, 0), "white")
    game_over_surface = large_pixel_font.render(f"GAME OVER!", (0, 0, 0, 0), "white")
   
    # Render
    for bullet in player.bullets:
        bullet.render(screen)

    for bullet in enemy_formation.bullets:
        bullet.render(screen)

    player.render(screen)

    enemy_formation.render(screen)

    screen.blit(score_surface, (0, 0))
    screen.blit(lives_surface, (screen.get_width() - lives_surface.get_width(), 0))
    if (is_game_over):
        screen.blit(game_over_surface, ((screen.get_width() - game_over_surface.get_width()) / 2, screen.get_height() / 2 - game_over_surface.get_height()))

    pygame.display.flip()

    if not is_game_over:
        delta_time = clock.tick(60)/1000

pygame.quit()