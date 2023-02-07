import random
from enum import Enum


class DisplayConfig:
    WIDTH, HEIGHT = int(1280 * 0.8), int(720 * 0.8)
    bg_color = (60, 60, 70)


class PowerUpTypes(Enum):
    WIDTH = "width"
    NEW_BALL = "new_ball"
    SPLIT_BALL = "split_ball"


class EntityConstants:
    class game:
        wall_speed = 0.1
        powerup_rate = 0.2

    class brick:
        width = 32
        height = 10
        color = lambda: (
            125 + random.randint(0, 30),
            15 + random.randint(0, 40),
            10 + random.randint(0, 30),
        )
        color_powerup = lambda: (
            180 + random.randint(0, 10),
            130 + random.randint(0, 20),
            10 + random.randint(0, 20),
        )

    class ball:
        radius = 2
        color = lambda: (
            100 + random.randint(0, 155),
            200 + random.randint(0, 55),
            200 + random.randint(0, 55),
        )

    class paddle:
        width = 50
        max_width = 180
        height = 10
        color = lambda: (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )

    class power_up:
        width = 5
        height = width
        color = {
            PowerUpTypes.WIDTH: (200, 200, 50),
            PowerUpTypes.NEW_BALL: (50, 200, 200),
            PowerUpTypes.SPLIT_BALL: (200, 50, 200),
        }
        speed = 2
