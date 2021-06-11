#Нахождение всех ходов в циврофой нотации
import time
import move_class as mc
import copy
King = '5' 
Queen = '1' # вроде работает
Rook = '2' # вроде работает
Bishop = '3' # вроде работает
Knight = '4' # вроде работает
tm = time.time()
def find_chess_moves(player_color, position, castling_data, last_move):
    all_exists_moves = []
    color_char = 'w' if player_color else 'b'
    for file in range(8):
        for rank in range(8):
            pos_fig = position[file][rank]
            if pos_fig != None and pos_fig[0] == color_char:
                figure_char = pos_fig[1]
                if figure_char == 'P':
                    all_exists_moves += find_pawn_moves(player_color, position, rank, file, last_move)
                elif figure_char == 'N':
                    all_exists_moves += find_knight_moves(player_color, position, rank, file)
                elif figure_char == 'R':
                    all_exists_moves += find_rook_moves(player_color, position, rank, file)
                elif figure_char == 'B':
                   all_exists_moves += find_bishop_moves(player_color, position, rank, file)
                if figure_char == 'Q': 
                    all_exists_moves += find_queen_moves(player_color, position, rank, file)
                if figure_char == 'K':
                    all_exists_moves += find_king_moves(player_color, position, rank, file, castling_data)
    return all_exists_moves

#ran3k - A-H, fi3les = 1-8
def find_queen_moves(player_color, position, rank, file):
    return find_bishop_moves(player_color, position, rank, file) + find_rook_moves(player_color, position, rank, file)

def find_knight_moves(player_color, position, rank, file):
    oponent_color = 'b' if player_color else 'w'
    current_pos_dig_not = digital_notation(file,rank)
    all_knight_moves = []
    default_knight_moves = [[-2, -1], [-2, 1], [2, -1], [2, 1], [-1, -2], [1, -2], [-1, 2], [1, 2]]
    for i in default_knight_moves:
        # не выходить за пределы
        cache_file = file + i[0]
        cache_rank = rank + i[1]
        if (0 <= cache_file <=7) and (0 <= cache_rank <=7)  and cell_have_chessman(oponent_color, position[cache_file][cache_rank]):
            all_knight_moves.append(mc.CMove(player_color,current_pos_dig_not, digital_notation(cache_file,cache_rank)))
    return all_knight_moves

def find_bishop_moves(player_color, position, rank, file):
    oponent_color = 'b' if player_color else 'w'
    current_pos_dig_not = digital_notation(file,rank)
    all_bishop_moves = []
    default_bishop_moves = [[-1, 1], [1, 1],[1, -1], [-1, -1]]
    for j in default_bishop_moves:
        for i in range(1,8):
            # не выходить за пределы
            cache_file = file + j[0] * i
            cache_rank = rank + j[1] * i
            if (0 <= cache_file <=7) and (0 <= cache_rank <=7):
                if position[cache_file][cache_rank] == None:
                    all_bishop_moves.append(mc.CMove(player_color,current_pos_dig_not, digital_notation(cache_file,cache_rank)))
                elif cell_have_chessman(oponent_color, position[cache_file][cache_rank], False):
                    all_bishop_moves.append(mc.CMove(player_color,current_pos_dig_not, digital_notation(cache_file,cache_rank)))
                    break
                else:
                    break
            else:
                break
    return all_bishop_moves

def find_rook_moves(player_color, position, rank, file):
    oponent_color = 'b' if  player_color else 'w'
    current_pos_dig_not = digital_notation(file,rank)
    all_rock_moves = []
    default_rock_moves = [[-1, 0], [1, 0],[0, -1], [0, 1]]
    for j in default_rock_moves:
        for i in range(1,8):
            # не выходить за пределы
            cache_file = file + j[0] * i
            cache_rank = rank + j[1] * i
            if (0 <= cache_file <=7) and (0 <= cache_rank <=7):
                if position[cache_file][cache_rank] == None:
                    all_rock_moves.append(mc.CMove(player_color,current_pos_dig_not, digital_notation(cache_file,cache_rank)))
                elif cell_have_chessman(oponent_color, position[cache_file][cache_rank], False):
                    all_rock_moves.append(mc.CMove(player_color,current_pos_dig_not, digital_notation(cache_file,cache_rank)))
                    break
                else:
                    break
            else:
                break
    return all_rock_moves


