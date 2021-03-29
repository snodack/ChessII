import sys, pygame
pygame.init()
white_color = pygame.Color(255,255,255)
black_color = pygame.Color(65,25,0)
tips_color = pygame.Color(0,255,0)
size = width, height = 900, 640
chess_board_size = 640
cell_size = chess_board_size / 8
screen = pygame.display.set_mode(size)

ranks = ['A','B','C','D','E','F','G','H']
files = [i for i in range(1,9)]

font_size = 20
font = pygame.font.SysFont('didot.ttc', font_size)

chessmen = {
    "bP": pygame.image.load("D:/diplom/resources/alpha/bP.png"),
    "bN": pygame.image.load("D:/diplom/resources/alpha/bN.png"),
    "bB": pygame.image.load("D:/diplom/resources/alpha/bB.png"),
    "bK": pygame.image.load("D:/diplom/resources/alpha/bK.png"),
    "bQ": pygame.image.load("D:/diplom/resources/alpha/bQ.png"),
    "bR": pygame.image.load("D:/diplom/resources/alpha/bR.png"),
    "wP": pygame.image.load("D:/diplom/resources/alpha/wP.png"),
    "wN": pygame.image.load("D:/diplom/resources/alpha/wN.png"),
    "wB": pygame.image.load("D:/diplom/resources/alpha/wB.png"),
    "wK": pygame.image.load("D:/diplom/resources/alpha/wK.png"),
    "wQ": pygame.image.load("D:/diplom/resources/alpha/wQ.png"),
    "wR": pygame.image.load("D:/diplom/resources/alpha/wR.png")
    
}
#Рисуем доску и подсказки
def draw_board(player_color = 1, show_tips = True):
    screen.fill(pygame.Color(0,0,0))
    #Нарисование доски
    for rank in range(1,9):
        for file in range(1,9): 
            pygame.draw.rect(screen,
                            black_color if (file + rank + player_color) % 2 == 0 else white_color,
                            pygame.Rect(chess_board_size - cell_size * file,
                                        chess_board_size - cell_size * rank, 
                                        cell_size,
                                        cell_size))
    if show_tips:
        if player_color:
            for i in range (len(files)):
                img_rank = font.render(ranks[i], True, tips_color)
                img_file = font.render(str(files[7-i]), True, tips_color)
                screen.blit(img_rank,
                            (i*cell_size,
                            chess_board_size - font_size))
                screen.blit(img_file,
                            (0,
                            cell_size/2 + i*cell_size - img_file.get_size()[1]/2))
        else:
            for i in range (len(files)):
                img_rank = font.render(ranks[7-i], True, tips_color)
                img_file = font.render(str(files[i]), True, tips_color)
                screen.blit(img_rank,
                            (cell_size +i*cell_size - img_rank.get_size()[0],
                            0))
                screen.blit(img_file,
                            (chess_board_size - img_file.get_size()[0],
                            cell_size/2 + i*cell_size - img_file.get_size()[1]/2))
        
        
    pygame.display.flip()

def drawchessman(position, player_color = 1):
    if player_color:
        for i in range(8):
            for j in range(8):
                pos_figure = position[i][j]
                if pos_figure != None:
                    fig = chessmen[pos_figure]
                    screen.blit(fig, pygame.Rect(
                    j*cell_size,
                    i*cell_size,
                    cell_size,
                    cell_size))
    else:
        for i in range(8):
            for j in range(8):
                pos_figure = position[i][j]
                if pos_figure != None:
                    fig = chessmen[pos_figure]
                    screen.blit(fig, pygame.Rect(
                    (7-j)*cell_size,
                    (7-i)*cell_size,
                    cell_size,
                    cell_size))
    pygame.display.flip()
    return
start_position = [["bR","bN","bB","bQ","bK","bB","bN","bR"],
                    ["bP","bP","bP","bP","bP","bP","bP","bP"],
                    [None,None,None,None,None,None,None,None],
                    [None,None,None,None,None,None,None,None],
                    [None,None,None,None,None,None,None,None],
                    [None,None,None,None,None,None,None,None],
                    ["wP","wP","wP","wP","wP","wP","wP","wP"],
                    ["wR","wN","wB","wQ","wK","wB","wN","wR"]
]
draw_board()
drawchessman(start_position)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
   