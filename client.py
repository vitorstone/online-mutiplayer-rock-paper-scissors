import pygame
from network import Network
from game import Game
from button import ALL_BUTTONS
import colors

pygame.init()
width = 700
height = 700
window: pygame.Surface = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
pygame.mixer.music.load("data/sounds/Fluffing-a-Duck.mp3")
pygame.mixer.music.play(-1)


def redrawWindow(window: pygame.Surface, game: Game, player: int):

    window.fill((255, 250, 250))

    if game.isConnected():

        font = pygame.font.Font("data/fonts/PressStart2P-Regular.ttf", 20)
        text: pygame.Surface = font.render("Your Move", 1, colors.BLACK)
        window.blit(text, (80, 200))
        text: pygame.Surface = font.render("Opponent's", 1, colors.BLACK)
        window.blit(text, (380, 200))

        moveP1 = game.get_player_move(0)
        moveP2 = game.get_player_move(1)

        if game.bothWent():
            text1 = font.render(moveP1, 1, colors.BLACK)
            text2 = font.render(moveP2, 1, colors.BLACK)
        else:
            if game.p1Went and player == 0:
                text1 = font.render(moveP1, 1, colors.BLACK)
            elif game.p1Went:
                text1 = font.render("Locked In", 1, colors.BLACK)
            else:
                text1 = font.render("Waiting...", 1, colors.BLACK)

            if game.p2Went and player == 1:
                text2 = font.render(moveP2, 1, colors.BLACK)
            elif game.p2Went:
                text2 = font.render("Locked In", 1, colors.BLACK)
            else:
                text2 = font.render("Waiting...", 1, colors.BLACK)

        if player == 1:
            window.blit(text2, (100, 350))
            window.blit(text1, (400, 350))

        else:
            window.blit(text1, (100, 350))
            window.blit(text2, (400, 350))

        for btn in ALL_BUTTONS:
            btn.draw(window)

    else:
        font = pygame.font.Font("data/fonts/PressStart2P-Regular.ttf", 30)
        text: pygame.Surface = font.render("Waiting for Player...", 1, colors.BLACK)

        window.blit(
            text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2)
        )

    pygame.display.update()


def main():

    run = True
    clock = pygame.time.Clock()
    network = Network()
    player = network.getPlayerNumber()
    print("You are player ", player)

    while run:
        clock.tick(60)
        try:
            game: Game = network.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(window, game, player)
            pygame.time.delay(500)
            try:
                game: Game = network.send("reset")
            except:
                run = False
                print("Couldn't get game.")
                break

            font = pygame.font.Font("data/fonts/PressStart2P-Regular.ttf", 40)

            if (game.winner() == 1 and player == 1) or (
                game.winner() == 0 and player == 0
            ):
                text: pygame.Surface = font.render("You Won!", 1, colors.GREEN)
            elif game.winner() == -1:
                text: pygame.Surface = font.render("Tie Game!", 1, colors.BLUE)
            else:
                text: pygame.Surface = font.render("You Lost...", 1, colors.RED)

            window.blit(
                text,
                (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2),
            )
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                for btn in ALL_BUTTONS:
                    if btn.click(pos) and game.isConnected():
                        if player == 0:
                            if not game.p1Went:
                                network.send(btn.text)
                        else:
                            if not game.p2Went:
                                network.send(btn.text)

        redrawWindow(window, game, player)


def menu():

    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        window.fill((255, 250, 250))
        font = pygame.font.Font("data/fonts/PressStart2P-Regular.ttf", 30)
        text: pygame.Surface = font.render("Click to Play!", 1, (0, 0, 0))
        window.blit(text, (150, 300))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                click = pygame.mixer.Sound("data/sounds/arcade-click.wav")
                click.play()

    main()


while True:

    menu()
