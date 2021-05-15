import chess_gym as gs

chess_env = gs.Chess_Environment()
chess_state = chess_env.reset()
for i in range (4000):
    game  = chess_env.game_state
    a ,b,c,d = chess_env.step(i)
    if b > -10:
        print(i)
a = chess_env.game_state
print(a)