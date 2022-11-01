import tkinter
import random


class Circle:
    colors = [
        "yellow",
        "blue",
        "red",
        "green",
        "purple",
        "pink",
        "orange",
        "white",
        "violet",
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = random.randint(10, 20)
        self.col = random.choice(Circle.colors)
        self.dx = random.randint(1, 8)
        self.dy = random.randint(1, 8)

    def draw(self, c):
        c.create_oval(
            self.x,
            self.y,
            self.x + self.r * 2,
            self.y + self.r * 2,
            fill=self.col,
        )

    def move(self, xlimit, ylimit):
        self.x += self.dx
        self.y += self.dy
        if self.x > xlimit or self.x < 0:
            self.dx = -self.dx
        if self.y > ylimit or self.y < 0:
            self.dy = -self.dy


class mainwnd:
    def __init__(self, wnd):
        self.mainFrame = tkinter.Frame(wnd)
        self.mainFrame.pack()
        self.lbl = tkinter.Label(self.mainFrame, text="My First Label")
        self.lbl.pack()
        self.btn = tkinter.Button(
            self.mainFrame, text="Push", command=self.buttonPressed
        )
        self.btn.pack()
        self.state = 0
        self.cvs = tkinter.Canvas(
            self.mainFrame, bg="black", width=400, height=300
        )
        self.cvs.bind("<Button-1>", self.somethingClicked)
        self.cvs.bind("<Button-3>", self.somethingClicked)
        self.cvs.pack()
        self.allCircles = []

    def buttonPressed(self):
        if self.state == 0:
            self.btn.configure(text="Pause")
            self.state = 1
        else:
            self.state = 0
            self.btn.configure(text="Push")
        self.cvs.delete(tkinter.ALL)
        self.allCircles.clear()
        # self.cvs.delete(random.choice(self.circles))

    def somethingClicked(self, e):
        # print(e.x,e.y)
        # self.cvs.create_oval(e.x,e.y,e.x+20,e.y+20,fill="blue")
        cir = Circle(e.x, e.y)
        cir.draw(self.cvs)
        self.allCircles.append(cir)

    def periodicFunction(self):
        self.cvs.delete(tkinter.ALL)
        for cir in self.allCircles:
            cir.move(400, 300)
            cir.draw(self.cvs)

        self.cvs.after(50, self.periodicFunction)


wnd = tkinter.Tk()
wnd.title("15-112 Rocks")
wnd.geometry("500x400")
print("Before main loop")

theApp = mainwnd(wnd)
theApp.cvs.after(500, theApp.periodicFunction)
# wnd.mainloop()


# lbl = tkinter.Label(wnd,text="My First Label")
# lbl.pack()
# btn = tkinter.Button(wnd,text="Push")
# btn.pack()

wnd.mainloop()

print("After main loop")
