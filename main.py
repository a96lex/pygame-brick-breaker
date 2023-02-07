import asyncio

import pygame

from game import Game
from entities import Balls, Bricks, Paddle, PowerUps


paddle = Paddle()
bricks = Bricks()
power_ups = PowerUps()
balls = Balls()

balls.add_from_paddle(paddle)

game = Game(bricks, balls, power_ups, paddle)


async def main():
    running = True
    draging = False
    while running:
        game.main_loop()
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                pass

            elif event.type == pygame.MOUSEBUTTONDOWN:
                draging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                draging = False
            elif event.type == pygame.MOUSEMOTION:
                if draging:
                    paddle.rect.x = mx - paddle.rect.width / 2
        await asyncio.sleep(0)


asyncio.run(main())
