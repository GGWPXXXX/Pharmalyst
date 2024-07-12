import tkinter as tk
from Controller import Controller


class Monitor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pharmalyst")
        self.geometry("1000x800")
        self.resizable(False, False)
        self.__canvas = tk.Canvas(self, width=1000, height=800)
        self.__canvas.place(x=0, y=0)
        self.__controller = Controller(self.__canvas, self)
        self.__controller.initial()


if __name__ == "__main__":
    app = Monitor()
    app.mainloop()
