import move_finder as mf
#на вход нейронке будем падавать транспонированную матрицу позиции из-за rank
current_player_color = True
players_castling = [(True, True), (True, True)]
stack_position = []
stack_move = []

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
        figure = position[current_position_figure[0][1]]
        position[current_position_figure[0]][current_position_figure[1]] = None
        position[next_position_figure[0][1]] = figure
       
        # Убираем возможность рокировки
        if figure[1] == 'K':
            players_castling[current_player_color] = (False, False)
        if (current_position_figure[1] == 7 and current_position_figure[0] == int(7 - 7 * current_player_color )):
            players_castling[current_player_color][0] == False
        elif (current_position_figure[1] == 0 and current_position_figure[0] == int(7 - 7 * current_player_color )):
            players_castling[current_player_color][1] == False
        
    #Длинная рокировка
    elif len(move) > 2:
        #Проверяем нет ли шахов по пути на рокировку
        position[int(7 - 7 * current_player_color][4], position[int(7 - 7 * current_player_color][2] = None , position[int(7 - 7 * current_player_color][4]
        position[int(7 - 7 * current_player_color][3], position[int(7 - 7 * current_player_color][1] = position[int(7 - 7 * current_player_color][7], None
    #Короткая рокировка
    else:
        position[int(7 - 7 * current_player_color][4], position[int(7 - 7 * current_player_color][6] = None , position[int(7 - 7 * current_player_color][4]
        position[int(7 - 7 * current_player_color][5], position[int(7 - 7 * current_player_color][7] = position[int(7 - 7 * current_player_color][7], None
    return (position, players_castling)

def check_castling_shah(position, player_color, long_castling):
    if !mf.check_shah(position, player_color):
        return False
    position[int(7 - 7 * current_player_color][4], position[int(7 - 7 * current_player_color][5 - 2 * long_castling] = None , position[int(7 - 7 * current_player_color][4]
    if !mf.check_shah(position, player_color):
        return False
    position[int(7 - 7 * current_player_color][5 - 2 * long_castling], position[int(7 - 7 * current_player_color][6 - 4 * long_castling] = None , position[int(7 - 7 * current_player_color][5 - 2 * long_castling]
    if !mf.check_shah(position, player_color):
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
            move_next_position = make_move(position, i)
            move_check_result =  mf.check_shah(move_next_position, current_player_color)
         if move_check_result:
             possible_moves.append(i)
    





    