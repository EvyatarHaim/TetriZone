import pygame
from Game.game import Game
from Game.colors import Colors
import socket
from utils import send_message


# Format the time that is on the timer.
def format_time(seconds):
    minutes = seconds // 60
    seconds %= 60
    return f"{minutes:02}:{seconds:02}"


# Run the Tetris game.
def tetris_game(client_socket: socket, username, key):
    pygame.init()

    title_font = pygame.font.SysFont('Poppins Black', 24)
    score_surface = title_font.render("Score", True, Colors.white)
    next_surface = title_font.render("Next", True, Colors.white)
    game_over_surface = title_font.render("GAME OVER", True, Colors.white)

    score_rect = pygame.Rect(320, 55, 170, 60)
    next_rect = pygame.Rect(320, 215, 170, 180)

    # Adjust the position of the timer rectangle based on next_rect.
    timer_rect = pygame.Rect(next_rect.left, next_rect.bottom + 50, next_rect.width, 50)

    screen = pygame.display.set_mode((500, 620))
    pygame.display.set_caption("Tetris")

    clock = pygame.time.Clock()

    game = Game()

    GAME_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(GAME_UPDATE, 200)

    counter = 0
    elapsed_time = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if game.game_over:
                    game.game_over = False
                    game.reset()
                if event.key == pygame.K_LEFT and game.game_over == False:
                    game.move_left()
                if event.key == pygame.K_RIGHT and game.game_over == False:
                    game.move_right()
                if event.key == pygame.K_DOWN and game.game_over == False:
                    game.move_down()
                    game.update_score(0, 1)
                if event.key == pygame.K_UP and game.game_over == False:
                    game.rotate()
            if event.type == GAME_UPDATE and game.game_over == False:
                game.move_down()
                elapsed_time += 0.2  # Update elapsed time

        # Drawing
        score_value_surface = title_font.render(str(game.score), True, Colors.white)
        timer_surface = title_font.render("Time: " + format_time(int(elapsed_time)), True,
                                          Colors.white)  # Update timer surface

        screen.fill(Colors.dark_blue)
        screen.blit(score_surface, (365, 20, 50, 50))
        screen.blit(next_surface, next_rect.topleft)

        if game.game_over and counter == 0:
            counter = 1

            screen.blit(game_over_surface, (520, 650, 50, 50))
            # Game_over|username|score|game_time(in seconds)
            message = '|'.join(["Game_Over", username, str(game.score), str(game.lines), str(int(elapsed_time))])
            send_message(message, client_socket, key)

        pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
        screen.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx,
                                                                      centery=score_rect.centery))
        pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
        game.draw(screen)

        screen.blit(timer_surface, timer_rect.topleft)  # Draw the timer at the adjusted position

        pygame.display.update()
        clock.tick(60)
