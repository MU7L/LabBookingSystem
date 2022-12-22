import tkinter as tk

import global_manager as gm
from database import db
from gui.teacher_frames import BookFrame, RecordFrame, InfoFrame


class TeacherPage:
    def __init__(self):
        # root
        gm.root.title('实验室预约系统 - {} (开发中)'.format(gm.user["name"]))
        gm.root.geometry('600x400')

        # 菜单栏
        menu = tk.Menu(gm.root)
        menu.add_command(label="预约实验室", command=lambda: self.cmd_to_frame(0))
        menu.add_command(label="查看预约记录", command=lambda: self.cmd_to_frame(1))
        menu.add_command(label="个人信息", command=lambda: self.cmd_to_frame(2))
        gm.root.config(menu=menu)

        # frames
        self.frames = [BookFrame(), RecordFrame(), InfoFrame()]
        self.frame_now = -1  # 没有 frame 时设置为 -1

    def cmd_to_frame(self, f):
        if self.frame_now != -1:
            self.frames[self.frame_now].pack_forget()
        self.frame_now = f
        self.frames[f].pack()


if __name__ == '__main__':
    gm.user = {
        "no": "1",
        "name": "从永年"
    }
    gm.root = tk.Tk()
    TeacherPage()
    gm.root.mainloop()
    db.close()
