import pygame

from network import Network

WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")

clientNumber = 0


def draw(win, players):
    win.fill((255, 255, 255))
    for player in players:
        player.draw(win)
    pygame.display.update()


def main():
    run = True
    n = Network()
    player = n.get_player()
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        player2 = n.send(player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        player.move()
        draw(WIN, [player, player2])


main()
