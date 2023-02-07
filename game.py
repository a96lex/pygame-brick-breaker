import pygame

from constants import DisplayConfig
from entities import PowerUpTypes, Balls, Bricks, Paddle, PowerUps


def handle_collision(brick: pygame.sprite.Sprite, ball: pygame.sprite.Sprite):
    dtop = abs(brick.rect.top - ball.rect.bottom)
    dbottom = abs(brick.rect.bottom - ball.rect.top)
    dleft = abs(brick.rect.left - ball.rect.right)
    dright = abs(brick.rect.right - ball.rect.left)

    if any([y < 3 for y in [dtop, dbottom]]):
        ball.speed.y = -ball.speed.y
    if any([x < 3 for x in [dleft, dright]]):
        ball.speed.x = -ball.speed.x


def handle_paddle_collision(
    ball: pygame.sprite.Sprite,
    paddle: pygame.sprite.Sprite,
):
    percentage_from_center = (
        ball.rect.centerx - paddle.rect.centerx
    ) / paddle.rect.width
    ball.bounce_with_angle(percentage_from_center * 40)


class Game:
    display: pygame.Surface
    bricks: Bricks
    balls: Balls
    paddle: Paddle
    power_ups: PowerUps

    def __init__(self, bricks, balls, power_ups, paddle) -> None:
        pygame.init()
        self.display = pygame.display.set_mode(
            (DisplayConfig.WIDTH, DisplayConfig.HEIGHT)
        )
        pygame.display.set_caption("Bricks")
        pygame.display.init()
        self.bricks = bricks
        self.balls = balls
        self.power_ups = power_ups
        self.paddle = paddle

    def main_loop(self) -> None:
        self.display.fill(DisplayConfig.bg_color)
        for group in [self.bricks, self.balls, self.power_ups]:
            group.draw(self.display)
            group.update()
        self.paddle.draw(self.display)
        collisions = pygame.sprite.groupcollide(self.bricks, self.balls, True, False)

        for brick, v in collisions.items():
            for ball in v:
                handle_collision(brick, ball)
            if brick.has_power_up and len(self.power_ups) < 10:
                self.power_ups.add_from_brick(brick)

        balls_hit = pygame.sprite.spritecollide(self.paddle, self.balls, False)
        for ball in balls_hit:
            handle_paddle_collision(ball, self.paddle)

        power_ups_hit = pygame.sprite.spritecollide(self.paddle, self.power_ups, True)

        for power_up in power_ups_hit:
            if power_up.type == PowerUpTypes.NEW_BALL:
                self.balls.add_from_paddle(self.paddle)
            if power_up.type == PowerUpTypes.SPLIT_BALL:
                unique_balls = set()

                for ball in self.balls:
                    if ball not in unique_balls and len(self.balls) < 1000:
                        unique_balls.add(ball)
                        self.balls.add_from_ball(ball)
            if power_up.type == PowerUpTypes.WIDTH:
                self.paddle.update_width(2)

        pygame.display.update()
        pygame.time.delay(8)
