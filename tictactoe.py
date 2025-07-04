import pygame
import sys

# Rənglər
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COLOR = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)

# Parametrlər
WIDTH, HEIGHT = 400, 450
SQUARE_SIZE = WIDTH // 3
LINE_WIDTH = 5
CROSS_WIDTH = 15
CIRCLE_WIDTH = 10
CIRCLE_RADIUS = SQUARE_SIZE // 3
SPACE = SQUARE_SIZE // 4

# Pygame başlat
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
font = pygame.font.SysFont(None, 36)
input_font = pygame.font.SysFont(None, 28)
clock = pygame.time.Clock()

# Oyun lövhəsi
board = [[0 for _ in range(3)] for _ in range(3)]

def draw_board():
    screen.fill(WHITE)
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (0, i*SQUARE_SIZE), (WIDTH, i*SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i*SQUARE_SIZE, 0), (i*SQUARE_SIZE, SQUARE_SIZE*3), LINE_WIDTH)

def draw_figures():
    for row in range(3):
        for col in range(3):
            if board[row][col] == 1:
                # X
                pygame.draw.line(screen, BLACK,
                    (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                    (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                    CROSS_WIDTH)
                pygame.draw.line(screen, BLACK,
                    (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                    (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE),
                    CROSS_WIDTH)
            elif board[row][col] == 2:
                # O
                pygame.draw.circle(screen, RED,
                    (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                    CIRCLE_RADIUS, CIRCLE_WIDTH)

def is_available(row, col):
    return board[row][col] == 0

def mark_square(row, col, player):
    board[row][col] = player

def is_full():
    for row in board:
        if 0 in row:
            return False
    return True

def check_win(player):
    for i in range(3):
        if all([board[i][j] == player for j in range(3)]): return True
        if all([board[j][i] == player for j in range(3)]): return True
    if all([board[i][i] == player for i in range(3)]): return True
    if all([board[i][2 - i] == player for i in range(3)]): return True
    return False

def display_message(text, color=GREEN):
    pygame.draw.rect(screen, WHITE, (0, HEIGHT - 50, WIDTH, 50))
    msg = font.render(text, True, color)
    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT - 40))
    pygame.display.update()

def get_player_names():
    input_boxes = [pygame.Rect(80, 100, 240, 40), pygame.Rect(80, 180, 240, 40)]
    active = [False, False]
    texts = ["", ""]
    titles = ["Oyunçu 1 (X):", "Oyunçu 2 (O):"]
    entered = [False, False]

    while True:
        screen.fill(WHITE)
        for i in range(2):
            title = input_font.render(titles[i], True, BLACK)
            screen.blit(title, (input_boxes[i].x, input_boxes[i].y - 25))
            pygame.draw.rect(screen, BLACK, input_boxes[i], 2)
            txt_surface = input_font.render(texts[i], True, BLACK)
            screen.blit(txt_surface, (input_boxes[i].x + 5, input_boxes[i].y + 5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(2):
                    active[i] = input_boxes[i].collidepoint(event.pos)
            if event.type == pygame.KEYDOWN:
                for i in range(2):
                    if active[i]:
                        if event.key == pygame.K_RETURN:
                            entered[i] = True
                            active[i] = False
                        elif event.key == pygame.K_BACKSPACE:
                            texts[i] = texts[i][:-1]
                        else:
                            texts[i] += event.unicode

        pygame.display.update()
        clock.tick(30)

        # Yalnız hər iki ad yazılıb və Enter basılıbsa keç
        if all(entered) and all(texts):
            return texts[0], texts[1]

# ==== OYUN BAŞLAYIR ====
player1_name, player2_name = get_player_names()
player = 1
game_over = False
draw_board()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = event.pos
            if y < SQUARE_SIZE * 3:
                row = y // SQUARE_SIZE
                col = x // SQUARE_SIZE
                if is_available(row, col):
                    mark_square(row, col, player)
                    draw_figures()
                    if check_win(player):
                        winner = player1_name if player == 1 else player2_name
                        display_message(f"Qazanan: {winner} 🎉")
                        game_over = True
                    elif is_full():
                        display_message("Heç-heçə 🤝", RED)
                        game_over = True
                    else:
                        player = 2 if player == 1 else 1

    pygame.display.update()
