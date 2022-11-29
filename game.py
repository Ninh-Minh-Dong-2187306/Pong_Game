import pygame

from src import color
from src.player import Player
from src.ball import Ball
from network import Network

pygame.init()

WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

FPS = 60
PLAYER_WIDTH, PLAYER_HEIGHT = 20, 100
BALL_RADIUS = 7

SCORE_FONT = pygame.font.SysFont("comicsans", 50)
WINNING_SCORE = 10


def draw(win, players, ball):
    win.fill(color.BLACK)

    # left_score_text = SCORE_FONT.render(f"{left_score}", 1, color.WHITE)
    # right_score_text = SCORE_FONT.render(f"{right_score}", 1, color.WHITE)
    # win.blit(left_score_text,
    #          (WIDTH // 4 - left_score_text.get_width() // 2, 20))
    # win.blit(right_score_text,
    #          (WIDTH * (3 / 4) - right_score_text.get_width() // 2, 20))

    for player in players:
        player.draw(win)

    for i in range(10, HEIGHT, HEIGHT // 20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, color.WHITE,
                         (WIDTH // 2 - 5, i, 10, HEIGHT // 20))

    ball.draw(win)
    pygame.display.update()


def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel


def handle_paddle_movement(keys, player):
    if keys[pygame.K_UP] and player.y - player.VEL >= 0:
        player.move(up=True)
    if keys[pygame.K_DOWN] and player.y + player.VEL + player.height <= HEIGHT:
        player.move(up=False)

    # if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
    #     right_paddle.move(up=True)
    # if keys[pygame.
    #         K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
    #     right_paddle.move(up=False)


def main():

    def send_data():
        data = str(net.id) + ":" + str(player.x) + "," + str(player.y)
        reply = net.send(data)
        return reply

    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0, 0

    run = True
    clock = pygame.time.Clock()
    net = Network()

    player1 = Player(10, HEIGHT // 2 - PLAYER_HEIGHT // 2, PLAYER_WIDTH,
                     PLAYER_HEIGHT)
    player2 = Player(WIDTH - 10 - PLAYER_WIDTH,
                     HEIGHT // 2 - PLAYER_HEIGHT // 2, PLAYER_WIDTH,
                     PLAYER_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    if str(net.id) == 0:
        player = player1
        enemy = player2
    else:
        player = player2
        enemy = player1

    # player1_score = 0
    # player2_score = 0

    while run:
        clock.tick(FPS)
        draw(WIN, [player, enemy], ball)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, player)

        enemy.x, enemy.y = parse_data(send_data())

        ball.move()
        handle_collision(ball, player, enemy)

        if ball.x < 0:
            # player2_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            # player1_score += 1
            ball.reset()

        # won = False
        # if player1_score >= WINNING_SCORE:
        #     won = True
        #     win_text = "Player 1 won!"
        # elif player2_score >= WINNING_SCORE:
        #     won = True
        #     win_text = "Player 2 won!"
        #
        # if won:
        #     text = SCORE_FONT.render(win_text, 1, color.WHITE)
        #     WIN.blit(text, (WIDTH // 2 - text.get_width() // 2,
        #                     HEIGHT // 2 - text.get_height() // 2))
        #     pygame.display.update()
        #     pygame.time.delay(5000)
        #     ball.reset()
        #     player1.reset()
        #     player2.reset()
        #     player1_score = 0
        #     player2_score = 0

    pygame.quit()


if __name__ == '__main__':
    main()
