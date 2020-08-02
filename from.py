from tkinter import Tk, IntVar, Checkbutton, Button, W


def print_button_callback():
    global state
    for i in range(3):
        if state[i][1].get():
            print(state[i][0])

myApp=Tk()
state = [("Option {0}".format(i+1),IntVar()) for i in range(3)]

for i in range(3):
    Checkbutton(myApp, text=state[i][0], variable=state[i][1]).grid(row=i, sticky=W)

Button(myApp, text="Print", command=print_button_callback).grid(row=3, sticky=W)


myApp.mainloop()