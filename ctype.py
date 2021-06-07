import ctypes
global_position = [["bR","bN","bB","bQ","bK","bB","bN","bR"],
                    ["bP","bP","bP","bP","bP","bP","bP","bP"],
                    [None,None,None,None,None,None,None,None],
                    [None,None,None,None,None,None,None,None],
                    [None,None,None,None,None,None,None,None],
                    [None,None,None,None,None,None,None,None],
                    ["wP","wP","wP","wP","wP","wP","wP","wP"],
                    ["wR","wN","wB","wQ","wK","wB","wN","wR"]
]
class PyItem:
    def __init__(self, value, name):
        self.value = value
        self.name = name

class CItem(ctypes.Structure):
    _fields_ = [
                 ('value', ctypes.c_int),
                 ('name', ctypes.c_wchar_p)
                ]

def create_list(size):
    return [[PyItem(int(str(i+1)+str(j+1)), global_position[i][j] if global_position[i][j] else "") for j in range(size)] for i in range(size)]

def py_list2c_array(py_list, size):
    rowType = CItem * size
    resultType = ctypes.POINTER(CItem) * size
    result = resultType()
    for i in range(size):
        row = rowType()
        for j in range(size):
            row[j] = CItem()
            row[j].value = py_list[i][j].value
            row[j].name = ctypes.c_wchar_p(py_list[i][j].name)
        result[i] = ctypes.cast(row, ctypes.POINTER(CItem))
    return ctypes.cast(result, ctypes.POINTER(ctypes.POINTER(CItem)))

if __name__ == '__main__':
    sLib = ctypes.cdll.LoadLibrary('D:\\ChessII\\c_segment\\chess_dl\\x64\\Debug\\chess_dl.dll')

    size = 8
    py_list = create_list(size)
    c_array = py_list2c_array(py_list, size)

    sLib.eval_func.argtypes = [ctypes.POINTER(ctypes.POINTER(CItem)), ctypes.c_size_t]
    sLib.eval_func.restype = ctypes.c_float
    result = sLib.eval_func(c_array, ctypes.c_size_t(size))
    print('Результат: {}'.format(result))