def find_pawn_moves(player_color, position, rank, file, last_move):
    oponent_color = 'b' if player_color else 'w'
    current_pos_dig_not = digital_notation(file,rank)
    player_move_direction = -2 * player_color  + 1
    all_pawn_moves = []
    cache_file = file + player_move_direction
    if cache_file >7 or cache_file<0: return []
    # Ходы вперед
    if position[cache_file][rank] == None:
        if (cache_file)%7 ==0:
            #Превращение пешек
            all_pawn_moves.append(mc.CMove(player_color,current_pos_dig_not, digital_notation(cache_file,rank), True))
        else:
            all_pawn_moves.append(mc.CMove(player_color,current_pos_dig_not, digital_notation(cache_file,rank)))
            if (((int)(3.5 - player_move_direction * 1.5) * player_move_direction > file * player_move_direction ) and # до 3 полосы - два хода пешкой
            position[file + 2 * player_move_direction][rank] == None): 
                all_pawn_moves.append(mc.CMove(player_color,current_pos_dig_not, digital_notation(file + 2 * player_move_direction,rank), aisle=True))
    
    #Взятие другие фигур
    if (rank + 1 <= 7  and 
        cell_have_chessman(oponent_color, position[cache_file][rank + 1], False)):
        if (cache_file)%7 ==0:
            #Превращение пешек
            all_pawn_moves.append(mc.CMove(player_color,current_pos_dig_not, digital_notation(cache_file,rank + 1), True))
        else:
            all_pawn_moves.append(mc.CMove(player_color,current_pos_dig_not, digital_notation(cache_file,rank + 1)))
    
    if (rank - 1 >= 0  and 
        cell_have_chessman(oponent_color, position[cache_file][rank - 1], False)):
        if (cache_file)%7 ==0:
            #Превращение пешек
            all_pawn_moves.append(mc.CMove(player_color,current_pos_dig_not, digital_notation(cache_file,rank - 1), True))
        else:
            all_pawn_moves.append(mc.CMove(player_color,current_pos_dig_not, digital_notation(cache_file,rank - 1)))

    #Взятие на проходе
    if (last_move != None and
        last_move.get_allow_aisle() and
        #На той же высоте
        (4 - 1 *  player_color) == last_move.get_to_int()[0] == file and
        # На сосеедней клетке
        abs(rank - last_move.get_to_int()[1]) == 1):
            all_pawn_moves.append(mc.CMove(player_color,current_pos_dig_not, digital_notation(cache_file,rank + (last_move.get_to_int()[1] - rank))))
    return all_pawn_moves

def find_king_moves(player_color, position, rank, file, castling_data):
    oponent_color = 'b' if player_color else 'w'
    current_pos_dig_not = digital_notation(file,rank)
    all_king_moves = []
    kings_default_move = [[1,-1], [1,0], [1,1],
                         [0,-1], [0,1],
                         [-1,-1], [-1,0], [-1,1]]
    #Обычные  ходы
    for moves in kings_default_move:
        if (0<= file + moves[0] <= 7 and
            0<= rank + moves[1] <= 7):
            if cell_have_chessman(oponent_color, position[file + moves[0]][rank + moves[1]]):
                all_king_moves.append(mc.CMove(player_color,current_pos_dig_not, digital_notation(file + moves[0],rank + moves[1])))
    #Рокировка
    #Короткая 0-0
    #Проверка на позицию короля - не нужна, так как передвижение короля, шахи и т.д учитывает castling_data
    if (castling_data[0] and 
        position[file][rank + 1] == None and
        position[file][rank + 2] == None):
        all_king_moves.append(mc.CMove(player_color,"00"))
    #Длинная 0-0-0
    if (castling_data[1] and
        position[file][rank - 1] == None and
        position[file][rank - 2] == None and
        position[file][rank - 3 ] == None):
        all_king_moves.append(mc.CMove(player_color,"000"))


    return all_king_moves

#цифровая нотация
def digital_notation(cell_file, cell_rank):
    return  (str)(cell_file) + (str)(cell_rank)

def cell_have_chessman(color_char, cell, allow_none = True):
    if cell == None:
        if allow_none:
            return True
        else:
            return False
    elif cell[0] == color_char:
        return True

