import pygame

from network import Network
from src.ball import Ball

WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")

clientNumber = 0
# ball = Ball(350 - 7, 250 - 7, 7)


def draw(win, players, ball):
    win.fill((40, 40, 40))
    for player in players:
        player.draw(win)
    ball.draw(win)
    pygame.display.update()


def main():
    pygame.init()
    run = True
    n = Network()
    player = n.get_player()
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        player2, ball = n.send(player)
        # list = n.send(player)
        # player2 = list[0]
        # ball = list[1]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        player.move()
        draw(WIN, [player, player2], ball)


main()
