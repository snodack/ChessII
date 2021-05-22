
# нотации Форсайта—Эдвардса 
def to_fen(state, current_color, castling, last_move, count_move, last_pawn_move=0):
    #position
    fen_state = ''
    for hor_i in range(len(state)):
        hor = state[hor_i]
        hor_string = ''
        if hor_i != 0:
            hor_string = '/'
        hor_empty_place = 0
        for cell in hor:
            if cell == None:
                hor_empty_place+=1
            else:
                if hor_empty_place!=0:
                    hor_string += str(hor_empty_place)
                hor_empty_place = 0
                if cell[0]=='b':
                    hor_string+=cell[1].lower()
                else: 
                    hor_string+=cell[1]
        if hor_empty_place!=0:
                        hor_string += str(hor_empty_place)
        fen_state += hor_string
    player_char = 'w' if current_color else 'b'
    fen_state += f' {player_char} '

    #castling
    cast_string = ''
    if castling[1][0] or castling[1][1]:
        if castling[1][0]: cast_string += 'K'
        if castling[1][1]: cast_string += 'Q'
    #black   
    if castling[0][0] or castling[0][1]:
        if castling[0][0]: cast_string += 'k'
        if castling[0][1]: cast_string += 'q'
    if cast_string != '':
        fen_state +=cast_string
    else:
        fen_state += '-'

    #pawn
    if last_move.get_allow_aisle():
        def_move = last_move.get_def_format()
        if last_move.player_color:
            fen_state += f' {def_move[2]}3'
        else: 
            fen_state += f' {def_move[2]}6'
    else:
        fen_state +=' -'

    fen_state += f' {last_pawn_move}'
    fen_state += f' {count_move}'
    return fen_state

