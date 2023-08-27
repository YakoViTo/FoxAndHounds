#Kavir Alvarado CI: 26.256.604
import pygame
from copy import deepcopy
import time

#constante
WIDTH, HEIGHT = 700, 700
ROWS, COLS = 8, 8
SQUARE_SIZE = HEIGHT//ROWS

#colores
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
INDIGO = (75, 0, 130)
GOLD = (255,215,0)
ORANJE = "#EB6600"

#ventana
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Juego: El Zorro y los Cazadores')

#piezas
zorro = pygame.image.load("Zorro.png")
cazador = pygame.image.load("Cazador.png")
fi = window.blit(zorro, zorro.get_rect())
hi = window.blit(cazador, cazador.get_rect())

#tabla
class Board:
    #constructor
    def __init__(self):
        self.board = []
        self.board_debug = []
        self.create_board()
        self.foxPos = (7, 4)
        self.prevFoxPos = (0,0)

    #crear tablero de juego gui
    def draw_board(self, window):
        window.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(window, WHITE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    #función de cálculo de puntuación
    #si un movimiento lleva a un estado donde el zorro gana entonces doy un "incentivo" para tomar esa ruta
    #El zorro tiene más movimientos válidos: intento avanzar, probablemente donde me lleve a la victoria.
    #La distancia reunida de todos los cazadores al zorro es menor: intento retroceder o buscar una salida.
    #La distancia reunida de todos los cazadores al zorro es mayor: intento moverme hacia adelante.
    #La distancia entre el cazador de arriba y el de abajo, respectivamente entre el cazador de la derecha y el de la izquierda son mayores: intento pasar entre ellos.
    #No hay cazadores al frente: avanzo hasta llegar a la fila 0
    def evaluate(self):
        if len(self.get_valid_moves(self.get_piece(self.foxPos[0], self.foxPos[1]))) == 0 :
            return 10000000
        return -(7 - self.foxPos[0]) * 10 
        - len(self.get_valid_moves(self.get_piece(self.foxPos[0], self.foxPos[1]))) * 4 
        - self.distance_to_fox() * 8 - self.distance_between_blacks() * 6 - self.will_win()


    #segunda función para calcular la puntuación
    #un movimiento del zorro tiene una puntuación más alta si está más cerca de la línea 0, si está más lejos de las cazadores y si tiene tantos movimientos como sea posible en un punto
    #también uso la primera función de evolución para hacer que el zorro use movimientos que le lleven a una victoria más rápida  
    def alternate_evaluate(self):
        
        return 8**abs(self.foxPos[0] - 7) + self.distance_to_fox() * 2 + 4 ** abs(4 - self.foxPos[1]) - self.evaluate()


   #función para obtener una lista de todas las piezas de un tipo - se utiliza principalmente para devolver loboos y ver sus posiciones    
    def get_all_pieces(self, tipo):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.tipo == tipo:
                    pieces.append(piece)
        return pieces

    #función para la suma de distancias entre cazadores y zorros
    def distance_to_fox(self):
        distance = 0
        for piece in self.get_all_pieces(BLACK):
            distance = distance + abs(self.foxPos[0] - piece.row) + abs(self.foxPos[1] - piece.col)
        return distance

    #para calcular la posición "abierta" de los cazadores
    def distance_between_blacks(self):
        distance = 0
        minX = 8
        maxX = 0
        minY = 8
        maxY = 0
        for piece in self.get_all_pieces(BLACK):
            if piece.row > maxY :
                maxY = piece.row
            if piece.col > maxX :
                maxX = piece.col
            if piece.row < minY :
                minY = piece.row
            if piece.col < minX :
                minX = piece.row
        return (maxX - minX) * 2 + (maxY - minY) * 3 + maxX *2

    #función que comprueba si el zorro va a ganar
    #"simular" un estado sucesor sin calcularlo
    def will_win(self):
        for move in self.get_valid_moves(self.get_piece(self.foxPos[0], self.foxPos[1])):
            if move[0] == 0:
                return 1000000
        return 0

    #mover una pieza en el tablero - pieza es la pieza, fila y col son los nuevos indicadores de posición
    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        self.board_debug[piece.row][piece.col], self.board_debug[row][col] = self.board_debug[row][col], self.board_debug[piece.row][piece.col]
        if piece.tipo == fi:
            self.foxPos = (row, col)
            self.prevFoxPos = (piece.row, piece.col)
        piece.move(row, col)


    #función para comprobar el estado final
    def winner(self):
            piece = self.get_piece(self.foxPos[0], self.foxPos[1])
            if self.foxPos[0] == 0:
                return 'Fox'
            elif not self.get_valid_moves(piece) :
                return 'Hounds'
            else:
                return None

    #pieza getter en el tablero - se utiliza principalmente para la depuración durante la realización del tema
    def get_piece(self, row, col):
        return self.board[row][col]

    #tabla en memoria - 0 donde no tengo piezas, Objeto pieza donde tengo pieza
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 1 :
                        self.board[row].append(HunterPiece(row, col, hi))
                    elif row == 7 and col == 4:
                        self.board[row].append(FoxPiece(row,col, fi))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)


    #construir la matriz de la placa en la forma necesaria para la depuración - donde tengo piezas muestro su tipo, de lo contrario muestro el color en la placa    
    def _init_board_debug(self):
        for row in range(ROWS):
            self.board_debug.append([])
            for col in range(COLS):
                if isinstance(self.board[row][col], FoxPiece):
                    if str(self.board[row][col]) == str(fi) :
                        self.board_debug[row].append("Fox")
                    else:
                        self.board_debug[row].append("Hound")
                else:
                    if row%2 == 0:
                        if col%2 == 1:
                            self.board_debug[row].append("BLACK")
                        else:
                            self.board_debug[row].append("WHITE")
                    else:
                        if col%2 == 0:
                            self.board_debug[row].append("BLACK")
                        else:
                            self.board_debug[row].append("WHITE")
        return self.board_debug

    #visualización de la tabla almacenada para depuración
    def debug_print(self):
        if self.board_debug == []:
            self._init_board_debug()
        for row in range(ROWS):
            print(self.board_debug[row])


    #función para dibujar piezas en el tablero
    def draw(self, window):
        self.draw_board(window)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0 :
                    piece.position_piece(window)

    #función para averiguar las posiciones en las que se puede mover una pieza en un momento dado
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.tipo == fi:
            moves.update(self._traverse_left(row-1, max(row-3, -1), -1, piece.tipo, left))
            moves.update(self._traverse_right(row-1, max(row-3, -1), -1, piece.tipo, right))
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.tipo, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.tipo, right))


        if piece.tipo == hi:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.tipo, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.tipo, right))
        return moves

    #función para mover una pieza en diagonal
    #posición inicial, posición final, dirección, tipo de la pieza, columna izquierda    
    def _traverse_left(self, start, stop, step, tipo, left, skipped=[]):

        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0 :
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r + 3, ROWS)
                break
            elif current.tipo == fi or current.tipo == hi:
                break
            else:
                last = [current]

            left -= 1

        return moves

    #análoga a la función anterior, pero para los movimientos a la derecha
    def _traverse_right(self, start, stop, step, tipo, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                break
            elif current.tipo == fi or current.tipo == hi:
                break
            else:
                last = [current]

            right += 1

        return moves

#piese
class HunterPiece:

    def __init__(self, row, col, tipo):
        self.row = row
        self.col = col
        self.tipo = tipo

        self.x = 0
        self.y = 0
        self.pos()

    #la posición de una pista en la pantalla
    def pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 5
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 15

    #cambiar de posición después de desplazarse
    def move(self, row, col):
        self.row = row
        self.col = col
        self.pos()

    #Posicionar cada pieza de los cazadores dentro de sus cuadros
    def position_piece(self, window):
        hi = window.blit(cazador, (self.x, self.y))

class FoxPiece:

    def __init__(self, row, col, tipo):
        self.row = row
        self.col = col
        self.tipo = tipo

        self.x = 0
        self.y = 0
        self.pos()

    #la posición de una pista en la pantalla
    def pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 7
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 14

    #cambiar de posición después de desplazarse
    def move(self, row, col):
        self.row = row
        self.col = col
        self.pos()

    #Posicionar la pieza del zorro dentro del cuadro
    def position_piece(self, window):
        fi = window.blit(zorro, (self.x, self.y))
        
class Game:
    def __init__(self, window):
        self.selected = None
        self._init()
        self.window = window

    #comprobar la condición de victoria
    def update(self):
        self.board.draw(self.window)
        if self.selected:
            self.draw_valid_moves(self.valid_moves)
        if self.board.winner() == 'Fox':
            
            font = pygame.font.Font('freesansbold.ttf', 50)
            text = font.render(' !!         ZORRO GANA         !!', True, ORANJE)
            window.blit(text, (0, 325))
            pygame.display.update()
            time.sleep(4)
            exit(1)

        elif self.board.winner() == 'Hounds':
            
            font = pygame.font.Font('freesansbold.ttf', 45)
            text = font.render('!!      CAZADORES GANAN      !!', True, ORANJE)
            window.blit(text, (0, 325))
            pygame.display.update()
            time.sleep(4)
            exit(1)

        else:
            pass
        pygame.display.update()

    def _init(self):
        self.board = Board()
        self.turn = fi
        self.valid_moves = {}
        self.board.debug_print()

    #función que selecciona una pista y muestra los movimientos válidos
    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            #movimiento inválido => reanudar intento de movimiento
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        #si cambio la parte - utilizada para depurar
        if piece != 0 and piece.tipo == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        return False

    #función para moverse en el rango
    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            self.board.debug_print()
            self.change_turn()
        else:
            return False
        return True

    #función para dibujar los posibles movimientos de una pista
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.window, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 20)

    #función de alternancia del reproductor
    def change_turn(self):
        self.valid_moves = []
        if self.turn == fi:
            self.turn = hi
        else:
            self.turn = fi

    def get_board(self):
        return self.board

    #función para movimientos informáticos
    def ai_move(self, board):
        self.board = board
        self.change_turn()

