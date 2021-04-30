import sys, pygame
import asyncio
from abc import ABC, abstractmethod

#Глобальные
pygame.init()
show_tips = True
white_color = pygame.Color(255,255,255)
black_color = pygame.Color(65,25,0)
green_color = pygame.Color(0,255,0)
tips_color = pygame.Color(80,80,80)
transormation_bg_color = pygame.Color(105, 105, 105)
debug_mode = True # Позволяет играть самим с собой
size = width, height = 900, 640
chess_board_size = 640
cell_size = chess_board_size / 8
cell_move_radius = cell_size/4
screen = pygame.display.set_mode(size)

current_player_color = True
current_position = [] 
current_state =  None # Хранит текущее состояние
current_available_moves = [] #Доступные ходы
current_available_cells = [] #Доступные точки нужны для отображения
ranks = ['A','B','C','D','E','F','G','H']
files = [i for i in range(1,9)]

current_context = None #Для обратной связи
font_size = 20
font = pygame.font.SysFont('didot.ttc', font_size)

chessmen = {
    "bP": pygame.image.load("./resources/alpha/bP.png"),
    "bN": pygame.image.load("./resources/alpha/bN.png"),
    "bB": pygame.image.load("./resources/alpha/bB.png"),
    "bK": pygame.image.load("./resources/alpha/bK.png"),
    "bQ": pygame.image.load("./resources/alpha/bQ.png"),
    "bR": pygame.image.load("./resources/alpha/bR.png"),
    "wP": pygame.image.load("./resources/alpha/wP.png"),
    "wN": pygame.image.load("./resources/alpha/wN.png"),
    "wB": pygame.image.load("./resources/alpha/wB.png"),
    "wK": pygame.image.load("./resources/alpha/wK.png"),
    "wQ": pygame.image.load("./resources/alpha/wQ.png"),
    "wR": pygame.image.load("./resources/alpha/wR.png")
    
}
#Рисуем доску и подсказки
def draw_board(player_color = 1, dedicated_cell = None):
    player_color = 1
    screen.fill(pygame.Color(0,0,0))
    #Нарисование доски
    for rank in range(1,9):
        for file in range(1,9): 
            pygame.draw.rect(screen,
                            black_color if (file + rank + player_color) % 2 == 0 else white_color,
                            pygame.Rect(chess_board_size - cell_size * file,
                                        chess_board_size - cell_size * rank, 
                                        cell_size,
                                        cell_size))
    if dedicated_cell:
        pygame.draw.rect(screen,
        green_color,                          
        pygame.Rect(cell_size * dedicated_cell[1],
                                            cell_size * dedicated_cell[0], 
                                            cell_size,
                                            cell_size,
                                            width = 1,))
    if show_tips:
        if player_color:
            for i in range (len(files)):
                img_rank = font.render(ranks[i], True, tips_color)
                img_file = font.render(str(files[7-i]), True, tips_color)
                screen.blit(img_rank,
                            (i*cell_size,
                            chess_board_size - font_size))
                screen.blit(img_file,
                            (0,
                            cell_size/2 + i*cell_size - img_file.get_size()[1]/2))
        else:
            for i in range (len(files)):
                img_rank = font.render(ranks[7-i], True, tips_color)
                img_file = font.render(str(files[i]), True, tips_color)
                screen.blit(img_rank,
                            (cell_size +i*cell_size - img_rank.get_size()[0],
                            0))
                screen.blit(img_file,
                            (chess_board_size - img_file.get_size()[0],
                            cell_size/2 + i*cell_size - img_file.get_size()[1]/2))
        
        
    pygame.display.flip()

def drawchessman(position, player_color):
    global current_player_color
    current_player_color = player_color
    for i in range(8):
        for j in range(8):
            pos_figure = position[i][j]
            if pos_figure != None:
                fig = chessmen[pos_figure]
                screen.blit(fig, pygame.Rect(
                j*cell_size,
                i*cell_size,
                cell_size,
                cell_size))
    pygame.display.flip()
    return

def draw_transformation_window(rank, player_color):
    '''
    Функция отрисовки полей для выбора превращение пешки: Ферзь, Слон и т.д.
    '''
    color_figure = 'w' if current_player_color else 'b'
    files_to_draw = [0, 1, 2, 3] if player_color else [7, 6, 5, 4]
    transformation_figures = ['Q', 'R', 'B', 'K']
    for i in range(len(files_to_draw)):
        pygame.draw.circle(
            screen, 
            transormation_bg_color, 
            ((int)(rank * cell_size + cell_size/2), (int)(files_to_draw[i]*cell_size +cell_size/2)), 
            (int)(cell_size / 2),
            width=0)
        fig = chessmen[color_figure + transformation_figures[i]]
        screen.blit(
            fig, 
            pygame.Rect(
            rank*cell_size,
            i*cell_size,
            cell_size,
            cell_size))
    pygame.display.flip()


