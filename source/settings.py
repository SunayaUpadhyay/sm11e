# game setup
WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64
PLAYER_HEALTH = 200
DEFAULT_IMAGE_SIZE = (TILESIZE, TILESIZE)
PLAYER_DEFAULT_IMAGE_SIZE = (60, 75)
PLAYER_ANIMATION_TIME = 0.20
ENEMY_ANIMATION_TIME = 0.2
INITIAL_SPAWN_TIMER = 3000
MAX_SPAWN_LIMIT = 500
SPAWN_DECREMENT_TIME = 50
MAX_ENEMIES = 50
DASH_SPEED = 10

BULLET_DATA = {
    "damage": 20,
    "cooldown": 20,
    "graphic": "../graphics/character/player/bullet/bullet_f0.png",
}

ENEMIES = {
    "big_demon": {
        "health": 200,
        "damage": 30,
        "size": (128, 128),
        "speed": 2,
        "graphic": "../graphics/character/enemies/big_demon/",
        "animation_number": 4,
    },
    "big_zombie": {
        "health": 160,
        "damage": 20,
        "speed": 3,
        "size": (128, 128),
        "graphic": "../graphics/character/enemies/big_zombie/",
        "animation_number": 4,
    },
    "ogre": {
        "health": 100,
        "damage": 15,
        "speed": 3,
        "size": (96, 96),
        "graphic": "../graphics/character/enemies/ogre/",
        "animation_number": 4,
    },
    "swampy": {
        "health": 50,
        "speed": 5,
        "damage": 20,
        "size": (64, 64),
        "graphic": "../graphics/character/enemies/swampy/",
        "animation_number": 4,
    },
    "eye": {
        "health": 50,
        "damage": 10,
        "size": (64, 64),
        "speed": 6,
        "graphic": "../graphics/character/enemies/eye/",
        "animation_number": 6,
    },
    "doc": {
        "health": 25,
        "damage": 5,
        "size": (64, 64),
        "speed": 5,
        "graphic": "../graphics/character/enemies/doc/",
        "animation_number": 8,
    },
    "archer": {
        "health": 75,
        "damage": 10,
        "size": (64, 64),
        "speed": 5,
        "graphic": "../graphics/character/enemies/archer/",
        "animation_number": 8,
    },
}
