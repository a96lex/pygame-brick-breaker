import math
import random

import pygame

from constants import DisplayConfig, EntityConstants, PowerUpTypes


def init_velocity_from_angle(degrees: int):
    a = math.radians(degrees)
    x, y = math.cos(a), math.sin(a)
    vel = pygame.Vector2(x, y)
    vel *= 3
    return vel


class Paddle(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(
            [EntityConstants.paddle.width, EntityConstants.paddle.height]
        )
        self.image.fill(EntityConstants.paddle.color())
        self.rect = self.image.get_rect()
        self.rect.x = int(DisplayConfig.WIDTH / 2 - EntityConstants.paddle.width / 2)
        self.rect.y = int(DisplayConfig.HEIGHT - 60)

    def update_width(self, d_width):
        x, y = self.rect.x, self.rect.y
        self.image = pygame.Surface(
            [
                min(EntityConstants.paddle.max_width, self.rect.width + d_width),
                EntityConstants.paddle.height,
            ]
        )
        self.image.fill(EntityConstants.paddle.color())
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Brick(pygame.sprite.Sprite):
    x: float
    y: float
    has_power_up: bool

    def __init__(self, x, y, power_up) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(
            [EntityConstants.brick.width, EntityConstants.brick.height]
        )
        if power_up:
            self.image.fill(EntityConstants.brick.color_powerup())
        else:
            self.image.fill(EntityConstants.brick.color())
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.has_power_up = power_up

    def update(self):
        self.y += EntityConstants.game.wall_speed
        self.rect.y = self.y
        if self.rect.top > DisplayConfig.HEIGHT:
            self.kill()


class Bricks(pygame.sprite.Group):
    displace_brick = False
    wall_height = -EntityConstants.brick.height

    def add_brick_line(self):
        self.displace_brick = not self.displace_brick
        for i in range(DisplayConfig.WIDTH // EntityConstants.brick.width + 1):
            self.add(
                Brick(
                    i * EntityConstants.brick.width
                    - EntityConstants.brick.width / 2 * (self.displace_brick),
                    -EntityConstants.brick.height,
                    power_up=random.random() < EntityConstants.game.powerup_rate,
                )
            )

    def update(self, *args, **kwargs):
        if self.wall_height >= 0:
            self.add_brick_line()
            self.wall_height = -EntityConstants.brick.height
            EntityConstants.game.wall_speed += 0.02

        self.wall_height += EntityConstants.game.wall_speed
        super().update(*args, **kwargs)


class Ball(pygame.sprite.Sprite):
    speed: pygame.Vector2
    x: float
    y: float

    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(
            [EntityConstants.ball.radius, EntityConstants.ball.radius]
        )
        self.image.fill(EntityConstants.ball.color())
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

        self.speed = speed

    def bounce_with_angle(self, offset):
        self.speed.y = -abs(self.speed.y)
        new_angle = self.speed.as_polar()[1] + math.copysign(
            math.pow(abs(offset), 1.4), offset
        )

        self.speed = init_velocity_from_angle(new_angle)
        self.speed.y = -abs(self.speed.y)

    def update(self):
        new_pos = self.rect.move(self.speed.x, self.speed.y)

        if new_pos.right > DisplayConfig.WIDTH or new_pos.left < 0:
            self.speed.x = -self.speed.x
        if new_pos.bottom > DisplayConfig.HEIGHT:
            self.kill()
        if new_pos.top < 0:
            self.speed.y = -self.speed.y
        self.x += self.speed.x
        self.y += self.speed.y
        self.rect.x = self.x
        self.rect.y = self.y


class Balls(pygame.sprite.Group):
    def add_from_paddle(self, paddle: Paddle):
        self.add(
            Ball(
                paddle.rect.centerx,
                paddle.rect.centery,
                init_velocity_from_angle(random.randint(-140, 40)),
            )
        )

    def add_from_ball(self, ball: Ball):
        self.add(
            Ball(
                ball.rect.centerx,
                ball.rect.centery,
                init_velocity_from_angle(random.randint(0, 360)),
            )
        )


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, width=None) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(list(PowerUpTypes))

        self.image = pygame.Surface(
            [EntityConstants.power_up.width, EntityConstants.power_up.height]
        )
        self.image.fill(EntityConstants.power_up.color[self.type])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update_width(self, dw) -> None:
        self.__init__(self.rect.x, self.rect.y, self.rect.width + dw)

    def update(self):
        self.rect.move_ip(0, EntityConstants.power_up.speed)
        if self.rect.top > DisplayConfig.HEIGHT:
            self.kill()


class PowerUps(pygame.sprite.Group):
    def add_from_brick(self, brick: Brick):
        self.add(
            PowerUp(
                brick.rect.centerx - EntityConstants.power_up.width / 2,
                brick.rect.y,
            )
        )
