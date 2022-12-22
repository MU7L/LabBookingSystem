import tkinter as tk
import tkinter.messagebox as tkm

from database import db
import global_manager as gm
from gui.teacher_page import TeacherPage
from gui.admin_page import AdminPage


class LoginPage:
    def __init__(self):
        # data
        self.data_username = tk.StringVar()
        self.data_password = tk.StringVar()

        # root
        gm.root.title('实验室预约系统 登录')
        gm.root.geometry(gm.set_size('size1'))

        # frame
        self.page = tk.Frame(gm.root)
        self.page.pack()

        label_acnt = tk.Label(self.page, text='账号：')
        label_pswd = tk.Label(self.page, text='密码：')
        entry_acnt = tk.Entry(self.page, textvariable=self.data_username)
        entry_pswd = tk.Entry(self.page, textvariable=self.data_password, show='*')
        btn_login = tk.Button(self.page, text='登录', command=lambda: self.btn_login_click())

        label_acnt.grid(row=0, column=0)
        label_pswd.grid(row=1, column=0)
        entry_acnt.grid(row=0, column=1)
        entry_pswd.grid(row=1, column=1)
        btn_login.grid(row=2, column=0)

    def btn_login_click(self):
        username = self.data_username.get()
        password = self.data_password.get()
        res, msg = db.check_login(username, password)
        # res, msg = db.check_login_test(0)  # 登录测试 0:admin 1:teacher
        if res:
            # 登录成功
            print(gm.user['name'], '登录成功')
            self.page.destroy()
            if gm.user['name'] == 'admin':
                AdminPage()
            else:
                TeacherPage()
        else:
            # 登录失败
            if not tkm.askretrycancel(title='登录失败', message=msg):
                gm.root.quit()


if __name__ == '__main__':
    gm.root = tk.Tk()
    LoginPage()
    gm.root.mainloop()
    db.close()