#algoritmo minimax - posición es el estado en el tablero, depth es la profundidad del árbol, max_player - bool que comprueba si se elige min o max.
def minmax(position, depth, max_player):
    
    if depth == 0 or position.winner() != None:
        return position.alternate_evaluate(), position
    if position.winner() != None:
        exit(1)
    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, fi):
            evaluation = minmax(move, depth - 1, False)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        return maxEval, best_move

    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, hi):
            evaluation = minmax(move, depth - 1, True)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        return minEval, best_move


#función auxiliar de simulación de movimientos para minimax
def simulate_move(piece, move, board):
    board.move(piece, move[0], move[1])
    return board

#devuelve todos los movimientos posibles para una categoría de piezas
#la función sucesora que almacena los estados a los que conducen los posibles movimientos simulados
def get_all_moves(board, tipo):
    moves = []
    for piece in board.get_all_pieces(tipo):
        valid_moves = board.get_valid_moves(piece)
        for move in valid_moves.keys():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board)
            moves.append(new_board)
    return moves

#que me da la posición del ratón en la matriz
def get_pos_mouse(pos):
    x,y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

#main para correr el juego
def run(depth):
    running = True
    clock = pygame.time.Clock()
    game = Game(window)
    pygame.init()
    while running:
        clock.tick(60)

        if game.turn == fi:
            value, new_board = minmax(game.get_board(), depth, True)
            game.ai_move(new_board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_pos_mouse(pos)
                game.select(row, col)

        game.update()
    pygame.quit()
#run
run(4)
input()


