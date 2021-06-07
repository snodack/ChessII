from copy import Error
import ctypes
import random
from types import TracebackType
import move_finder as mf
from multiprocessing.dummy import Pool as ThreadPool

import time

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

def evaluate(eval_func, position, castling, current_player , last_move, depth, alpha, beta):
    if depth == 0:
        return -eval_func(position)
    #Генерируем следующий позиции
    moves = mf.find_moves(position, current_player, castling, last_move)
    if len(moves) == 0: return current_player*(-1)* 10000
    #Максимизация
    #Альфа бета отсечение
    if current_player:
        bestmove = -10000
        for move in moves:
            new_pos, castl = mf.make_move(position, move, current_player, castling, last_move)
            bestmove = max(bestmove, evaluate(eval_func, new_pos, castl, not current_player, move, depth - 1, alpha, beta ))
            alpha = max(alpha, bestmove);
            if (beta <= alpha):
                return bestmove
        return bestmove;
    else: #Минимализация
        bestmove = 10000
        for move in moves:
            new_pos, castl = mf.make_move(position, move, current_player, castling, last_move)
            bestmove = min(bestmove, evaluate(eval_func, new_pos, castl, not current_player, move, depth - 1, alpha, beta ))
            beta = min(beta, bestmove);
            if (beta <= alpha):
                return bestmove
        return bestmove;

def eval_test(position):
    return random.uniform(-30,30)
    
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
    pool = ThreadPool(16)
    gen_pos = lambda mv: mf.make_move(position, mv, current_player, castling, last_move)
    positions = pool.map(gen_pos, moves)
    eval_pos = lambda pos_i: evaluate(eval_func, positions[pos_i][0], positions[pos_i][1], not current_player, moves[pos_i], depth-1, -10001, 10001)
    evals = list(map(eval_pos, list(range(len(moves)))))
    if len(evals) == 0:
        return None
    bestmax = 0
    for i in range(1,len(evals)):
        if evals[i] < evals[bestmax]:
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


def py_list2c_list(py_list):
    c_list = ctypes.create_string_buffer(py_list.encode('utf-8'))
    return c_list

def test_func(a_piece, b):
    return -a_piece + b
'''
def c_eval(position):
    size = 8
    c_array = py_list2c_array(position, size)
    result = sLib.eval_func(c_array, ctypes.c_size_t(size))
    return result
'''

sLib = ctypes.cdll.LoadLibrary('D:\\ChessII\\c_segment\\chess_dl\\x64\\Release\\chess_dl.dll')
#sLib.eval_func.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), ctypes.c_size_t]
#sLib.eval_func.restype = ctypes.c_float
sLib.eval_c.argtypes = [ctypes.c_char_p, ctypes.c_int]
sLib.eval_c.restype =  ctypes.POINTER(ctypes.c_wchar_p)
#sLib.find_rock_moves.restype = ctypes.c_int

def c_evaluation(fem, depth):
    size = len(fem)
    c_list = py_list2c_list(fem)
    move = sLib.eval_c(c_list, depth)
    a = ctypes.c_wchar_p.from_buffer(move)
    move_string = a.value
    return move_string
    



