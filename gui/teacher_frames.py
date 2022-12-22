import tkinter as tk

import global_manager as gm


class BookFrame(tk.Frame):
    def __init__(self):
        super().__init__(gm.root)
        tk.Label(self, text=self.__class__.__name__).pack()


class RecordFrame(tk.Frame):
    def __init__(self):
        super().__init__(gm.root)
        tk.Label(self, text=self.__class__.__name__).pack()


class InfoFrame(tk.Frame):
    def __init__(self):
        super().__init__(gm.root)
        tk.Label(self, text=self.__class__.__name__).pack()
