from tkinter import Canvas, Tk

def main():
    print('hello world')

master = Tk()
canvas = Canvas(master, bg="black", height=32, width=64)

def hello(event):
    print(event.char)

master.bind('<Key s>', hello)
# canvas.bind('<Key>', hello)
canvas.pack()
canvas.mainloop()