from enum import Enum


class ConfigKey(Enum):
    # Visual
    SCREEN_WIDTH = "screen-width"
    SCREEN_HEIGHT = "screen-height"
    FPS = "FPS"
    SCREEN_COLOR = "screen-color"
    TEXT_COLOR = "text-color"

    # Font
    FONT_PATH = "font-path"
    BASE_FONT_SIZE = "base-font-size"
    LARGE_FONT_SIZE = "large-font-size"

    # Sprite
    SPRITESHEET_PATH = "spritesheet-path"

    # Sound
    ENEMY_MOVE_SOUND_1 = "enemy-move-sound-1"
    ENEMY_MOVE_SOUND_2 = "enemy-move-sound-2"
    ENEMY_MOVE_SOUND_3 = "enemy-move-sound-3"
    ENEMY_MOVE_SOUND_4 = "enemy-move-sound-4"
    PLAYER_SHOOT_SOUND = "player-shoot-sound"
    PLAYER_DEATH_SOUND = "player-death-sound"

    # Enemy
    ENEMY_ROW = "enemy-row"
    ENEMY_COL = "enemy-col"
    ENEMY_SIZE_WIDTH = "enemy-size-width"
    ENEMY_SIZE_HEIGHT = "enemy-size-height"
    ENEMY_SPEED = "enemy-speed"
    ENEMY_FORMATION_GAP = "enemy-formation-gap"
    ENEMY_FORMATION_MOVE_DOWN_DISTANCE = "enemy-formation-move-down-distance"
    ENEMY_RESPAWN_TIMER_MS = "enemy-respawn-timer-ms"
    ENEMY_MAX_BULLETS = "enemy-max-bullet"
    ENEMY_STEP_INTERVAL = "enemy-step-interval"
    ENEMY_MIN_FIRING_COOLDOWN = "enemy-min-firing-cooldown"
    ENEMY_MAX_FIRING_COOLDOWN = "enemy-max-firing-cooldown"
    ENEMY_ANIMATION_INTERVAL = "enemy-animation-interval"

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

    # Barrier
    BARRIER_COUNT = "barrier-count"
    BARRIER_WIDTH = "barrier-width"
    BARRIER_HEIGHT = "barrier-height"
    BARRIER_DAMAGED_WIDTH = "barrier-damaged-width"
    BARRIER_DAMAGED_HEIGHT = "barrier-damaged-height"


class Config:
    def __init__(self) -> None:
        pass

    def display_config(self):
        return {
            ConfigKey.SCREEN_WIDTH: 600,
            ConfigKey.SCREEN_HEIGHT: 800,
            ConfigKey.FPS: 60,
            ConfigKey.SCREEN_COLOR: "black",
            ConfigKey.TEXT_COLOR: "white",
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

    def sound_config(self):
        return {
            ConfigKey.ENEMY_MOVE_SOUND_1: "./assets/audios/fastinvader1.wav",
            ConfigKey.ENEMY_MOVE_SOUND_2: "./assets/audios/fastinvader2.wav",
            ConfigKey.ENEMY_MOVE_SOUND_3: "./assets/audios/fastinvader3.wav",
            ConfigKey.ENEMY_MOVE_SOUND_4: "./assets/audios/fastinvader4.wav",
            ConfigKey.PLAYER_SHOOT_SOUND: "./assets/audios/shoot.wav",
            ConfigKey.PLAYER_DEATH_SOUND: "./assets/audios/explosion.wav",
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
            ConfigKey.ENEMY_FORMATION_MOVE_DOWN_DISTANCE: 20,
            ConfigKey.ENEMY_RESPAWN_TIMER_MS: 2000,
            ConfigKey.ENEMY_MAX_BULLETS: 3,
            ConfigKey.ENEMY_MIN_FIRING_COOLDOWN: 1,
            ConfigKey.ENEMY_MAX_FIRING_COOLDOWN: 2,
            ConfigKey.ENEMY_STEP_INTERVAL: 0.5,
            ConfigKey.ENEMY_ANIMATION_INTERVAL: 0.5,
        }

    def barrier_config(self):
        return {
            ConfigKey.BARRIER_COUNT: 4,
            ConfigKey.BARRIER_WIDTH: 80,
            ConfigKey.BARRIER_HEIGHT: 30,
            ConfigKey.BARRIER_DAMAGED_WIDTH: 30,
            ConfigKey.BARRIER_DAMAGED_HEIGHT: 30,
        }
