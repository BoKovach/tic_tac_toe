import os.path

import pygame
import sys

pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 36)

blue = pygame.Color('blue')
red = pygame.Color('red')
green = pygame.Color('green')
light_blue = pygame.Color('lightblue')
sky_blue = pygame.Color('skyblue')
black = pygame.Color('black')

pygame.display.set_caption('Tic Toc Toe')

screen = pygame.display.set_mode((500, 500))

base_path = os.path.dirname(__file__)
images_path = os.path.join(base_path, 'assets', 'images')

x_img = pygame.image.load(os.path.join(images_path, 'red_x.png')).convert_alpha()
o_img = pygame.image.load(os.path.join(images_path, 'red_o.png')).convert_alpha()

cell_size = 100
symbol_size = 100 - 20

x_img = pygame.transform.scale(x_img, (symbol_size, symbol_size))
o_img = pygame.transform.scale(o_img, (symbol_size - 10, symbol_size - 10))

reset_button_rect = pygame.Rect(180, 420, 140, 50)

board = [['' for _ in range(3)]for _ in range(3)]
current_player = 'X'


def draw_reset_button():
    pygame.draw.rect(screen, sky_blue, reset_button_rect, border_radius=10)
    text_surface = font.render("Restart", True, black)
    text_rect = text_surface.get_rect(center=reset_button_rect.center)
    screen.blit(text_surface, text_rect)


def reset_game():
    global board, current_player, winner
    board = [['' for _ in range(3)] for _ in range(3)]
    current_player = 'X'
    winner = False


def check_for_winner(b, player):
    for r in range(3):
        if b[r][0] == b[r][1] == b[r][2] != '':
            return player

    for c in range(3):
        if b[0][c] == b[1][c] == b[2][c] != '':
            return player

    if b[0][0] == b[1][1] == b[2][2] != '':
        return player

    if b[0][2] == b[1][1] == b[2][0] != '':
        return player


def draw_turn_text(win_or_draw):
    if winner:
        text_surface = font.render("Game Over!", True, black)
        screen.blit(text_surface, (100, 30))

        text_surface = font.render(f"Winner is player: {current_player}", True, black)
        screen.blit(text_surface, (100, 60))
    elif draw:
        text_surface = font.render("Game Over!", True, black)
        screen.blit(text_surface, (100, 30))

        text_surface = font.render("It's a draw!", True, black)
        screen.blit(text_surface, (100, 60))
    else:
        text = f"Current Player: {current_player}"
        text_surface = font.render(text, True, black)
        screen.blit(text_surface, (100, 50))


def draw_board():
    screen.fill(light_blue)

    pygame.draw.rect(screen, pygame.Color('green'), (100, 100, 300, 300), 10)
    pygame.draw.line(screen, pygame.Color('green'), (100, 200), (390, 200), 10)
    pygame.draw.line(screen, pygame.Color('green'), (100, 300), (390, 300), 10)
    pygame.draw.line(screen, pygame.Color('green'), (200, 100), (200, 390), 10)
    pygame.draw.line(screen, pygame.Color('green'), (300, 100), (300, 390), 10)

    for r in range(3):
        for c in range(3):
            if board[r][c] == 'X':
                screen.blit(x_img, ((c + 1.1) * cell_size, (r + 1.1) * cell_size))
            elif board[r][c] == 'O':
                screen.blit(o_img, ((c + 1.1) * cell_size, (r + 1.1) * cell_size))


winner = False
draw = False
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            if winner or draw:
                if reset_button_rect.collidepoint(mouse_x, mouse_y):
                    reset_game()
                    draw = False
            else:
                row = (mouse_y // cell_size) - 1
                col = (mouse_x // cell_size) - 1

                if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == '':
                    board[row][col] = current_player
                    winner = check_for_winner(board, current_player)

                    if not winner:
                        is_full = all(cell != '' for row in board for cell in row)
                        if is_full:
                            draw = True
                        else:
                            current_player = 'O' if current_player == 'X' else 'X'

    draw_board()
    draw_turn_text(winner or draw)

    if winner or draw:
        draw_reset_button()

    pygame.display.update()

pygame.quit()
