from enum import Enum


class ConfigKey(Enum):
    # Visual
    SCREEN_WIDTH = "screen-width"
    SCREEN_HEIGHT = "screen-height"
    FPS = "FPS"

    # Font
    FONT_PATH = "font-path"
    BASE_FONT_SIZE = "base-font-size"
    LARGE_FONT_SIZE = "large-font-size"

    # Sprite
    SPRITESHEET_PATH = "spritesheet-path"

    # Enemy
    ENEMY_ROW = "enemy-row"
    ENEMY_COL = "enemy-col"
    ENEMY_SIZE_WIDTH = "enemy-size-width"
    ENEMY_SIZE_HEIGHT = "enemy-size-height"
    ENEMY_SPEED = "enemy-speed"
    ENEMY_FORMATION_GAP = "enemy-formation-gap"
    ENEMY_FORMATION_MOVE_DOWN_DISTANCE = "enemy-formation-move-down-distance"

    # Player
    PLAYER_SIZE_WIDTH = "player-size-width"
    PLAYER_SIZE_HEIGHT = "player-size-height"
    PLAYER_SPEED = "player-speed"
    PLAYER_LIVES = "player-lives"
    PLAYER_DEATH_TIMER_MS = "player-death-timer-ms"
    PLAYER_START_Y_OFFSET = "player-start-y-offset"
    PLAYABLE_AREA_OFFSET = "playable-area-offset"

    # Bullet
    PLAYER_BULLET_SPEED = "player-bullet-speed"
    ENEMY_BULLET_SPEED = "enemy-bullet-speed"


class Config:
    def __init__(self) -> None:
        pass

    def display_config(self):
        return {
            ConfigKey.SCREEN_WIDTH: 600,
            ConfigKey.SCREEN_HEIGHT: 800,
            ConfigKey.FPS: 60,
        }

    def font_config(self):
        return {
            ConfigKey.FONT_PATH: "./assets/fonts/ARCADECLASSIC.TTF",
            ConfigKey.BASE_FONT_SIZE: 26,
            ConfigKey.LARGE_FONT_SIZE: 40,
        }

    def asset_config(self):
        return {
            ConfigKey.SPRITESHEET_PATH: "./assets/sprites/SpaceInvadersSpriteSheet.png",
        }

    def gameplay_config(self):
        return {
            # Player
            ConfigKey.PLAYABLE_AREA_OFFSET: 10,
            ConfigKey.PLAYER_START_Y_OFFSET: 80,
            # Bullet
            ConfigKey.ENEMY_BULLET_SPEED: 300,
            ConfigKey.PLAYER_BULLET_SPEED: 500,
        }

    def player_config(self):
        return {
            ConfigKey.PLAYER_SIZE_WIDTH: 40,
            ConfigKey.PLAYER_SIZE_HEIGHT: 20,
            ConfigKey.PLAYER_SPEED: 200,
            ConfigKey.PLAYER_LIVES: 3,
            ConfigKey.PLAYER_DEATH_TIMER_MS: 2000,
        }

    def enemy_formation_config(self):
        return {
            ConfigKey.ENEMY_ROW: 5,
            ConfigKey.ENEMY_COL: 5,
            ConfigKey.ENEMY_SIZE_WIDTH: 40,
            ConfigKey.ENEMY_SIZE_HEIGHT: 20,
            ConfigKey.ENEMY_SPEED: 10,
            ConfigKey.ENEMY_FORMATION_GAP: 20,
            ConfigKey.ENEMY_FORMATION_MOVE_DOWN_DISTANCE: 10,
        }
