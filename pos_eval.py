from copy import Error
from types import TracebackType
import move_finder as mf
from multiprocessing.dummy import Pool as ThreadPool
def evaluate(eval_func, position, castling, current_player , last_move, depth):
    if depth == 0:
        return eval_func(position)
    #Генерируем следующий позиции
    moves = mf.find_moves(position, current_player, castling, last_move)

    evals = []
    gen_pos = lambda mv: mf.make_move(position, mv, current_player, castling, last_move)
    positions = list(map(gen_pos, moves))
    eval_pos = lambda pos_i: evaluate(eval_func, positions[pos_i][0], positions[pos_i][1], not current_player, moves[pos_i], depth-1)
    evals = list(map(eval_pos, list(range(len(moves)))))
    bestmax = 0
    for i in range(1,len(evals)):
        if evals[i] > evals[bestmax]:
            bestmax = i
    return evals[i]

def evaluate_root(eval_func, position, castling, current_player , last_move,depth = 4):
    '''
    Функция полной оценки

    Параметры:
    eval_func -> функция оценки текущей позиции
    position -> текущая позиция
    depth -> глубина поиска
    
    Вызывается рекурсивно
    Возвращает оценку, положительно -> перевес в сторону белых, отрицательно -> в сторону черныx

    '''
    if depth == 0 or depth > 16:
        raise Error("Ошибка задачи глубины")
    #Генерируем следующий позиции
    moves = mf.find_moves(position, current_player, castling, last_move)
    evals = []
    pool = ThreadPool(4)
    gen_pos = lambda mv: mf.make_move(position, mv, current_player, castling, last_move)
    positions = pool.map(gen_pos, moves)
    eval_pos = lambda pos_i: evaluate(eval_func, positions[pos_i][0], positions[pos_i][1], not current_player, moves[pos_i], depth-1)
    evals = pool.map(eval_pos, list(range(len(moves))))

    bestmax = 0
    for i in range(1,len(evals)):
        if evals[i] > evals[bestmax]:
            bestmax = i
    return moves[bestmax]
    
        

global_position = [["bR","bN","bB","bQ","bK","bB","bN","bR"],
                    ["bP","bP","bP","bP","bP","bP","bP","bP"],
                    [None,None,None,None,None,None,None,None],
                    [None,None,None,None,None,None,None,None],
                    [None,None,None,None,None,None,None,None],
                    [None,None,None,None,None,None,None,None],
                    ["wP","wP","wP","wP","wP","wP","wP","wP"],
                    ["wR","wN","wB","wQ","wK","wB","wN","wR"]
]


def simple_eval_position(position):
    '''
    Оценка текущей позиции с помощью таблиц
    '''
    figure_price = {"K": 900, "Q": 90,  "R":50, "B":30, "N": 30, "P": 10}
    tables = {
        "K": [
        [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [ -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
        [ -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
        [  2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0 ],
        [  2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0 ]
        ],
        "Q":  [
        [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
        [ -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
        [ -1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
        [ -0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
        [  0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
        [ -1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
        [ -1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
        [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
        ],
        "R": [
        [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [  0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
        [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
        [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
        [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
        [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
        [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
        [  0.0,   0.0, 0.0,  0.5,  0.5,  0.0,  0.0,  0.0]
        ],
        "N": [
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
        [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
        [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
        [-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
        [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
        [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
        [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
        ],
        "B": [
        [ -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
        [ -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
        [ -1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
        [ -1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
        [ -1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
        [ -1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
        [ -1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
        [ -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
        ],
        "P": [
        [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
        [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
        [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
        [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
        [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
        [0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5],
        [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
        ]
    }
    eval_result = 0
    for file_i in range(len(position)):
        row = position[file_i]
        for elem_j in range(len(row)):
            cell = row[elem_j]
            if cell ==None:
                continue
            figure = cell[1]
            if cell[0] == 'w':
                eval_result += figure_price[figure] + tables[figure][file_i][elem_j]
            else:
                eval_result -= figure_price[figure] + tables[figure][abs(file_i-7)][elem_j]
    return eval_result

def test():
    a = list(range(20))
    pool = ThreadPool(5)
    test_lam = lambda a: test_func(a, 3)
    result = pool.map(test_lam, a)
    print(result)

def test_func(a_piece, b):
    return -a_piece + b
av = evaluate_root(simple_eval_position, global_position, [(True, True), (True, True)], True, None)
print(av)