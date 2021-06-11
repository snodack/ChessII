from tkinter import *
from tkinter import ttk


window = Tk()  
window.title("Дипломная работа Григорьев Е.О. ПРО-116")  
window.geometry('400x250')  
lbl = Label(window, text="Для начала работы, выберете цвет", font=("Arial Bold", 16))
lbl.pack()
lbl2 = Label(window, text="Глубина работы бота", font=("Arial Bold", 12))
lbl2.pack()
depth =ttk.Combobox(window, 
                            values=[
                                    1, 
                                    2,
                                    3,
                                    4,
                                    5,
                                    6,
                            ])
depth.current(3)
depth.pack()

def start_white_game():
    from core import start
    a = depth.current()+1
    window.destroy()
    start(True, a)
def start_black_game():
    from core import start
    a = depth.current()+1
    window.destroy()
    start(False, a)
    
button = Button(
    text="Черный",
    width=10,
    height=5,
    bg="black",
    fg="white",
    command=start_black_game
)
button2 = Button(
    text="Белый",
    width=10,
    height=5,
    bg="white",
    fg="black",
    command=start_white_game
)



button.pack(side="left",expand=2)
button2.pack(side="right", expand=2)
window.mainloop()
