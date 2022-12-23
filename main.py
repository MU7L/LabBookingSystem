from tkinter import Tk

import global_manager as gm
from gui.login_page import LoginPage
from database import db

gm.root = Tk()
LoginPage()
gm.root.mainloop()
print(gm.user['name'], '退出')
db.close()
