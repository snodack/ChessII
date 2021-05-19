def get_actions():
    CELL = 8
    moves = []
    default_rock_moves = [[-1, 0], [1, 0],[0, -1], [0, 1]]
    default_bishop_moves = [[-1, 1], [1, 1],[1, -1], [-1, -1]]
    default_knight_moves = [[-2, -1], [-2, 1], [2, -1], [2, 1], [-1, -2], [1, -2], [-1, 2], [1, 2]]

    count = 0
    for file in range(8):
        for rank in range(8):
            #Ладья
            for j in default_rock_moves:
                for i in range(1,8):
                    cache_file = file + j[0] * i
                    cache_rank = rank + j[1] * i
                    if (0 <= cache_file <=7) and (0 <= cache_rank <=7):
                        moves.append(str(file)+ str(rank) + str(cache_file)+ str(cache_rank))
                    else:
                        break
            #Слон
            for j in default_bishop_moves:
                for i in range(1,8):
                # не выходить за пределы
                    cache_file = file + j[0] * i
                    cache_rank = rank + j[1] * i
                    if (0 <= cache_file <=7) and (0 <= cache_rank <=7):
                        moves.append(str(file)+ str(rank) + str(cache_file)+ str(cache_rank))
                    else:
                        break
            #Конь
            for i in default_knight_moves:
                # не выходить за пределы
                cache_file = file + i[0]
                cache_rank = rank + i[1]
                if (0 <= cache_file <=7) and (0 <= cache_rank <=7):
                    moves.append(str(file)+ str(rank) + str(cache_file)+ str(cache_rank))
    return moves

                    