def check_shah(position, player_color):
    #Нашли короля
    player_color_char =  'w' if player_color else 'b'
    oponent_color_char = 'b' if player_color  else 'w'
    king_position = [0,0]
    flag_king = False
    for file in range(len(position)):
        for rank in range(len(position[file])):
            if position[file][rank] == player_color_char + 'K':
                king_position = [file, rank]
                flag_king = True
                break
        if flag_king:
            break
    #Ищем пешки
    pawn_position = [[1 - 2*player_color, -1],[1 - 2*player_color, 1]]
    for possible_pos in pawn_position:
        figure_posit = [king_position[0] + possible_pos[0], king_position[1] + possible_pos[1]]
        if (0 <=figure_posit[0] <=7 and 0 <=figure_posit[1] <=7):
            if position[figure_posit[0]][figure_posit[1]] == oponent_color_char + 'P':
                return False
    #Ищем слонов и ферзя
    signs = [[1,1], [-1,1], [1,-1], [-1,-1]]
    for i in range(len(signs)):
        for j in range (1,8):
            figure_posit = [king_position[0] + j * signs[i][0], king_position[1] + j * signs[i][1]]
            if (0 <=figure_posit[0] <=7 and 0 <=figure_posit[1] <=7):
                cache_pos = position[figure_posit[0]][figure_posit[1]]
                #Черные фигуры
                if cache_pos == oponent_color_char + 'B' or cache_pos == oponent_color_char + 'Q':
                    return False
                #Пусто
                elif cache_pos == None:
                    continue
                #Белые фигуры
                else:
                    break
            else:
                break

    #Ищем ладью  и ферзя
    signs = [[1,0], [-1,0], [0,-1], [0,1]]
    for i in range(len(signs)):
        for j in range (1,8):
            figure_posit = [king_position[0] + j * signs[i][0], king_position[1] + j * signs[i][1]]
            if (0 <=figure_posit[0] <=7 and 0 <=figure_posit[1] <=7):
                cache_pos = position[figure_posit[0]][figure_posit[1]]
                #Черные фигуры
                if cache_pos == oponent_color_char + 'R' or cache_pos == oponent_color_char + 'Q':
                    return False
                #Пусто
                elif cache_pos == None:
                    continue
                #Белые фигуры
                else:
                    break
    #Ищем Конь
    signs = [[-2, -1], [-2, 1], [2, -1], [2, 1], [-1, 2], [1, 2], [-1, -2], [1, -2]]
    for i in signs:
        figure_posit = [king_position[0] + i[0], king_position[1] + i[1]]
        if (0 <=figure_posit[0] <=7 and 0 <=figure_posit[1] <=7):
            cache_pos = position[figure_posit[0]][figure_posit[1]]
            if cache_pos == oponent_color_char + 'N':
                return False

    signs = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
    for i in signs:
        figure_posit = [king_position[0] + i[0], king_position[1] + i[1]]
        if (0 <=figure_posit[0] <=7 and 0 <=figure_posit[1] <=7):
            cache_pos = position[figure_posit[0]][figure_posit[1]]
            if cache_pos == oponent_color_char + 'K':
                return False
    return True

def find_moves(position, player_color, player_castl, last_move):
    '''
    Поиск всех возможных корректных ходов
    '''
    #Возможные ходы
    possible_moves = []
    # Moves without check by shah - ходы которые потенциально не могу быть произведены
    move_wcbs = find_chess_moves(player_color, position, player_castl[player_color], last_move)
    #Необходимо проверить их
    move_next_position = None
    for i in move_wcbs:
        i_move = i.get_move()
        move_check_result = False
        #Рокировка
        if len(i_move)<4:
            if len(i_move)> 2:
                #Длинная рокировка
                move_check_result = check_castling_shah(position,player_color, True)
            else:
                #Коротка рокировка
                move_check_result = check_castling_shah(position,player_color, False)
        else:
            move_next_position = make_move(position, i, player_color, player_castl, last_move)[0]
            move_check_result =  check_shah(move_next_position, player_color)
        if move_check_result:
             possible_moves.append(i)
    if possible_moves == []:
        if not check_shah(move_next_position, player_color):
            color = "white" if player_color else "black"
            print(color + " lose!")
        else:
            print("pat")
    return possible_moves

def make_move(global_position, i_move, current_player_color, players_castling, last_move):
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
            '4': 'N'
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
        if (last_move != None and
            last_move.get_allow_aisle() and
            figure[1] == 'P' and 
            global_position[next_position_figure[0]][next_position_figure[1]] == None and
            current_position_figure[1] != next_position_figure[1]):
            cache = last_move.get_to_int()
            position[cache[0]][cache[1]] = None

        
    #Длинная рокировка "000"
    elif len(move) > 2:
        king_file = (int)(7 - 7 * (not current_player_color))
        #Проверяем нет ли шахов по пути на рокировку
        position[king_file][4], position[king_file][2] = None , position[king_file][4]
        position[king_file][3], position[king_file][0] = position[king_file][0], None
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
    if not check_shah(position, player_color):
        return False
    king_file = (int)(7 - 7 * (not player_color))
    position[king_file][4], position[king_file][5 - 2 * long_castling] = None , position[king_file][4]
    if not check_shah(position, player_color):
        return False
    position[king_file][5 - 2 * long_castling], position[king_file][6 - 4 * long_castling] = None , position[king_file][5 - 2 * long_castling]
    if not check_shah(position, player_color):
        return False
    return True

start_position = [["wR",None,None,None,"wK",None,"wN","wR"],
                    ["wP","wP","wP","wP","wP","wP","wP","wP"],
                    [None,None,None,None,None,None,None,None],
                    [None,None,None,"bR",None,None,"bQ",None],
                    [None,"bN",None,None,"bB",None,None,None],
                    [None,None,None,None,None,None,None,None],
                    ["bP","bP","bP","bP","bP","bP","bP","bP"],
                    ["bR","bN","bB","bQ","bK","bB","bN","bR"]
]
#result = find_chess_moves(1, start_position)
#print(result)
#print("\n vremya " +(str)(time.time() - tm) )