def draw_figure_moves():
    '''Отрисовка ходов'''
    for i in current_available_cells:
        pygame.draw.circle(
            screen,
            green_color,
            ((int)(i.get_to()[1]) * cell_size + cell_size/2, 
            (int)(i.get_to()[0])*cell_size +cell_size/2), 
            cell_move_radius, width = 0)
    pygame.display.flip()

def show_moves(file_rank):
    global current_available_cells
    #обычные фигуры 
    current_available_cells = [i for i in current_available_moves if (int)(i.get_from()[0]) == file_rank[0] and (int)(i.get_from()[1]) == file_rank[1]]
    draw_figure_moves()

def handle_click(pos):
    #отметить зеленым если фигура ваша
    file_rank = ((int)(pos[1]/cell_size), (int)(pos[0]/cell_size))
    #на случай нажатия за пределы клеток
    if file_rank[0] > 7 or file_rank[1] > 7:
        return
    current_state.process(current_position, file_rank)


#Функция отрисовки
def draw(position, player_color, avaiable_moves):
    global current_position
    global current_available_moves
    global current_state
    current_state = default_state()
    current_available_moves = avaiable_moves
    current_position = position
    draw_board(player_color)
    drawchessman(current_position, player_color)
    
async def input_check():
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif event.type ==pygame.MOUSEBUTTONUP:
                handle_click(event.pos)

start_position = [["bR","bN","bB","bQ","bK","bB","bN","bR"],
                    ["bP","bP","bP","bP","bP","bP","bP","bP"],
                    [None,None,None,None,None,None,None,None],
                    [None,None,None,None,None,None,None,None],
                    [None,None,None,None,None,None,None,None],
                    [None,None,None,None,None,None,None,None],
                    ["wP","wP","wP","wP","wP","wP","wP","wP"],
                    ["wR","wN","wB","wQ","wK","wB","wN","wR"]
]
# Абстрактный класс для состояния
class state(ABC):
    def process(self, position, file_rank):
        pass

# Класс обычного состояния
class default_state(state):
    def process(self, position, file_rank):
        draw_board(current_player_color, file_rank)
        drawchessman(current_position,current_player_color)
        # Обработка нажатия на клетку
        color_figure = 'w' if current_player_color else 'b'
        fig = current_position[file_rank[0]][file_rank[1]]
        if fig != None and fig[0] == color_figure:

            
            # Показ доступных ходов
            show_moves(file_rank)
            # Переход к состоянию figure_state
            transition_to(figure_state())

        pass

class figure_state(state):
    def process(self, position, file_rank):
        draw_board(current_player_color)
        drawchessman(current_position,current_player_color)
        # Обработка нажатия на клетку
        for i in current_available_cells: 
        # Если выбран доступный ход - его выполнение(передача в core)
        # Нужно полностью находить ход
            if (int)(i.get_to()[0]) == file_rank[0] and (int)(i.get_to()[1]) == file_rank[1]:
                #Если это ход пешки на последнюю горизнталь
                if i.is_pt():
                    draw_transformation_window(file_rank[1], current_player_color)
                    transition_to(transformation_state(i))
                    return
                # Передать ход в core
                current_context.core.player_make_move(i)
                # Переход к состоянию enemy_state
                if debug_mode:
                    transition_to(default_state())
                else:
                    transition_to(enemy_state())
                return
        # Иначе - переход в default_state
        current_state =  default_state()
        current_state.process(position, file_rank)
        
        pass

class enemy_state(state):
    def process(self, position, file_rank):
        # Обработка нажатия - не происходит
        # Предопределение ходов в будущем
        pass

class transformation_state(state):
    ''' Состояние описывает поведение графического модуля
    во время выбора фигуры для трансформации пешка -> фигура'''
    def __init__(self, move):
        self.expected_move = move
        self.files = [0, 1, 2, 3] if move.get_player_color() else [7, 6, 5, 4]
    
    def process(self, position, file_rank):
        move_rank = self.expected_move.get_to_int()[1]
        #Если это нажатие на одну из кнопок превращение
        if file_rank[1] == move_rank:
            for i in range(len(self.files)):
                if self.files[i] == file_rank[0]:
                    trans_figures = ['1', '2', '3', '4']
                    self.expected_move.trans_to_figure(trans_figures[i])
                    current_context.core.player_make_move(self.expected_move)
                    if debug_mode:
                        transition_to(default_state())
                    else:
                        transition_to(enemy_state())
                    return
        else:
            transition_to(default_state())
            current_state.process(position, file_rank)

        pass
    


class graphic_context():
    def __init__(self, core_context):
        self.core = core_context

def init_context(core_context):
    global current_context
    current_context = graphic_context(core_context)
# Функция перехода в другое состояние
def transition_to(new_state: state):
    global current_state
    current_state = new_state

