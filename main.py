import tkinter as tk

import global_manager as gm
from gui.login_page import LoginPage
from database import db

gm.root = tk.Tk()
LoginPage()
gm.root.mainloop()
db.close()
