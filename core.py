import move_finder as mf
import graphic as gc
#на вход нейронке будем падавать транспонированную матрицу позиции из-за rank
current_player_color = True
players_castling = [(True, True), (True, True)]
stack_position = []
stack_move = []
start_position = [["bR","bN","bB","bQ","bK","bB","bN","bR"],
                    ["bP","bP","bP","bP","bP","bP","bP","bP"],
                    [None,None,None,None,None,None,None,None],
                    [None,None,None,None,None,None,None,None],
                    [None,None,None,None,None,None,None,None],
                    [None,None,None,None,None,None,None,None],
                    ["wP","wP","wP","wP","wP","wP","wP","wP"],
                    ["wR","wN","wB","wQ","wK","wB","wN","wR"]
]

def make_move(position, move):
    # Ходы с превращением пешки
    if len(move) > 4:
        figures = {
            '1': 'Q',
            '2': 'R',
            '3': 'B',
            '4': 'K'
        }
        color_figure = 'w' if current_player_color else 'b'
        current_position_figure = ((int)(move[1]), (int)(move[0]));
        next_position_figure = ((int)(move[3]), (int)(move[2]))
        position[next_position_figure[0]][1] = color_figure + figures[moves[4]]
        position[current_position_figure[0]][current_position_figure[1]] = None
    # Обычные ходы
    elif len(move) > 3:

        current_position_figure = ((int)(move[1]), (int)(move[0]));
        next_position_figure = ((int)(move[3]), (int)(move[2]))
        figure, position[current_position_figure[1]][current_position_figure[0]] = position[current_position_figure[1]][current_position_figure[0]], None
       
        # Убираем возможность рокировки
        if figure[1] == 'K':
            players_castling[current_player_color] = (False, False)
        if (current_position_figure[1] == 7 and current_position_figure[0] == int(7 - 7 * current_player_color )):
            players_castling[current_player_color][0] == False
        elif (current_position_figure[1] == 0 and current_position_figure[0] == int(7 - 7 * current_player_color )):
            players_castling[current_player_color][1] == False
        
    #Длинная рокировка
    elif len(move) > 2:
        king_file = (int)(7 - 7 * current_player_color)
        #Проверяем нет ли шахов по пути на рокировку
        position[king_file][4], position[king_file][2] = None , position[king_file][4]
        position[king_file][3], position[king_file][1] = position[king_file][7], None
    #Короткая рокировка
    else:
        king_file = (int)(7 - 7 * current_player_color)
        position[king_file][4], position[king_file][6] = None , position[king_file][4]
        position[king_file][5], position[king_file][7] = position[king_file][7], None
    return (position, players_castling)

def check_castling_shah(position, player_color, long_castling):
    if not mf.check_shah(position, player_color):
        return False
    king_file = (int)(7 - 7 * current_player_color)
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
        move_check_result = False
        #Рокировка
        if len(i)<4:
            if len(i)> 2:
                move_check_result = check_castling_shah(position,current_player_color, True)
            else:
                move_check_result = check_castling_shah(position,current_player_color, True)
        else:
            move_next_position = make_move(position, i)[0]
            move_check_result =  mf.check_shah(move_next_position, current_player_color)
        if move_check_result:
             possible_moves.append(i)
    return possible_moves
    
def start(position, player_color):
    global current_player_color
    current_player_color = player_color
    possible_moves = find_moves(position)
    gc.draw(position, player_color, possible_moves)
    gc.input_check()
    print('hi')

start(start_position, current_player_color)



    