import pygame
import math
import sys
import numpy as np
import random

# Inicialización de Pygame
pygame.init()

# Constantes
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)

# Colores
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Configuración de la pantalla
screen = pygame.display.set_mode(size)
modo_juego = None
# Fuentes
FONT = pygame.font.SysFont("monospace", 75)
fuente = pygame.font.SysFont('Arial', 24)

# Renderizar texto
texto1 = fuente.render('Presiona 1 para Humano vs IA', True, WHITE, BLACK)
texto2 = fuente.render('Presiona 2 para IA vs IA', True, WHITE, BLACK)
texto_rect1 = texto1.get_rect(center=(width // 2, height // 2 - 20))
texto_rect2 = texto2.get_rect(center=(width // 2, height // 2 + 20))
# Bucle para seleccionar el modo de juego
while modo_juego is None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                modo_juego = "Humano vs IA"
            elif event.key == pygame.K_2:
                modo_juego = "IA vs IA"

    # Rellenar el fondo
    screen.fill(BLACK)

    # Dibujar texto en la pantalla
    screen.blit(texto1, texto_rect1)
    screen.blit(texto2, texto_rect2)

    pygame.display.update()
    
# Tablero
board = np.zeros((ROW_COUNT, COLUMN_COUNT))

PLAYER = 0
AI = 1
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2


def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Aquí debes implementar la lógica para verificar si hay un ganador.
    pass

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE + SQUARESIZE/2), int(r*SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), RADIUS)
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):        
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE + SQUARESIZE/2), height - int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE + SQUARESIZE/2), height - int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)
    pygame.display.update()

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def check_horizontal_win(board, piece):
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):  # -3 para evitar exceder el límite del tablero
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    return False

def check_vertical_win(board, piece):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    return False

def check_diagonal_win(board, piece):
    # Diagonal positiva
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Diagonal negativa
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
                
    return False

def winning_move(board, piece):
    # Revisar por ubicaciones horizontales ganadoras
    if check_horizontal_win(board, piece):
        return True

    # Revisar por ubicaciones verticales ganadoras
    if check_vertical_win(board, piece):
        return True

    # Revisar las ubicaciones diagonales ganadoras
    if check_diagonal_win(board, piece):
        return True

    return False


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def minimax(board, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or is_terminal_node(board):
        if is_terminal_node(board):
            if winning_move(board, AI_PIECE):
                return (None, float("inf"))  # Retornar un valor infinito para una victoria
            elif winning_move(board, PLAYER_PIECE):
                return (None, float("-inf"))  # Retornar un valor infinito negativo para una derrota
            else:  # El juego ha terminado sin más movimientos válidos
                return (None, 0)
        else:  # La profundidad es cero
            return (None, 0)  # Modificado para no usar score_position

    if maximizingPlayer:
        value = -math.inf
        column = random.choice(get_valid_locations(board))
        for col in get_valid_locations(board):
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:  # Jugador minimizador
        value = math.inf
        column = random.choice(get_valid_locations(board))
        for col in get_valid_locations(board):
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def minimax_simple(board, depth, maximizingPlayer):
    if depth == 0 or is_terminal_node(board):
        if is_terminal_node(board):
            if winning_move(board, AI_PIECE):  # Suponiendo que AI_PIECE es la IA2
                return (None, float("inf"))
            elif winning_move(board, PLAYER_PIECE):  # Suponiendo que PLAYER_PIECE es la IA1 o el jugador humano
                return (None, float("-inf"))
            else:
                return (None, 0)
        else:
            return (None, 0)

    if maximizingPlayer:
        value = -math.inf
        column = random.choice(get_valid_locations(board))
        for col in get_valid_locations(board):
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)  # Suponiendo que AI_PIECE representa a la IA2
            new_score = minimax_simple(b_copy, depth-1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value
    else:
        value = math.inf
        column = random.choice(get_valid_locations(board))
        for col in get_valid_locations(board):
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)  # Suponiendo que PLAYER_PIECE representa a la IA1 o al jugador humano
            new_score = minimax_simple(b_copy, depth-1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value


def is_board_full(board):
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            if board[row][col] == 0:
                return False  # Encontró una celda vacía, el tablero no está lleno
    return True 

# Función principal
def main():
    # Inicialización de variables
    
    global turno_humano
    
    if modo_juego == "Humano vs IA":
        turno_humano = True
    elif modo_juego == "IA vs IA":
        # Decide quién comienza en modo IA vs IA. Aquí usamos True o False aleatoriamente como ejemplo.
        # Puedes ajustarlo según la lógica específica que desees.
        turno_humano = random.choice([True, False])
    
    game_over = False
    board = create_board()
    draw_board(board)
    pygame.display.update()

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION and turno_humano:
                # Mostrar previsualización del movimiento del jugador
                pass

            if event.type == pygame.MOUSEBUTTONDOWN and turno_humano:
                # Procesar el movimiento del humano
                col = event.pos[0] // SQUARESIZE
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)
                    if winning_move(board, PLAYER_PIECE):
                        game_over = True
                        # Mostrar mensaje de victoria del jugador
                    turno_humano = False  # Cambiar al turno de la IA
                    draw_board(board)

        # Turno de la IA
        if not game_over and not turno_humano and modo_juego != "IA vs IA":
            col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
            if is_valid_location(board, col):
                pygame.time.wait(500)  # Retraso para simular pensamiento de la IA
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)
                if winning_move(board, AI_PIECE):
                    game_over = True
                    # Mostrar mensaje de victoria de la IA
                turno_humano = True  # Devolver el turno al jugador humano
                draw_board(board)

        # Modo IA vs IA
        if not game_over and modo_juego == "IA vs IA":
            # Alternar entre Minimax con poda para IA1 y Minimax simple para IA2.
            if turno_humano:  # IA1 juega con Minimax con poda.
                col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
            else:  # IA2 juega con Minimax simple (sin poda).
                col, minimax_score = minimax_simple(board, 5, True)  # Ajusta según la firma de tu minimax_simple.
            
            if is_valid_location(board, col):
                pygame.time.wait(500)
                row = get_next_open_row(board, col)
                piece = PLAYER_PIECE if turno_humano else AI_PIECE
                drop_piece(board, row, col, piece)
                if winning_move(board, piece):
                    game_over = True
                turno_humano = not turno_humano
                draw_board(board)

        if game_over:
            screen.fill(BLACK)  # Limpia la pantalla antes de mostrar el mensaje

            if winning_move(board, PLAYER_PIECE):
                if modo_juego == "Humano vs IA":
                    message = "¡Jugador gana!"
                else:  # En modo IA vs IA, PLAYER_PIECE representa a la IA 1
                    message = "¡IA 1 gana! (alpha-beta pruning)"
            elif winning_move(board, AI_PIECE):
                if modo_juego == "Humano vs IA":
                    message = "¡IA gana!"
                else:  # En modo IA vs IA, AI_PIECE representa a la IA 2
                    message = "¡IA 2 gana (sin alpha-beta pruning)!"
            elif is_board_full(board):
                message = "¡Empate!"
            else:
                message = "Error: estado desconocido."
            
            fuente = pygame.font.SysFont("monospace", 24)
            label = fuente.render(message, 1, WHITE)
            screen.blit(label, (width / 2 - label.get_width() / 2, height / 2 - label.get_height() / 2))
            
            pygame.display.update()
            pygame.time.wait(7000)  # Espera 7 segundos antes de salir o reiniciar

            # Aquí puedes agregar la lógica para reiniciar el juego o salir
            break  # Rompe el bucle si solo deseas terminar el juego

if __name__ == "__main__":
    main()
