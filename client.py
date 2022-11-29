import pygame

from network import Network
from src import color

pygame.init()

WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("multiplayer PONG")

FONT = pygame.font.SysFont("monospace", 50)


def draw(win, players, ball, score):
    win.fill((40, 40, 40))

    score.draw(win)

    for player in players:
        player.draw(win)

    for i in range(10, HEIGHT, HEIGHT // 20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, color.WHITE,
                         (WIDTH // 2 - 5, i, 10, HEIGHT // 20))

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
        player2, ball, score = n.send(player)
        # print(scores)
        # won = scores[2]
        # if won:
        #     text = pygame.font.SysFont("comicsans",
        #                                50).render(scores[3], 1,
        #                                           (255, 255, 255))
        #     WIN.blit(text, (WIDTH // 2 - text.get_width() // 2,
        #                     HEIGHT // 2 - text.get_height() // 2))
        #     pygame.display.update()
        #     pygame.time.delay(5000)
        #     ball.reset()
        #     player.reset()
        #     player2.reset()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        player.move()
        draw(WIN, [player, player2], ball, score)


main()
