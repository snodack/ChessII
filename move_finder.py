#Нахождение всех ходов в циврофой нотации
import time
King = 5 
Queen = 1 # вроде работает
Rook = 2 # вроде работает
Bishop = 3 # вроде работает
Knight = 4 # вроде работает
tm = time.time()
def find_chess_moves(player_color, position, castling_data = (True, True)):
    all_exists_moves = []
    color_char = 'w' if player_color else 'b'
    for file in range(8):
        for rank in range(8):
            pos_fig = position[file][rank]
            if pos_fig != None and pos_fig[0] == color_char:
                figure_char = pos_fig[1]
                if figure_char == 'P':
                    all_exists_moves += find_pawn_moves(player_color, position, rank, file)
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
    if file - 2 >= 0:
        if rank-1 >= 0 and cell_have_chessman(oponent_color, position[file-2][rank-1]):
            all_knight_moves.append(current_pos_dig_not*100 + digital_notation(file-2,rank-1))
        if rank + 1 <=7 and  cell_have_chessman(oponent_color, position[file-2][rank+1]):
             all_knight_moves.append(current_pos_dig_not*100 + digital_notation(file - 2,rank + 1))
    if file + 2 <=7:
        if rank-1 >= 0 and cell_have_chessman(oponent_color, position[file+2][rank-1]):
            all_knight_moves.append(current_pos_dig_not*100 + digital_notation(file + 2,rank - 1))
        if rank + 1 <=7 and cell_have_chessman(oponent_color, position[file+2][rank+1]):
             all_knight_moves.append(current_pos_dig_not*100 + digital_notation(file + 2,rank + 1))    
    if rank - 2 >= 0:
        if file-1 >= 0 and cell_have_chessman(oponent_color, position[file-1][rank-2]):
            all_knight_moves.append(current_pos_dig_not*100 + digital_notation(file - 1,rank - 2))
        if file + 1 <=7 and cell_have_chessman(oponent_color, position[file+1][rank-2]):
             all_knight_moves.append(current_pos_dig_not*100 + digital_notation(file + 1,rank - 2))
    if rank + 2 <= 7:
        if file-1 >= 0 and cell_have_chessman(oponent_color, position[file-1][rank + 2]):
            all_knight_moves.append(current_pos_dig_not*100 + digital_notation(file - 1,rank + 2))
        if file + 1 <=7 and cell_have_chessman(oponent_color, position[file+1][rank + 2]):
             all_knight_moves.append(current_pos_dig_not*100 + digital_notation(file + 1,rank + 2))
    return all_knight_moves

def find_bishop_moves(player_color, position, rank, file):
    oponent_color = 'b' if player_color else 'w'
    current_pos_dig_not = digital_notation(file,rank)
    all_bishop_moves = []
    for i in range(1,8):
        if (file + i <= 7  and
             rank + i <=7):
                if position[file + i][rank + i] == None:
                    all_bishop_moves.append(current_pos_dig_not*100 + digital_notation(file + i,rank + i))
                elif cell_have_chessman(oponent_color, position[file + i][rank + i], False):
                    all_bishop_moves.append(current_pos_dig_not*100 + digital_notation(file + i,rank + i))
                    break
                else:
                    break
        else:
                break
    for i in range(1,8):
        if (file + i <= 7  and
             rank - i >= 0):
            if position[file + i][rank - i] == None:
                all_bishop_moves.append(current_pos_dig_not*100 + digital_notation(file + i,rank - i))
            elif cell_have_chessman(oponent_color, position[file + i][rank - i], False):
                all_bishop_moves.append(current_pos_dig_not*100 + digital_notation(file + i,rank - i))
                break
            else:
                    break
        else:
                break
    
    for i in range(1,8):
        if (file - i >= 0  and
             rank - i >= 0):
            if position[file - i][rank - i] == None:
                all_bishop_moves.append(current_pos_dig_not*100 + digital_notation(file - i,rank - i))
            elif cell_have_chessman(oponent_color, position[file - i][rank - i], False):
                all_bishop_moves.append(current_pos_dig_not*100 + digital_notation(file - i,rank - i))
                break
            else:
                break
        else:
                break

    for i in range(1,8):
        if (file - i >= 0  and
             rank + i <=7):
            if position[file - i][rank + i] == None:
                all_bishop_moves.append(current_pos_dig_not*100 + digital_notation(file - i,rank + i))
            elif cell_have_chessman(oponent_color, position[file - i][rank + i], False):
                all_bishop_moves.append(current_pos_dig_not*100 + digital_notation(file - i,rank + i))
                break
            else:
                break
             
        else:
                break
    return all_bishop_moves

