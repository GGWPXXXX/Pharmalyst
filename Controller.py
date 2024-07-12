from FrontPage import FrontPage
import tkinter as tk


class Controller:

    def __init__(self, canvas: tk.Canvas, window: tk.Tk) -> None:
        self.__front = FrontPage(window)
        self.__canvas = canvas

    def initial(self):
        self.__front.welcome_page(self.__canvas)
