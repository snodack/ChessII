#на вход нейронке будем падавать транспонированную матрицу позиции из-за rank
current_player_color = True
players_castling = [(True, True), (True, True)]
stack_position = []
stack_move = []
def make_move(position, move):
        global stack_position
        global stack_move
        global players_castling
        global current_player_color
    # Ходы с превращением пешки
    if len(move) > 4:
        return
    # Обычные ходы
    elif len(move) > 3:
        
        stack_position.append(position)
        stack_move.append(move)

        current_position_figure = ((int)(move[1]), (int)(move[0]));
        next_position_figure = ((int)(move[4]), (int)(move[3]))
        figure = position[current_position_figure[0][1]] 
        current_position_figure[0][1] = None
        position[next_position_figure[0][1]] = figure
       
        # Убираем возможность рокировки
        if figure[1] == 'K':
            players_castling[current_player_color] = (False, False)
        if (current_position_figure[1] == 7 and current_position_figure[0] == int(7 - 7 * current_player_color )):
            players_castling[current_player_color][0] == False
        elif (current_position_figure[1] == 0 and current_position_figure[0] == int(7 - 7 * current_player_color )):
            players_castling[current_player_color][1] == False
        
         current_player_color = !current_player_color

        return position
    #Длинная рокировка
    elif len(move) > 2:
        position[int(7 - 7 * current_player_color][4], position[int(7 - 7 * current_player_color][2] = None , position[int(7 - 7 * current_player_color][4]
        position[int(7 - 7 * current_player_color][3], position[int(7 - 7 * current_player_color][1] = position[int(7 - 7 * current_player_color][7], None
        return
    #Короткая рокировка
    else:
        position[int(7 - 7 * current_player_color][4], position[int(7 - 7 * current_player_color][6] = None , position[int(7 - 7 * current_player_color][4]
        position[int(7 - 7 * current_player_color][5], position[int(7 - 7 * current_player_color][7] = position[int(7 - 7 * current_player_color][7], None
        return


    