import move_finder as mf
import graphic as gc
import copy
import asyncio
#на вход нейронке будем падавать транспонированную матрицу позиции из-за rank
current_player_color = True
players_castling = [(True, True), (True, True)]
stack_position = []
stack_move = []
global_position = [["bR","bN","bB","bQ","bK","bB","bN","bR"],
                    ["bP","bP","bP","bP","bP","bP","wP","bP"],
                    [None,None,None,None,None,None,None,None],
                    [None,None,None,None,None,None,None,None],
                    [None,None,None,None,None,None,None,None],
                    [None,None,None,None,None,None,None,None],
                    ["wP","wP","wP","wP","wP","wP","wP","wP"],
                    ["wR","wN","wB","wQ","wK","wB","wN","wR"]
]

class core_context():
    def player_make_move(self, move):
        player_make_move(move)


def make_move(global_position, i_move):
    move = i_move.get_move()
    position = copy.deepcopy(global_position) #копия глобальной позиции - дабы не портить основу
    castling = copy.deepcopy(players_castling)
    color_figure = 'w' if current_player_color else 'b'
    # Ходы с превращением пешки
    if len(move) > 4:
        figures = {
            '1': 'Q',
            '2': 'R',
            '3': 'B',
            '4': 'K'
        }
        current_position_figure = ((int)(move[0]), (int)(move[1]));
        next_position_figure = ((int)(move[2]), (int)(move[3]))
        position[next_position_figure[0]][next_position_figure[1]] = color_figure + figures[move[4]]
        position[current_position_figure[0]][current_position_figure[1]] = None
    # Обычные ходы "2233"
    elif len(move) > 3:
        #Разбираем ход
        #Позиция фигуры до хода
        current_position_figure = ((int)(move[0]), (int)(move[1]));
        #Позиция фигуры после хода
        next_position_figure = ((int)(move[2]), (int)(move[3]))
        figure, position[current_position_figure[0]][current_position_figure[1]] = position[current_position_figure[0]][current_position_figure[1]], None
        position[next_position_figure[0]][next_position_figure[1]] = figure
        # Убираем возможность рокировки, при движении короля
        if figure[1] == 'K':
            castling[current_player_color] = (False, False)
        # Движение Ладьи справа(сбивает рокировки)
        if (current_position_figure[1] == 7 and current_position_figure[0] == int(7 - 7 * current_player_color )):
            castling[current_player_color][0] == False
        # Движение Ладьи слева(сбивает рокировки)
        elif (current_position_figure[1] == 0 and current_position_figure[0] == int(7 - 7 * current_player_color )):
            castling[current_player_color][1] == False
        
    #Длинная рокировка "000"
    elif len(move) > 2:
        king_file = (int)(7 - 7 * (not current_player_color))
        #Проверяем нет ли шахов по пути на рокировку
        position[king_file][4], position[king_file][2] = None , position[king_file][4]
        position[king_file][3], position[king_file][0] = position[king_file][7], None
        castling[current_player_color] = (False, False)
    #Короткая рокировка "00"
    else:
        king_file = (int)(7 - 7 * (not current_player_color))
        position[king_file][4], position[king_file][6] = None , position[king_file][4]
        position[king_file][5], position[king_file][7] = position[king_file][7], None
        castling[current_player_color] = (False, False)
    return (position, castling)

def check_castling_shah(check_position, player_color, long_castling):
    position = copy.deepcopy(check_position)
    #Если король под шахом ->выход
    if not mf.check_shah(position, player_color):
        return False
    king_file = (int)(7 - 7 * (not current_player_color))
    position[king_file][4], position[king_file][5 - 2 * long_castling] = None , position[king_file][4]
    if not mf.check_shah(position, player_color):
        return False
    position[king_file][5 - 2 * long_castling], position[king_file][6 - 4 * long_castling] = None , position[king_file][5 - 2 * long_castling]
    if not mf.check_shah(position, player_color):
        return False
    return True

def find_moves(position):
    #Возможные ходы
    possible_moves = []
    # Moves without check by shah - ходы которые потенциально не могу быть произведены
    move_wcbs = mf.find_chess_moves(current_player_color, position, players_castling[current_player_color])
    #Необходимо проверить их
    move_next_position = None
    for i in move_wcbs:
        i_move = i.get_move()
        move_check_result = False
        #Рокировка
        if len(i_move)<4:
            if len(i_move)> 2:
                #Длинная рокировка
                move_check_result = check_castling_shah(position,current_player_color, True)
            else:
                #Коротка рокировка
                move_check_result = check_castling_shah(position,current_player_color, False)
        else:
            move_next_position = make_move(position, i)[0]
            move_check_result =  mf.check_shah(move_next_position, current_player_color)
        if move_check_result:
             possible_moves.append(i)
    if possible_moves == []:
        if not mf.check_shah(move_next_position, current_player_color):
            color = "white" if current_player_color else "black"
            print(color + " lose!")
    return possible_moves
    
def player_make_move(move):
    global global_position
    global players_castling
    global current_player_color
    global_position, players_castling = make_move(global_position, move)
    current_player_color = not current_player_color
    gc.draw(global_position, current_player_color, find_moves(global_position))


def start(position, player_color):
    global current_player_color
    position = position
    current_player_color = player_color
    possible_moves = find_moves(position)
    gc.draw(position, player_color, possible_moves)
    gc.init_context(core_context())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(gc.input_check())
start(global_position, current_player_color)




    