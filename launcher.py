from tkinter import *
from tkinter import ttk
from core import start

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
                                    7,
                                    8,
                                    9,])
depth.current(4)
depth.pack()

def start_white_game():
    a = depth.current()+1
    window.destroy()
    start(True, a)
    
button = Button(
    text="Черный",
    width=10,
    height=5,
    bg="black",
    fg="white",
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