def find_rook_moves(player_color, position, rank, file):
    oponent_color = 'b' if  player_color else 'w'
    all_rock_moves = []
    current_pos_dig_not = digital_notation(file,rank)
    for i in ([j for j in range(-1,-8, -1)]):
        if (file + i >=0 and file + i <= 7):
            if position[file + i][rank] == None:
                all_rock_moves.append(current_pos_dig_not*100 + digital_notation(file + i,rank))
            elif cell_have_chessman(oponent_color, position[file + i][rank], False):
                all_rock_moves.append(current_pos_dig_not*100 + digital_notation(file + i,rank))
                break
            else:
                break
        else:
            break
    for i in ([j for j in range(1, 8)]):
        if (file + i >=0 and file + i <= 7):
            if position[file + i][rank] == None:
                all_rock_moves.append(current_pos_dig_not*100 + digital_notation(file + i,rank))
            elif cell_have_chessman(oponent_color, position[file + i][rank], False):
                all_rock_moves.append(current_pos_dig_not*100 + digital_notation(file + i,rank))
                break
            else:
                break
        else:
            break
    for i in ([j for j in range(-1,-8, -1)]):
        if (rank + i >=0):
            if position[file][rank + i] == None:
                all_rock_moves.append(current_pos_dig_not*100 + digital_notation(file,rank + i))
            elif cell_have_chessman(oponent_color, position[file][rank + i], False):
                all_rock_moves.append(current_pos_dig_not*100 + digital_notation(file,rank + i))
                break
            else:
                break
        else:
            break
    for i in ([j for j in range(1, 8)]):
        if (rank + i <=7 ):
            if position[file][rank + i] == None:
                all_rock_moves.append(current_pos_dig_not*100 + digital_notation(file,rank + i))
            elif cell_have_chessman(oponent_color, position[file][rank + i], False):
                all_rock_moves.append(current_pos_dig_not*100 + digital_notation(file,rank + i))
                break
            else:
                break
        else:
            break
    return all_rock_moves

def find_pawn_moves(player_color, position, rank, file):
    oponent_color = 'b' if player_color else 'w'
    current_pos_dig_not = digital_notation(file,rank)
    player_move_direction = 2 * player_color  - 1
    all_pawn_moves = []
    # Ходы вперед
    if position[file + player_move_direction][rank] == None:
        if file + player_move_direction == (int)(player_move_direction*3.5 + 3.5):
            all_pawn_moves.append(current_pos_dig_not*1000 + digital_notation(file + player_move_direction,rank)*10 + Queen)
            all_pawn_moves.append(current_pos_dig_not*1000 + digital_notation(file + player_move_direction,rank)*10 + Rook)
            all_pawn_moves.append(current_pos_dig_not*1000 + digital_notation(file + player_move_direction,rank)*10 + Bishop)
            all_pawn_moves.append(current_pos_dig_not*1000 + digital_notation(file + player_move_direction,rank)*10 + Knight)
        else:
            all_pawn_moves.append(current_pos_dig_not*100 + digital_notation(file + player_move_direction,rank))
        if (((int)(3.5 - player_move_direction * 1.5) * player_move_direction > file * player_move_direction ) and # до 3 полосы - два хода пешкой
        position[file + 2 * player_move_direction][rank] == None): 
            all_pawn_moves.append(current_pos_dig_not*100 + digital_notation(file + 2 * player_move_direction,rank))
    
    #Взятие другие фигур
    if (rank + 1 <= 7  and 
        cell_have_chessman(oponent_color, position[file + player_move_direction][rank + 1], False)):
        if rank == (int)(player_move_direction*3.5 + 3.5):
            all_pawn_moves.append(current_pos_dig_not*1000 + digital_notation(file + player_move_direction,rank + 1)*10 + Queen)
            all_pawn_moves.append(current_pos_dig_not*1000 + digital_notation(file + player_move_direction,rank + 1)*10 + Rook)
            all_pawn_moves.append(current_pos_dig_not*1000 + digital_notation(file + player_move_direction,rank + 1)*10 + Bishop)
            all_pawn_moves.append(current_pos_dig_not*1000 + digital_notation(file + player_move_direction,rank + 1)*10 + Knight)
        else:
            all_pawn_moves.append(current_pos_dig_not*100 + digital_notation(file + player_move_direction,rank + 1))
    
    if (rank - 1 >= 0  and 
        cell_have_chessman(oponent_color, position[file + player_move_direction][rank - 1], False)):
        if rank == (int)(player_move_direction*3.5 + 3.5):
            all_pawn_moves.append(current_pos_dig_not*1000 + digital_notation(file + player_move_direction,rank - 1)*10 + Queen)
            all_pawn_moves.append(current_pos_dig_not*1000 + digital_notation(file + player_move_direction,rank - 1)*10 + Rook)
            all_pawn_moves.append(current_pos_dig_not*1000 + digital_notation(file + player_move_direction,rank - 1)*10 + Bishop)
            all_pawn_moves.append(current_pos_dig_not*1000 + digital_notation(file + player_move_direction,rank - 1)*10 + Knight)
        else:
            all_pawn_moves.append(current_pos_dig_not*100 + digital_notation(file + player_move_direction,rank - 1))
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
                all_king_moves.append(current_pos_dig_not*100 + digital_notation(file + moves[0], rank + moves[1]))
    #Рокировка
    #Короткая 0-0
    if (castling_data[0] and
        position[file][rank + 1] == None and
        position[file][rank + 2] == None):
        all_king_moves.append("00")
    #Длинная 0-0-0
    if (castling_data[1] and
        position[file][rank - 1] == None and
        position[file][rank - 2] == None and
        position[file][rank - 3 ] == None):
        all_king_moves.append("000")


    return all_king_moves


    
    

#цифровая нотация
def digital_notation(cell_file, cell_rank):
    return (cell_rank+1)*10 + cell_file+1

def cell_have_chessman(color_char, cell, allow_none = True):
    if cell == None:
        if allow_none:
            return True
        else:
            return False
    elif cell[0] == color_char:
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
result = find_chess_moves(0, start_position)
print(result)
print("\n vremya " +(str)(time.time() - tm) )
