import importlib
import move_finder as mf
import graphic as gc
import copy
import asyncio
import fen_notation as fen
current_player_color = True
players_castling = [(True, True), (True, True)]
stack_position = []
stack_move = [None]
global_position = [["bR","bN","bB","bQ","bK","bB","bN","bR"],
                    ["bP","bP","bP","bP","bP","bP","bP","bP"],
                    [None,None,None,None,None,None,None,None],
                    [None,None,None,None,None,None,None,None],
                    [None,None,None,None,None,None,None,None],
                    [None,None,None,None,None,None,None,None],
                    ["wP","wP","wP","wP","wP","wP","wP","wP"],
                    ["wR","wN","wB","wQ","wK","wB","wN","wR"]
]

class core_context():
    def player_make_move(self, move):
        player_make_move(move)
    
def player_make_move(move):
    global global_position
    global players_castling
    global current_player_color
    global_position, players_castling = mf.make_move(global_position, move, current_player_color, players_castling, stack_move[-1])
    stack_move.append(move)
    current_player_color = not current_player_color
    fen_string = fen.to_fen(global_position, current_player_color, players_castling, stack_move[-1], len(stack_move)-1)
    gc.draw(global_position, current_player_color, mf.find_moves(global_position, current_player_color, players_castling, stack_move[-1]))


def start(position, player_color):
    global current_player_color
    position = position
    current_player_color = player_color
    possible_moves = mf.find_moves(global_position, current_player_color, players_castling, stack_move[-1])
    gc.draw(position, player_color, possible_moves)
    gc.init_context(core_context())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(gc.input_check())
start(global_position, current_player_color)




    