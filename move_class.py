#Классы для ходов #7
#Создать класс, в котором будет учитываться начальное поле и конечное поле и куда необходимо нажать 
# для этого ходп(пригодиться для рокировки и апргейда пешек). Также там можно иметь функцию преобразования 
# в книжный вид для отображения истории игры
class CMove:
    def __init__(self, player_color ,file_rank_from, file_rank_to = None, pawn_to = False):
        self.cell_from = file_rank_from
        self.cell_to = file_rank_to
        self.player_color = player_color
    def get_from(self):
        #Не рокировка
        if self.cell_to != None:
            return self.cell_from
        else:
            return (str)(7-7*(not self.player_color)) + '4'
    def get_to(self):
        #Не рокировка
        if self.cell_to != None:
            return self.cell_to
        #Длинная
        elif len(self.cell_from) > 2:
            return (str)(7-7*(not self.player_color)) + '2'
        #Короткая
        else:
            return (str)(7-7*(not self.player_color)) + '6'

    def get_move(self):
        if self.cell_to == None:
            return self.cell_from
        else:
            return self.cell_from + self.cell_to
